provider "aws" {
  region = "us-east-1"
}

variable "env" {
  description = "Environment for which resources will be created"
  type        = string
  default     = "prod"
}

variable "db_username_ssm_parameter" {
  description = "The SSM parameter name for the database username"
  type        = string
  default     = "/mca/postgressdb/username"
}

variable "db_password_ssm_parameter" {
  description = "The SSM parameter name for the database password"
  type        = string
  default     = "/mca/postgressdb/password"
}


data "aws_ssm_parameter" "db_username" {
  name = var.db_username_ssm_parameter
}

data "aws_ssm_parameter" "db_password" {
  name            = var.db_password_ssm_parameter
  with_decryption = true
}


locals {
  environment_configurations = {
    "nonprod" = {
      identifier              = "mcapostgresdb"
      vpc_id                  = "vpc-0ab1923d70753d8d4"
      db_instance_class       = "db.t3.small"
      kms_key_id              = "arn:aws:kms:us-east-1:426765591064:key/5e4ec07e-36d7-4d13-a690-c43a0cb8b8d4"
      allocated_storage       = 20
      max_allocated_storage   = 100
      db_name                 = "postgressdb"
      db_subnet_group_name    = "default-vpc-0ab1923d70753d8d4"
      username                = data.aws_ssm_parameter.db_username.value
      password                = data.aws_ssm_parameter.db_password.value
      multi_az                = false
      storage_type            = "gp2"
      backup_retention_period = 7
      maintenance_window      = "thu:13:25-thu:13:55"
      backup_window           = "12:45-13:15"
      storage_encrypted       = true
      rds_tags = {
        Environment   = "SIT"
        Name          = "mcamysqldb"
      }
      engine                          = "postgres"
      engine_version                  = "16.2"
      auto_minor_version_upgrade      = true
      enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
      publicly_accessible             = false
      skip_final_snapshot             = true
      final_snapshot_identifier       = "mcapostgressdb"

      security_group_name        = "RDSPostgresSecurityGroup"
      security_group_description = "Security group for nonprod environment"
      security_group_ingress = [
        {
          from_port   = 443
          to_port     = 443
          protocol    = "tcp"
          cidr_blocks = ["0.0.0.0/8"]
        },
        {
          from_port       = 80
          to_port         = 80
          protocol        = "tcp"
          security_groups = ["sg-046638587d71f8cac"]
        },
        {
          from_port   = 80
          to_port     = 80
          protocol    = "tcp"
          cidr_blocks = ["0.0.0.0/8"]
        }
      ]
    }
    "prod" = {
        identifier              = "mcpostgresdb"
        vpc_id                  = "vpc-jg7789998"
        db_instance_class       = "db.t3.small"
        kms_key_id              = "arn:aws:kms:us-east-1:426765591064:key/5e4ec07e-36d7-4d13-a690-c43a0cb8b8d4"
        allocated_storage       = 20
        max_allocated_storage   = 100
        db_name                 = "postgressdb"
        db_subnet_group_name    = "default-vpc-88"
        username                = data.aws_ssm_parameter.db_username.value
        password                = data.aws_ssm_parameter.db_password.value
        multi_az                = false
        storage_type            = "gp2"
        backup_retention_period = 7
        maintenance_window      = "thu:13:25-thu:13:55"
        backup_window           = "12:45-13:15"
        storage_encrypted       = true
        rds_tags = {
          Environment   = "SIT"
          Name          = "mcamysqldb"
        }
        engine                          = "postgres"
        engine_version                  = "16.2"
        auto_minor_version_upgrade      = true
        enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
        publicly_accessible             = false
        skip_final_snapshot             = true
        final_snapshot_identifier       = "mcapostgressdb"
        security_group_name        = "RDSPostgresSecurityGroup"
        security_group_description = "Security group for nonprod environment"
        security_group_ingress = [
          {
            from_port   = 443
            to_port     = 443
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/8"]
          },
          {
            from_port       = 80
            to_port         = 80
            protocol        = "tcp"
            security_groups = ["sg-046638587d71f8cac"]
          },
          {
            from_port   = 80
            to_port     = 80
            protocol    = "tcp"
            cidr_blocks = ["0.0.0.0/8"]
          }
        ]
    }
  }
  config = local.environment_configurations[var.env]
}

# Setting up security group
resource "aws_security_group" "instance_sg" {
  name        = local.config.security_group_name
  description = local.config.security_group_description
  vpc_id      = local.config.vpc_id
  tags = {
    Name = local.config.security_group_name
  }

  dynamic "ingress" {
    for_each = local.config.security_group_ingress
    content {
      from_port = ingress.value.from_port
      to_port   = ingress.value.to_port
      protocol  = ingress.value.protocol
      # Include cidr_blocks if specified
      cidr_blocks = lookup(ingress.value, "cidr_blocks", null)

      # Include security_groups if specified
      security_groups = lookup(ingress.value, "security_groups", null)
    }
  }
}

module "rds_postgresql" {
  source                          = "/home/lakhan/postgesrds/terraform-module/final-postgress"
  identifier                      = local.config.identifier
  instance_class                  = local.config.db_instance_class
  kms_key_id                      = local.config.kms_key_id
  vpc_security_group_ids          = [aws_security_group.instance_sg.id]
  allocated_storage               = local.config.allocated_storage
  auto_minor_version_upgrade      = local.config.auto_minor_version_upgrade
  backup_retention_period         = local.config.backup_retention_period
  backup_window                   = local.config.backup_window
  db_name                         = local.config.db_name
  db_subnet_group_name            = local.config.db_subnet_group_name
  enabled_cloudwatch_logs_exports = local.config.enabled_cloudwatch_logs_exports
  engine                          = local.config.engine
  engine_version                  = local.config.engine_version
  maintenance_window              = local.config.maintenance_window
  max_allocated_storage           = local.config.max_allocated_storage
  multi_az                        = local.config.multi_az
  username                        = local.config.username
  password                        = local.config.password
  publicly_accessible             = local.config.publicly_accessible
  storage_type                    = local.config.storage_type
  storage_encrypted               = local.config.storage_encrypted
  skip_final_snapshot             = local.config.skip_final_snapshot
  final_snapshot_identifier       = local.config.final_snapshot_identifier
  tags                            = local.config.rds_tags
}

output "db_instance_id" {
  value = module.rds_postgresql.db_instance_id
}

output "db_instance_endpoint" {
  value = module.rds_postgresql.db_instance_endpoint
}

output "db_instance_arn" {
  value = module.rds_postgresql.db_instance_arn
}

output "db_instance_address" {
  value = module.rds_postgresql.db_instance_address
}

output "db_instance_status" {
  value = module.rds_postgresql.db_instance_status
}