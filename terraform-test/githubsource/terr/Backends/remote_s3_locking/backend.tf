terraform {
  backend "s3" {
    bucket         = "dgruploads-terraform-state-file"
    key            = "terraform_state_file/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform_state_lock"
  }
}
