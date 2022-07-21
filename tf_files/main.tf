# define AWS provider and region
provider "aws" {
  region = "${var.aws_region}"
  default_tags {
      tags = {
         Environment = "${var.environment}" 
         Application = "${var.application}" 
         DeployedBy = "${var.deployed_by}" 
      }
  }
}

module "s3-bucket" {
  source = "./modules/s3-bucket"
  bucket_name = "${var.bucket_name}"
}