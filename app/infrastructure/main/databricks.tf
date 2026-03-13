
resource "azurerm_databricks_workspace" "dataproject_dbw" {
  name                = "dbw-${var.application_name}-${var.environment_name}"
  resource_group_name = azurerm_resource_group.dataproject_rg.name
  location            = azurerm_resource_group.dataproject_rg.location
  sku                 = "standard"
}