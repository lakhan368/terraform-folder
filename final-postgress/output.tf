output "db_instance_id" {
  description = "The ID of the RDS instance"
  value       = aws_db_instance.rds_instance.id
}

output "db_instance_endpoint" {
  description = "The endpoint of the RDS instance"
  value       = aws_db_instance.rds_instance.endpoint
}

output "db_instance_arn" {
  description = "The ARN of the RDS instance"
  value       = aws_db_instance.rds_instance.arn
}

output "db_instance_address" {
  description = "The address of the RDS instance"
  value       = aws_db_instance.rds_instance.address
}

output "db_instance_status" {
  description = "The status of the RDS instance"
  value       = aws_db_instance.rds_instance.status
}
