from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError
import json
import uuid
from dataclasses import dataclass


class ToolRecord:
    tool_id: str
    name: str
    description: str
    parameters_schema: Dict[str, Any]
    auth_data: Dict[str, Any]
    auth_type: str      # New field: e.g., 'api_key', 'oauth', 'aws_iam'
    auth_id: str        # New field: reference to auth configuration
    tool_type: str      # Python class name of the tool
    created_at: str
    updated_at: str
