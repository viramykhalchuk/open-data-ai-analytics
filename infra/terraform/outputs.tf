output "public_ip_address" {
  description = "Public IP address of the VM"
  value       = azurerm_public_ip.public_ip.ip_address
}

output "web_url" {
  description = "Web interface URL"
  value       = "http://${azurerm_public_ip.public_ip.ip_address}:${var.web_port}"
}

output "ssh_command" {
  description = "SSH command for VM connection"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.public_ip.ip_address}"
}
