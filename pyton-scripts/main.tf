provider "aws" {
  region = "us-east-1"
}

variable "env" {
  description = "Environment for which resources will be created"
  type        = string
  default     = "nonprod"
}


locals {
  environment_configurations = {
    "nonprod" = {
      identifier              = "mcapostgresdb"
      vpc_id                  = "vpc-04286d7e37de69708"
      db_instance_class       = "db.t3.small"
      allocated_storage       = 20
      max_allocated_storage   = 100
      db_name                 = "postgressdb"
      db_subnet_group_name    = "default"
      username                = "test"
      password                = "test1234"
      multi_az                = false
      storage_type            = "gp2"
      backup_retention_period = 7
      maintenance_window      = "thu:13:25-thu:13:55"
      backup_window           = "12:45-13:15"
      storage_encrypted       = true
      rds_tags = {
        Environment = "SIT"
        Name        = "mcamysqldb"
      }
      engine                          = "postgres"
      engine_version                  = "16.2"
      auto_minor_version_upgrade      = true
      enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
      publicly_accessible             = true
      skip_final_snapshot             = true
      final_snapshot_identifier       = "mcapostgressdb"

      security_group_name        = "RDSPostgresSecurityGroup"
      security_group_description = "Security group for nonprod environment"
      security_group_ingress = [
        {
          from_port   = 5432
          to_port     = 5432
          protocol    = "tcp"
          cidr_blocks = ["0.0.0.0/0"]
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
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
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
  source                          = "../final-postgress"
  identifier                      = local.config.identifier
  instance_class                  = local.config.db_instance_class
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









# Define a security group for the RDS instance
resource "aws_security_group" "rds_sg" {
  name        = "rds_sg"
  description = "Security group for RDS instance"
  vpc_id      = "vpc-04286d7e37de69708" # Replace with your VPC ID

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Replace with your IP range for better security
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create the MySQL RDS instance
resource "aws_db_instance" "mysql" {
  identifier           = "my-mysql-db"
  allocated_storage    = 20
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  db_name              = "mydatabase"
  username             = "admin"
  password             = "yourpassword"
  parameter_group_name = "default.mysql8.0"
  publicly_accessible  = true
  skip_final_snapshot  = true

  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  # Backup and maintenance settings
  backup_retention_period = 7
  backup_window           = "02:00-03:00"
  maintenance_window      = "sun:05:00-sun:06:00"

  # CloudWatch Logs
  enabled_cloudwatch_logs_exports = ["error", "general", "slowquery"]

  # Storage settings
  storage_type          = "gp2"
  max_allocated_storage = 100
  multi_az              = false
  storage_encrypted     = true

  tags = {
    Name = "My MySQL Database"
  }
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






