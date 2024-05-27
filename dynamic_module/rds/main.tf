module "ec2_instances" {
  source = "/home/ubuntu/Documents/terraform-folder/dynamic_module/module"

  instance_configs = [
    {
      name            = "instance1"
      ami             = "ami-12345678"
      instance_type   = "t2.micro"

      additional_tags = {
        Project = "MyProject"
        Owner   = "John Doe"
      }
    }
  ]

  environment = "prod"
}
