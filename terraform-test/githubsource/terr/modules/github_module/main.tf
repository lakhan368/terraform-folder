module "child_module_example" {
  source                = "github.com/lakhan368/Terraform/modules/root_module"
  ec2_image             = var.ec2_image
  ec2_instance_type     = var.ec2_instance_type
  ec2_vpc_id            = var.ec2_vpc_id 
  ec2_region            = var.ec2_region 
}
