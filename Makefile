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

DATAGEN_STG_DIR := ./app/src/data_gen/stg
DATAGEN_SRC_DIR := ./app/src/data_gen/src
DATAGEN_DIST_DIR := ./app/src/data_gen/dist
DATAGEN_RG_NAME := rg-$(TF_VAR_application_name)-$(TF_VAR_environment_name)
DATAGEN_APP_NAME := func-$(TF_VAR_application_name)-$(TF_VAR_environment_name)-datagen


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

build-datagen:
	@mkdir -p $(DATAGEN_STG_DIR)
	@mkdir -p $(DATAGEN_DIST_DIR)
	@rsync -a \
		--exclude "__pycache__/" \
		--exclude ".venv/" \
		--exclude ".vscode/" \
		--exclude "tests/" \
		--exclude ".gitignore" \
		--exclude "local.settings.json" \
		--exclude "requirements-dev.txt" \
		--exclude "pytest.toml" \
		$(DATAGEN_SRC_DIR) $(DATAGEN_STG_DIR)
	@cd $(DATAGEN_STG_DIR)/src && python -m pip install -r ./requirements.txt --target .
	@cd $(DATAGEN_STG_DIR)/src && zip -r ../../dist/build.zip .

deploy-datagen: build-datagen
	@az functionapp deployment source config-zip \
		-g "$(DATAGEN_RG_NAME)" \
		-n "$(DATAGEN_APP_NAME)" \
		--src "$(DATAGEN_DIST_DIR)/build.zip"
