provider "aws" {
  region  = var.region
  profile = var.profile
}

data "aws_ami" "latest_ecs_optimized" {
  most_recent = true
  filter {
    name   = "name"
    values = ["amzn-ami-*-amazon-ecs-optimized"]
  }
  owners = ["amazon"]
}

resource "aws_ecs_cluster" "climate_chatbot_cluster" {
  name = "climate_chatbot_cluster"
}

resource "aws_ecs_task_definition" "climate_chatbot" {
  family                   = "climate_chatbot"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name  = "climate-chatbot"
      image = "${aws_ecr_repository.climate_chatbot_repo.repository_url}:latest"
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "climate_chatbot_service" {
  name            = "climate_chatbot_service"
  cluster         = aws_ecs_cluster.climate_chatbot_cluster.id
  task_definition = aws_ecs_task_definition.climate_chatbot.arn
  desired_count   = 0
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = ["subnet-08c3ca76ab7bf0681"]
    assign_public_ip = true
  }
}

resource "aws_ecr_repository" "climate_chatbot_repo" {
  name = "climate-chatbot-repo"
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs_task_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_security_group" "allow_all" {
  name        = "allow_all"
  description = "Allow all inbound traffic"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
