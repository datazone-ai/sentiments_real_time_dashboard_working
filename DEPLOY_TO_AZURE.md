# Azure Streamlit Deployment Instructions

### 1. requirements.txt (already present)
* Make sure your requirements.txt includes all dependencies, e.g.:
* streamlit
* azure-storage-blob


### 2. startup.txt (for Azure App Service Linux)
* This file tells Azure how to start your Streamlit app.
* streamlit run app.py --server.port=8000 --server.address=0.0.0.0

### 3. .streamlit/secrets.toml (already present)
* Do NOT commit secrets.toml to public repos. Use Azure App Settings for production secrets.

### 4. Deploy using Azure CLI
* Replace <your-app-name> and <your-resource-group> as needed as you follow the code below.
```
# Log in to Azure
az login

# Create a resource group (if needed). I.e if you don't have on before or if you have skip to __create an App Service plan below__
az group create --name <your-resource-group> --location westeurope

# Create an App Service plan
az appservice plan create --name myPlan --resource-group <your-resource-group> --sku B1 --is-linux

# Create a Web App
az webapp create --resource-group <your-resource-group> --plan myPlan --name <your-app-name> --runtime "PYTHON|3.9"

# Deploy your code (from the project root)
az webapp deploy --resource-group <your-resource-group> --name <your-app-name> --src-path .
```
### 5. Configure App Settings in Azure Portal
* Go to your Web App > Settings > Configuration > Application settings
* Add your BLOB_CONNECTION_STRING as an application setting.

### 6. Set Startup Command in Azure Portal
* Go to your Web App > Settings > Configuration > General settings
* Set Startup Command to:
* streamlit run app.py --server.port=8000 --server.address=0.0.0.0

### 7. Browse to your app
* https://<your-app-name>.azurewebsites.net

### For production, use Azure Key Vault or App Settings for secrets, not secrets.toml.
