variable "aws_region" {
  type = string
}

variable "environment" {
  type = string
}

variable "application" {
  type = string
}

variable "deployed_by" {
  type = string
}

variable "bucket_name" {
    type = string
}

variable "log_bucket_name" {
    type = string
}

variable "default_tags" {
  description = ""
  type        = map
  default     = {}
}