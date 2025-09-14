terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
  }
}

# define the region
provider "aws" {
    region = "us-east-1"
}

# create sg for inbound traffic for ELK stack
resource "aws_security_group" "elk_sg" {
  name_prefix = "elk-security-group"
  description = "allow inbond traffic for ELK and SSH"
}