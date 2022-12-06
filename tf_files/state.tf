terraform {
  required_version = "=1.0.9"
  backend "s3" {
    bucket         = "gearbox-mc-terraform-state"
    key            = "state/terraform.state"
    region         = "us-east-2"
    encrypt        = true
    dynamodb_table = "tf-gearbox-mc-state-table"
  }
}

# Provision S3 bucket
resource "aws_s3_bucket" "terraform-gearbox-mc-state" {
  bucket = "gearbox-mc-terraform-state"
  tags = "${var.default_tags}"
}

resource "aws_s3_bucket_acl" "terraform_gearbox-mc-state-acl" {
    bucket = aws_s3_bucket.terraform-gearbox-mc-state.id
    acl = "private"
}



resource "aws_s3_bucket_server_side_encryption_configuration" "state_bucket_encryption" {
    bucket = aws_s3_bucket.terraform-gearbox-mc-state.bucket
    rule {
        apply_server_side_encryption_by_default {
            sse_algorithm = "AES256"
        }
    }
}

resource "aws_s3_bucket_versioning" "mc_state_versioning" {
    bucket = aws_s3_bucket.terraform-gearbox-mc-state.id
    versioning_configuration {
      status = "Enabled"
    }
}

resource "aws_s3_bucket_public_access_block" "block" {
  bucket = aws_s3_bucket.terraform-gearbox-mc-state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# dynamodb lock table to prevent concurrent writes 
resource "aws_dynamodb_table" "tf-gearbox-mc-state-table" {
  name           = "tf-gearbox-mc-state-table"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
  tags = "${var.default_tags}"
}
