terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = var.region
  profile = var.profile
}

resource "aws_instance" "app_server" {
  ami           = "ami-020737107b4baaa50"
  instance_type = "t2.micro"

  tags = {
    Name = "AppServerInstance"
  }
}
