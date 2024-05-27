resource "aws_instance" "app_server" {
  ami           = var.ami_id
  instance_type = var.instance

  tags = {
    Name = "AppServer"
  }
}

create and use ec2 module and pass the variable in the module based on the environment variable from the dynamic blocks
