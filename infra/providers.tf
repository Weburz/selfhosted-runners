terraform {
  required_version = ">=1.9.5"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "9aa29059-667f-40e4-995b-5922fa7a048f"
}
