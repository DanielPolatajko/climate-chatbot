output "repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.climate_chatbot_repo.repository_url
}
