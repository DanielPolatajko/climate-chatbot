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
  ami           = "ami-0443d29a4bc22b3a5"
  instance_type = "t2.micro"

#  TODO - need to get access to logs to see if this is working. After that, get default streamlit app working
  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y software-properties-common curl git
    add-apt-repository ppa:deadsnakes/ppa
    apt-get update -y
    apt-get install -y python3.10 python3.10-dev python3.10-distutils python3.10-venv
    curl -sSL https://install.python-poetry.org | python3.10 -
    git clone ${var.github_repo_url} app
    cd app
    poetry env use python3.10
    poetry install
    poetry run python climate_chatbot/app.py
  EOF

  tags = {
    Name = "AppServerInstance"
  }
}

