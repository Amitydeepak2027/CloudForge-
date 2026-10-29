
import json
import boto3
import unittest
import uuid


class TestTaskAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = boto3.client(
            "lambda",
            endpoint_url="http://localhost:4566",
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )

    def invoke_api(self, method, path, body=None):
        event = {
            "rawPath": path,
            "requestContext": {"http": {"method": method}},
        }

        if body is not None:
            event["body"] = json.dumps(body)

        response = self.client.invoke(
            FunctionName="cloudforge-api",
            Payload=json.dumps(event),
        )

        return json.loads(response["Payload"].read())

    def test_health(self):
        result = self.invoke_api("GET", "/health")
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(json.loads(result["body"])["status"], "healthy")

    def test_create_task(self):
        task_name = f"Test task {uuid.uuid4()}"
        result = self.invoke_api(
            "POST", "/tasks", {"task": task_name}
        )

        self.assertEqual(result["statusCode"], 201)
        task = json.loads(result["body"])
        self.assertEqual(task["task"], task_name)
        self.assertTrue(task["id"])

    def test_get_tasks(self):
        result = self.invoke_api("GET", "/tasks")

        self.assertEqual(result["statusCode"], 200)
        body = json.loads(result["body"])
        self.assertIn("tasks", body)
        self.assertIsInstance(body["tasks"], list)


if __name__ == "__main__":
    unittest.main()
