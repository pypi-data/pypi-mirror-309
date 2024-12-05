import os
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError
import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class AgentRecord:
    account_id: str
    agent_id: str
    model_id: str
    model_provider: str
    modality: str
    instructions: str
    model_config: Dict[str, Any]
    agent_config: Dict[str, Any]
    auth_data: Dict[str, Any]
    tools: List[str]  # List of tool IDs
    created_at: str
    updated_at: str
    created_by: str
    updated_by: str
    tool_instances: Optional[List[Dict[str, Any]]] = None  # Full tool data

@dataclass
class ToolRecord:
    tool_id: str
    name: str
    description: str
    parameters_schema: Dict[str, Any]
    auth_data: Dict[str, Any]
    auth_type: str
    auth_id: str
    tool_type: str
    created_at: str
    updated_at: str
    created_by: str
    updated_by: str


class DynamoDBManager:
    def __init__(self, table_name: str, region: str = 'us-west-2'):
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        region_name = os.environ.get('AWS_REGION', 'us-west-2')  # Default to us-west-2 if not specified
        self.dynamodb = boto3.resource('dynamodb',
                                       aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key,
                                       region_name=region)
        self.table = self.dynamodb.Table(table_name)

    def _format_timestamp(self) -> str:
        return datetime.utcnow().isoformat()


class AgentDB(DynamoDBManager):
    def __init__(self, table_name: str = 'agents', region: str = 'us-west-2', tool_db: Optional['ToolDB'] = None):
        super().__init__(table_name, region)
        self.tool_db = tool_db or ToolDB(region=region)

    def create_agent(self, agent_record: AgentRecord) -> str:
        """Create a new agent record in DynamoDB."""
        try:
            if not agent_record.agent_id:
                agent_record.agent_id = str(uuid.uuid4())

            agent_record.created_at = self._format_timestamp()
            agent_record.updated_at = agent_record.created_at

            # Remove tool_instances before saving
            agent_dict = asdict(agent_record)
            agent_dict.pop('tool_instances', None)

            self.table.put_item(
                Item=agent_dict,
                ConditionExpression='attribute_not_exists(agent_id)'
            )
            return agent_record.agent_id
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ValueError(f"Agent with ID {agent_record.agent_id} already exists")
            raise

    def get_agent(self, account_id: str, agent_id: str, include_tools: bool = True) -> Optional[AgentRecord]:
        """
        Retrieve an agent record by ID.

        Args:
            account_id: The account ID
            agent_id: The agent ID
            include_tools: Whether to include full tool data (default: True)
        """
        try:
            response = self.table.get_item(
                Key={
                    'account_id': account_id,
                    'agent_id': agent_id
                }
            )

            if 'Item' not in response:
                return None

            agent_data = response['Item']

            # Fetch associated tools if requested
            if include_tools and agent_data.get('tools'):
                tool_records = self.tool_db.get_tools_by_ids(agent_data['tools'])
                agent_data['tool_instances'] = [asdict(tool) for tool in tool_records]
            else:
                agent_data['tool_instances'] = None

            return AgentRecord(**agent_data)
        except ClientError:
            raise

    def update_agent(self, agent_record: AgentRecord) -> bool:
        """Update an existing agent record."""
        try:
            agent_record.updated_at = self._format_timestamp()

            update_expression = []
            expression_values = {}
            expression_names = {}

            # Create dynamic update expression
            agent_dict = asdict(agent_record)
            agent_dict.pop('tool_instances', None)  # Remove tool_instances before updating

            for key, value in agent_dict.items():
                if key not in ['account_id', 'agent_id']:  # Skip primary keys
                    update_expression.append(f"#{key} = :{key}")
                    expression_values[f":{key}"] = value
                    expression_names[f"#{key}"] = key

            self.table.update_item(
                Key={
                    'account_id': agent_record.account_id,
                    'agent_id': agent_record.agent_id
                },
                UpdateExpression=f"SET {', '.join(update_expression)}",
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
                ConditionExpression='attribute_exists(agent_id)'
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ValueError(f"Agent with ID {agent_record.agent_id} does not exist")
            raise

    def delete_agent(self, account_id: str, agent_id: str) -> bool:
        """Delete an agent record."""
        try:
            self.table.delete_item(
                Key={
                    'account_id': account_id,
                    'agent_id': agent_id
                },
                ConditionExpression='attribute_exists(agent_id)'
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return False
            raise

    def list_agents(self, account_id: str, include_tools: bool = True) -> List[AgentRecord]:
        """
        List all agents for an account.

        Args:
            account_id: The account ID
            include_tools: Whether to include full tool data (default: True)
        """
        try:
            response = self.table.query(
                KeyConditionExpression='account_id = :account_id',
                ExpressionAttributeValues={':account_id': account_id}
            )

            agents = []
            for item in response.get('Items', []):
                if include_tools and item.get('tools'):
                    tool_records = self.tool_db.get_tools_by_ids(item['tools'])
                    item['tool_instances'] = [asdict(tool) for tool in tool_records]
                else:
                    item['tool_instances'] = None
                agents.append(AgentRecord(**item))

            return agents
        except ClientError:
            raise


class ToolDB(DynamoDBManager):
    def __init__(self, table_name: str = 'tools', region: str = 'us-west-2'):
        super().__init__(table_name, region)

    def create_tool(self, tool_record: ToolRecord) -> str:
        """Create a new tool record in DynamoDB."""
        try:
            if not tool_record.tool_id:
                tool_record.tool_id = str(uuid.uuid4())

            tool_record.created_at = self._format_timestamp()
            tool_record.updated_at = tool_record.created_at

            self.table.put_item(
                Item=asdict(tool_record),
                ConditionExpression='attribute_not_exists(tool_id)'
            )
            return tool_record.tool_id
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ValueError(f"Tool with ID {tool_record.tool_id} already exists")
            raise

    def get_tool(self, tool_id: str) -> Optional[ToolRecord]:
        """Retrieve a tool record by ID."""
        try:
            response = self.table.get_item(
                Key={'tool_id': tool_id}
            )
            if 'Item' in response:
                return ToolRecord(**response['Item'])
            return None
        except ClientError:
            raise

    def update_tool(self, tool_record: ToolRecord) -> bool:
        """Update an existing tool record."""
        try:
            tool_record.updated_at = self._format_timestamp()

            update_expression = []
            expression_values = {}
            expression_names = {}

            # Create dynamic update expression
            for key, value in asdict(tool_record).items():
                if key != 'tool_id':  # Skip primary key
                    update_expression.append(f"#{key} = :{key}")
                    expression_values[f":{key}"] = value
                    expression_names[f"#{key}"] = key

            self.table.update_item(
                Key={'tool_id': tool_record.tool_id},
                UpdateExpression=f"SET {', '.join(update_expression)}",
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
                ConditionExpression='attribute_exists(tool_id)'
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ValueError(f"Tool with ID {tool_record.tool_id} does not exist")
            raise

    def delete_tool(self, tool_id: str) -> bool:
        """Delete a tool record."""
        try:
            self.table.delete_item(
                Key={'tool_id': tool_id},
                ConditionExpression='attribute_exists(tool_id)'
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return False
            raise

    def list_tools(self, filter_criteria: Optional[Dict[str, Any]] = None) -> List[ToolRecord]:
        """List all tools, optionally filtered by criteria."""
        try:
            if filter_criteria:
                filter_expression = []
                expression_values = {}
                expression_names = {}

                for key, value in filter_criteria.items():
                    filter_expression.append(f"#{key} = :{key}")
                    expression_values[f":{key}"] = value
                    expression_names[f"#{key}"] = key

                response = self.table.scan(
                    FilterExpression=' AND '.join(filter_expression),
                    ExpressionAttributeValues=expression_values,
                    ExpressionAttributeNames=expression_names
                )
            else:
                response = self.table.scan()

            return [ToolRecord(**item) for item in response.get('Items', [])]
        except ClientError:
            raise

    def get_tools_by_ids(self, tool_ids: List[str]) -> List[ToolRecord]:
        """Retrieve multiple tools by their IDs."""
        try:
            # DynamoDB batch get items has a limit of 100 items
            chunk_size = 100
            all_tools = []

            for i in range(0, len(tool_ids), chunk_size):
                chunk = tool_ids[i:i + chunk_size]
                response = self.dynamodb.batch_get_item(
                    RequestItems={
                        self.table.name: {
                            'Keys': [{'tool_id': tid} for tid in chunk]
                        }
                    }
                )

                if self.table.name in response['Responses']:
                    all_tools.extend([ToolRecord(**item)
                                      for item in response['Responses'][self.table.name]])

            return all_tools
        except ClientError:
            raise