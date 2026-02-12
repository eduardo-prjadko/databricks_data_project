# resource "azurerm_service_plan" "data_gen_asp" {
#   name                = "asp-${var.application_name}-${var.environment_name}"
#   resource_group_name = azurerm_resource_group.data_project_rg.name
#   location            = azurerm_resource_group.data_project_rg.location
#   os_type             = "Linux"
#   sku_name            = "F1"
# }

# resource "azurerm_linux_function_app" "data_gen_func" {
#   name                = "func-${var.application_name}-${var.environment_name}"
#   resource_group_name = azurerm_resource_group.data_project_rg.name
#   location            = azurerm_resource_group.data_project_rg.location

#   storage_account_name       = azurerm_storage_account.data_project_st.name
#   storage_account_access_key = azurerm_storage_account.data_project_st.primary_access_key
#   service_plan_id            = azurerm_service_plan.data_gen_asp.id

#   site_config {}
# }