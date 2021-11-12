# -CentralizedModelRepository_Azure

![Centralized Model Registry Architecture](https://docs.microsoft.com/en-us/azure/databricks/_static/images/mlflow/multiworkspace.png "Centralized Model Registry Architecture")

[Azure Article](https://docs.microsoft.com/en-us/azure/databricks/applications/machine-learning/manage-model-lifecycle/multiple-workspaces)

This repository contains some notebooks to facilitate the setup of a Centralized Model Repository.

The Central Setup notebook:
- Creates the Service Principals
- Adds the Service Principals to the Central Workspace
- Gives the Service Principals Token creation ACLS.
- Creates PAT Tokens for the Service Principals

The Satellite Setup notebook:
- Creates the Secret Scopes on the Satellite Workspace
- Adds the Secret to the Secret Scope
  - PAT Token
  - Central Workspace url
  - Central Workspace ID
