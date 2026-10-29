
# CloudForge

CloudForge is a serverless task management API built with Python, AWS Lambda, DynamoDB, and Terraform. It is designed for local development and testing using Docker and LocalEmu.

## Features

- Health check API
- Create tasks using POST /tasks
- Retrieve tasks using GET /tasks
- DynamoDB for task storage
- Terraform infrastructure as code
- Automated Python tests
- GitHub Actions workflow for CI checks

## Architecture

- **Python** — API logic
- **AWS Lambda** — serverless function
- **DynamoDB** — task storage
- **S3** — artifact storage
- **Terraform** — infrastructure provisioning
- **Docker and LocalEmu** — local AWS-like environment
- **GitHub Actions** — CI workflow

## Prerequisites

- Docker Desktop
- Terraform
- Python
- Python packages: boto3 and pytest

## Local Setup

1. Start Docker Desktop.
2. Start your LocalEmu container on port 4566.
3. Open a terminal in the project directory.
4. Initialize Terraform:

   ```powershell
   terraform init
   ```

5. Validate the configuration:

   ```powershell
   terraform validate
   ```

6. Apply infrastructure if needed:

   ```powershell
   terraform apply
   ```

## Run Tests

Install dependencies:

```powershell
python -m pip install boto3 pytest
```

Run the tests:

```powershell
python -m pytest -v
```

## API Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | /health | Check API health |
| POST | /tasks | Create a task |
| GET | /tasks | Retrieve tasks |

The API is currently tested by invoking the Lambda function directly through the local emulator.

## CI/CD

The GitHub Actions workflow is located at `.github/workflows/terraform-ci-cd.yml`. It checks Terraform formatting and configuration and runs Python tests. The Python test job must have its LocalEmu and Lambda test resources configured before it can pass on GitHub-hosted runners.

## Project Structure

```text
CloudForge/
├── .github/workflows/terraform-ci-cd.yml
├── lambda/app.py
├── tests/test_api.py
├── main.tf
├── providers.tf
├── variables.tf
├── outputs.tf
├── versions.tf
└── README.md
```

## Current Status

The local health, task creation, and task retrieval tests have passed. Terraform validation and planning have also succeeded.
