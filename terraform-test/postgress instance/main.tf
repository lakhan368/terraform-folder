provider "aws" {
  region = "us-east-1"# Change to your desired AWS region
}

# Security Group for RDS
resource "aws_security_group" "rds_sg_pg" {
  name        = "rds_security_group_pg"
  description = "Allow database access"
  vpc_id      = "vpc-0e405e66067bbd97a" 
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Change to your specific IP range
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "RDS Security Group"
  }
}

# Create the PostgreSQL RDS instance
resource "aws_db_instance" "postgres" {
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "15"  # Use a specific version if needed
  instance_class         = "db.t3.micro"
  #name                   = "mydatabase"
  db_name                = "mydb"
  username               = "lakhan"
  password               = "lakhan361"  # Use a secure method to handle sensitive data
  parameter_group_name   = "default.postgres15"
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.rds_sg_pg.id]

  # Additional optional settings
  publicly_accessible    = true
  storage_type           = "gp2"
  backup_retention_period = 7
  multi_az               = false
  tags = {
    Name = "MyPostgresDB"
  }
}
