
import json
import os
import uuid
from datetime import datetime, timezone

import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.environ.get("AWS_REGION", "us-east-1"),
   endpoint_url=os.environ.get(
    "LOCALSTACK_ENDPOINT",
    "http://172.17.0.2:4566",
),
)

table = dynamodb.Table(os.environ["TABLE_NAME"])


def response(status, data):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(data),
    }


def handler(event, context):
    method = event.get("requestContext", {}).get(
        "http", {}
    ).get("method", "GET")
    path = event.get("rawPath", "/")

    if path == "/health":
        return response(200, {"status": "healthy"})

    if path == "/tasks" and method == "POST":
        try:
            body = json.loads(event.get("body") or "{}")
        except json.JSONDecodeError:
            return response(400, {"error": "Invalid JSON"})

        task_name = body.get("task")

        if not isinstance(task_name, str) or not task_name.strip():
            return response(400, {"error": "Task is required"})

        item = {
            "id": str(uuid.uuid4()),
            "task": task_name.strip(),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        table.put_item(Item=item)
        return response(201, item)

    if path == "/tasks" and method == "GET":
        result = table.scan()
        return response(200, {"tasks": result.get("Items", [])})

    return response(404, {"error": "Route not found"})
