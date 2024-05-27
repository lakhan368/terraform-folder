output "instance_ip" {
  value = module.ec2_instance.public_ip
}

output "instance_tags" {
  value = module.ec2_instance.ec2_tags
}