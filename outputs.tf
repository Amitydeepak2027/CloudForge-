
output "api_url" {
  description = "Local Lambda Function URL"
  value       = aws_lambda_function_url.task_api.function_url
}

output "bucket_name" {
  value = aws_s3_bucket.artifacts.bucket
}

output "table_name" {
  value = aws_dynamodb_table.tasks.name
}
