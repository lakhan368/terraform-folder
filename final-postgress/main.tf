resource "aws_db_instance" "rds_instance" {
  identifier                    = var.identifier             # Change this to your desired identifier
  instance_class                = var.instance_class
  kms_key_id                    = var.kms_key_id
  vpc_security_group_ids        = var.vpc_security_group_ids
  allocated_storage             = var.allocated_storage
  auto_minor_version_upgrade    = var.auto_minor_version_upgrade
  backup_retention_period       = var.backup_retention_period
  backup_window                 = var.backup_window
  db_name                       = var.db_name
  db_subnet_group_name          = var.db_subnet_group_name
  enabled_cloudwatch_logs_exports = var.enabled_cloudwatch_logs_exports
  engine                        = var.engine
  engine_version                = var.engine_version
  maintenance_window            = var.maintenance_window
  max_allocated_storage         = var.max_allocated_storage
  multi_az                      = var.multi_az
  username                      = var.username
  password                      = var.password
  publicly_accessible           = var.publicly_accessible
  storage_encrypted             = var.storage_encrypted
  storage_type                  = var.storage_type
  skip_final_snapshot           = var.skip_final_snapshot
  final_snapshot_identifier     = var.final_snapshot_identifier
  tags                          = var.tags
  
}
