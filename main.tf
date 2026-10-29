
data "archive_file" "lambda_package" {
  type        = "zip"
  source_file = "${path.module}/lambda/app.py"
  output_path = "${path.module}/lambda_package.zip"
}

resource "aws_s3_bucket" "artifacts" {
  bucket = "${var.project_name}-artifacts"

  tags = {
    Project     = var.project_name
    ManagedBy   = "Terraform"
    Environment = "Local"
  }
}

resource "aws_dynamodb_table" "tasks" {
  name         = "${var.project_name}-tasks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Project = var.project_name
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_dynamodb" {
  name = "${var.project_name}-dynamodb-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:PutItem",
        "dynamodb:Scan"
      ]
      Resource = aws_dynamodb_table.tasks.arn
    }]
  })
}

resource "aws_lambda_function" "task_api" {
  timeout       = 30
  function_name = "${var.project_name}-api"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.handler"
  runtime       = "python3.12"

  filename         = data.archive_file.lambda_package.output_path
  source_code_hash = data.archive_file.lambda_package.output_base64sha256

  environment {
    variables = {
      TABLE_NAME          = aws_dynamodb_table.tasks.name
      LOCALSTACK_ENDPOINT = "http://172.17.0.2:4566"
    }
  }

  depends_on = [aws_iam_role_policy.lambda_dynamodb]

  tags = {
    Project = var.project_name
  }
}

resource "aws_lambda_function_url" "task_api" {
  function_name      = aws_lambda_function.task_api.function_name
  authorization_type = "NONE"
}
