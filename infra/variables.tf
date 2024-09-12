variable "vm_name" {
  type        = string
  description = "(Required) The name of the VM."
  nullable    = false
}

variable "vm_size" {
  type        = string
  description = "(Required) The size of the Linux VM."
  nullable    = false
}

variable "vm_admin_user" {
  type        = string
  description = "(Required) The admin user of the VM."
  nullable    = false
}

variable "location" {
  type        = string
  description = "(Required) The location of the database to provision the resources at."
  nullable    = false
}

variable "os_disk" {
  type = object({
    storage_account_type = string
    caching              = string
  })
  description = "Lorem Ipsum"
  nullable    = false
}

variable "source_image_id" {
  type        = string
  default     = null
  description = "(Optional) The ID of the image which this Linux Virtual Machine should be created from. Changing this forces a new resource to be created."
}
