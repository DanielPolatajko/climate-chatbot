resource "aws_ecr_repository" "climate_chatbot" {
  name                 = "climate_chatbot"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}