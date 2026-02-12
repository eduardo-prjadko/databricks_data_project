TF_VAR_application_name := dataproject
TF_VAR_environment_name := dev
TF_VAR_primary_location := westus2

# Define variables for the Terraform backend configuration
TF_BACKEND_LOCATION := westus2
TF_BACKEND_RG := rg-backend-$(TF_VAR_application_name)-$(TF_VAR_environment_name)
TF_BACKEND_SA := stbackend$(TF_VAR_application_name)$(TF_VAR_environment_name)
TF_BACKEND_CN := ci-backend-tfstate
TF_BACKEND_KEY := $(TF_VAR_application_name)-$(TF_VAR_environment_name).tfstate

TF_DIR := ./app/infrastructure/main
TF_BOOTSTRAP_DIR := ./app/infrastructure/bootstrap_backend

bootstrap-backend:
	@echo Bootstraping backend...
	@terraform -chdir=$(TF_BOOTSTRAP_DIR) init
	@export TF_VAR_application_name=$(TF_VAR_application_name) && \
		export TF_VAR_environment_name=$(TF_VAR_environment_name) && \
		export TF_VAR_primary_location=$(TF_VAR_primary_location) && \
		terraform -chdir=$(TF_BOOTSTRAP_DIR) apply -auto-approve
	
	@make init
	@make apply

	@rm -rf $(TF_BOOTSTRAP_DIR)/.terraform
	@rm -f $(TF_BOOTSTRAP_DIR)/terraform.tfstate
	@rm -f $(TF_BOOTSTRAP_DIR)/terraform.tfstate.backup

# Initialize Terraform
init:
	terraform -chdir=$(TF_DIR) init \
		-input=false \
		-backend-config="resource_group_name=$(TF_BACKEND_RG)" \
		-backend-config="storage_account_name=$(TF_BACKEND_SA)" \
		-backend-config="container_name=$(TF_BACKEND_CN)" \
		-backend-config="key=$(TF_BACKEND_KEY)"

# Run a Terraform plan
plan:
	@export TF_VAR_application_name=$(TF_VAR_application_name) && \
		export TF_VAR_environment_name=$(TF_VAR_environment_name) && \
		terraform -chdir=$(TF_DIR) plan -var-file="terraform.tfvars"

# Apply the plan
apply:
	@export TF_VAR_application_name=$(TF_VAR_application_name) && \
		export TF_VAR_environment_name=$(TF_VAR_environment_name) && \
		terraform -chdir=$(TF_DIR) apply -auto-approve

# Clean up unnecessary files
clean:
	rm -rf .terraform