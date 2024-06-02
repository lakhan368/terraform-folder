# Required parameters
variable "identifier" {
  description = "(Required, Forces new resource) The name of the RDS instance"
  type        = string
}

variable "instance_class" {
  description = "(Required) The instance type of the RDS instance."
  type        = string
}

variable "kms_key_id" {
  description = "(Required) The ARN for the KMS encryption key. If creating an encrypted instance."
  type        = string
}

variable "vpc_security_group_ids" {
  description = "List of VPC security groups to associate."
  type        = list(any)
}

# Optional parameters
variable "allocated_storage" {
  description = "The allocated storage in gibibytes. If max_allocated_storage is configured, this argument represents the initial storage allocation and differences between this value and the max_allocated_storage will allow storage auto-scaling."
  type        = number
}

variable "auto_minor_version_upgrade" {
  description = "Indicates that minor engine upgrades will be applied automatically to the DB instance during the maintenance window."
  type        = bool
}

variable "backup_retention_period" {
  description = "The days to retain backups for."
  type        = number
}

variable "backup_window" {
  description = "The daily time range during which automated backups are created if automated backups are enabled."
  type        = string
}

variable "db_name" {
  description = "The name of the database to create when the DB instance is created."
  type        = string
}

variable "db_subnet_group_name" {
  description = "A DB subnet group to associate with this DB instance."
  type        = string
}

variable "enabled_cloudwatch_logs_exports" {
  description = "List of log types to export to cloudwatch."
  type        = list(string)
}

variable "engine" {
  description = "The database engine to use."
  type        = string
}

variable "engine_version" {
  description = "The version number of the database engine to use."
  type        = string
}

variable "maintenance_window" {
  description = "The weekly time range (in UTC) during which system maintenance can occur."
  type        = string
}

variable "max_allocated_storage" {
  description = "The upper limit to which Amazon RDS can automatically scale the storage of the DB instance."
  type        = number
}

variable "multi_az" {
  description = "Specifies if the RDS instance is multi-AZ."
  type        = bool
}

variable "username" {
  description = "Username for the master DB user."
  type        = string
}

variable "password" {
  description = "Password for the master DB user."
  type        = string
  sensitive   = true
}

variable "publicly_accessible" {
  description = "Bool to control if instance is publicly accessible."
  type        = bool
}

variable "storage_encrypted" {
  description = "Specifies whether the DB instance is encrypted."
  type        = bool
}

variable "storage_type" {
  description = "Specifies the storage type to be associated with the DB instance."
  type        = string
}

variable "skip_final_snapshot" {
  description = "Specifies whether the DB instance is encrypted."
  type        = bool
}

variable "final_snapshot_identifier" {
  description = "Specifies the final snapshot identifier associated with the DB instance."
  type        = string
}


variable "tags" {
  description = "A map of tags to assign to the resource."
  type        = map(string)
   default     = {}
}
