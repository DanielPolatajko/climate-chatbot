terraform {
  backend "s3" {
    bucket  = "climate-chatbot-terraform-backend"
    key     = "terraform.tfstate"
    region  = "eu-west-2"
    profile = "terraform"
  }
}
