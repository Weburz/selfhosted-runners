// Assign a resource group for all the resource provisioned below
resource "azurerm_resource_group" "default" {
  name     = title("${var.vm_name}RG")
  location = var.location
}

// Setup a VNet to assign the VM to
resource "azurerm_virtual_network" "default" {
  resource_group_name = azurerm_resource_group.default.name
  name                = title("${var.vm_name}VNet")
  location            = azurerm_resource_group.default.location
  address_space       = ["10.0.0.0/16"]
}

// Provision a subnet for the VM's Network Interface
resource "azurerm_subnet" "default" {
  resource_group_name  = azurerm_resource_group.default.name
  name                 = title("${var.vm_name}Subnet")
  address_prefixes     = ["10.0.1.0/24"]
  virtual_network_name = azurerm_virtual_network.default.name
}

// Provision a Public IP address to access the VM remotely
resource "azurerm_public_ip" "default" {
  resource_group_name = azurerm_resource_group.default.name
  name                = title("${var.vm_name}PublicIP")
  location            = azurerm_resource_group.default.location
  allocation_method   = "Dynamic"
  sku                 = "Basic"

  lifecycle {
    // This is necessary (see the docs for more information on it)
    // https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/public_ip
    create_before_destroy = true
  }
}

// Provision a Network Interface for the VM to be accessed through
resource "azurerm_network_interface" "default" {
  resource_group_name = azurerm_resource_group.default.name
  location            = azurerm_resource_group.default.location
  name                = title("${var.vm_name}NIC")

  ip_configuration {
    name                          = title("${var.vm_name}IPConfig")
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.default.id
    public_ip_address_id          = azurerm_public_ip.default.id
  }
}

// Provision the VM to setup the GitHub Actions runners on
resource "azurerm_linux_virtual_machine" "default" {
  resource_group_name   = azurerm_resource_group.default.name
  name                  = title("${var.vm_name}VM")
  location              = azurerm_resource_group.default.location
  size                  = var.vm_size
  admin_username        = var.vm_admin_user
  network_interface_ids = [azurerm_network_interface.default.id]
  source_image_id       = var.source_image_id

  os_disk {
    storage_account_type = var.os_disk.storage_account_type
    caching              = var.os_disk.caching
    name                 = title("${var.vm_name}OSDisk")
  }

  source_image_reference {
    publisher = "Debian"
    offer     = "debian-11"
    sku       = "11-backports-gen2"
    version   = "latest"
  }

  admin_ssh_key {
    username   = "jarmos"
    public_key = file("~/.ssh/id_rsa.pub")
  }
}
