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
#
#resource "aws_vpc" "main" {
#  cidr_block = "10.0.0.0/16"
#  tags = {
#    Name = "main"
#  }
#}
#
#resource "aws_subnet" "main" {
#  vpc_id     = aws_vpc.main.id
#  cidr_block = "10.0.1.0/24"
#  tags = {
#    Name = "main"
#  }
#}
#
#resource "aws_internet_gateway" "main" {
#  vpc_id = aws_vpc.main.id
#  tags = {
#    Name = "main"
#  }
#}
#
#resource "aws_route_table" "main" {
#  vpc_id = aws_vpc.main.id
#  route {
#    cidr_block = "0.0.0.0/0"
#    gateway_id = aws_internet_gateway.main.id
#  }
#  tags = {
#    Name = "main"
#  }
#}
#
#resource "aws_route_table_association" "a" {
#  subnet_id      = aws_subnet.main.id
#  route_table_id = aws_route_table.main.id
#}
#
resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"
  #  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "ecr_role" {
  name = "ecr_role"

  assume_role_policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Principal": {
            "Service": "ec2.amazonaws.com"
          },
          "Effect": "Allow",
          "Sid": ""
        }
      ]
    }
  EOF
}

resource "aws_iam_policy" "ecr_policy" {
  name        = "ecr_policy"
  path        = "/"
  description = "Policy to allow EC2 instances to pull images from ECR"

  policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "ecr:GetAuthorizationToken",
            "ecr:BatchCheckLayerAvailability",
            "ecr:GetDownloadUrlForLayer",
            "ecr:GetRepositoryPolicy",
            "ecr:DescribeRepositories",
            "ecr:ListImages",
            "ecr:DescribeImages",
            "ecr:BatchGetImage",
            "ecr:InitiateLayerUpload",
            "ecr:UploadLayerPart",
            "ecr:CompleteLayerUpload",
            "ecr:PutImage"
          ],
          "Resource": "*"
        }
      ]
    }
  EOF
}

resource "aws_iam_role_policy_attachment" "ecr_policy_attachment" {
  role       = aws_iam_role.ecr_role.name
  policy_arn = aws_iam_policy.ecr_policy.arn
}

resource "aws_iam_instance_profile" "ecr_profile" {
  name = "ecr_profile"
  role = aws_iam_role.ecr_role.name
}

resource "aws_instance" "app_server" {
  ami           = "ami-0443d29a4bc22b3a5"
  instance_type = "t2.micro"
  iam_instance_profile = aws_iam_instance_profile.ecr_profile.name
  #  subnet_id = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.allow_ssh.id]

  user_data = <<-EOF
    #! /bin/sh
    yum update -y
    amazon-linux-extras install docker
    service docker start
    usermod -a -G docker ec2-user
    chkconfig docker on
    aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${aws_ecr_repository.climate_chatbot.repository_url}
    docker run ${aws_ecr_repository.climate_chatbot.repository_url}:latest
  EOF

  tags = {
    Name = "AppServerInstance"
  }
}

