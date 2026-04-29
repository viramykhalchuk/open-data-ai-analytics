variable "resource_group_name" {
  description = "Azure Resource Group name"
  type        = string
  default     = "rg-open-data-ai-analytics-lab4"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "westeurope"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "open-data-ai"
}

variable "admin_username" {
  description = "Admin username for Linux VM"
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "repo_url" {
  description = "GitHub repository URL"
  type        = string
  default     = "https://github.com/viramykhalchuk/open-data-ai-analytics.git"
}

variable "project_dir" {
  description = "Directory where the app will be cloned on VM"
  type        = string
  default     = "/opt/open-data-ai-analytics"
}

variable "compose_file" {
  description = "Docker Compose file name"
  type        = string
  default     = "compose.yaml"
}

variable "monitoring_compose_file" {
  description = "Docker Compose monitoring file name"
  type        = string
  default     = "monitoring/docker-compose.monitoring.yml"
}

variable "web_port" {
  description = "Public web port"
  type        = number
  default     = 8000
}

variable "prometheus_port" {
  description = "Public Prometheus port"
  type        = number
  default     = 9090
}

variable "grafana_port" {
  description = "Public Grafana port"
  type        = number
  default     = 3000
}
