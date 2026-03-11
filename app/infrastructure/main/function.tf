resource "azurerm_storage_account" "dataproject_function_st" {
  name                     = "st${var.application_name}${var.environment_name}datagen"
  resource_group_name      = azurerm_resource_group.dataproject_rg.name
  location                 = azurerm_resource_group.dataproject_rg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
}

resource "azurerm_service_plan" "data_gen_asp" {
  name                = "asp-${var.application_name}-${var.environment_name}"
  resource_group_name = azurerm_resource_group.dataproject_rg.name
  location            = azurerm_resource_group.dataproject_rg.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_function_app" "data_gen_func" {
  name                = "func-${var.application_name}-${var.environment_name}-datagen"
  resource_group_name = azurerm_resource_group.dataproject_rg.name
  location            = azurerm_resource_group.dataproject_rg.location

  storage_account_name       = azurerm_storage_account.dataproject_function_st.name
  storage_account_access_key = azurerm_storage_account.dataproject_function_st.primary_access_key
  service_plan_id            = azurerm_service_plan.data_gen_asp.id

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE": 1
  }

  site_config {
    application_stack {
      python_version = "3.12"
    }
  }

  enabled = true
  
  identity {
    type = "SystemAssigned"
  }
}