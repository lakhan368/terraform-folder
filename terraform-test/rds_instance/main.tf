#aws ssm put-parameter --name "/rds/db_name" --value "mydatabase" --type "String"
#aws ssm put-parameter --name "/rds/db_password" --value "password" --type "SecureString"


provider "aws" {
  region = "us-east-1"  # Change to your desired region
}

# Fetch SSM parameters
#data "aws_ssm_parameter" "db_name" {
#  name = "/rds/db_name"
#}

#data "aws_ssm_parameter" "db_password" {
#  name = "/rds/db_password"
#}

# Security group for the RDS instance
resource "aws_security_group" "rds_sg" {
  name        = "rds_security_group"
  description = "Allow MySQL inbound traffic"
  vpc_id      = "vpc-023ff8995cd9c627c"  # Replace with your VPC ID

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Adjust for your security needs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}




resource "aws_db_instance" "default" {
  allocated_storage    = 10
  db_name              = "mydb"
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  username             = "lakhan"
  password             = "lakhan361"
  publicly_accessible = true
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

}