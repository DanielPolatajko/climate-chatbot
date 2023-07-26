variable "region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "eu-west-2"
}

variable "profile" {
  description = "The AWS profile to use"
  type        = string
  default     = "terraform"
}

variable "github_repo_url" {
  description = "The GitHub URL where the app code exists"
  type        = string
  sensitive   = true
}
