
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.58.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "dataproject_rg" {
  name     = "rg-backend-${var.application_name}-${var.environment_name}"
  location = var.primary_location
}

resource "azurerm_storage_account" "dataproject_st" {
  name                     = "stbackend${var.application_name}${var.environment_name}"
  resource_group_name      = azurerm_resource_group.dataproject_rg.name
  location                 = azurerm_resource_group.dataproject_rg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}

resource "azurerm_storage_container" "tfstate_ci" {
  name                  = "ci-backend-tfstate"
  storage_account_id    = azurerm_storage_account.dataproject_st.id
  container_access_type = "private"
}