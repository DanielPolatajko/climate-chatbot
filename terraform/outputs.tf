output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.climate_chatbot.repository_url
}
