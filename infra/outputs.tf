// Print the IP address of the VM to STDOUT for remote access
output "public_ip_address" {
  value       = azurerm_public_ip.default.ip_address
  description = "The Public IP Address for remote access usage."
}

// Print the admin username of the VM to STDOUT for remote access
output "admin_username" {
  value       = azurerm_linux_virtual_machine.default.admin_username
  description = "The username to remotely access the VM with."
}
