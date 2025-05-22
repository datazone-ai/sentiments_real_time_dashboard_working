# Azure Streamlit App Deployment Script
# This script assumes you have Azure CLI and Docker installed.
# Replace <your-app-name> and <your-resource-group> as needed.

# 1. Azure App Service (Linux) Deployment Script

# Log in to Azure
az login

# Create a resource group (if needed)
az group create --name <your-resource-group> --location westeurope

# Create an App Service plan
az appservice plan create --name myPlan --resource-group <your-resource-group> --sku B1 --is-linux

# Create a Web App
az webapp create --resource-group <your-resource-group> --plan myPlan --name <your-app-name> --runtime "PYTHON|3.9"

# Deploy your code (from the project root)
az webapp deploy --resource-group <your-resource-group> --name <your-app-name> --src-path .

# Set Startup Command in Azure Portal or CLI
az webapp config set --resource-group <your-resource-group> --name <your-app-name> --startup-file "streamlit run app.py --server.port=8000 --server.address=0.0.0.0"

# Set environment variables (App Settings)
az webapp config appsettings set --resource-group <your-resource-group> --name <your-app-name> --settings BLOB_CONNECTION_STRING="<your-connection-string>"

# 2. Dockerfile for Azure Container Apps or Azure Web App for Containers

# Create a file named Dockerfile in your project root:

# --- Dockerfile ---
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]
# --- end Dockerfile ---

# Build and run locally (optional):
docker build -t my-streamlit-app .
docker run -p 8000:8000 -e BLOB_CONNECTION_STRING="<your-connection-string>" my-streamlit-app

# Push to Azure Container Registry (ACR) and deploy to Azure Container Apps or Web App for Containers as needed.
# See Azure documentation for details: https://learn.microsoft.com/en-us/azure/container-apps/get-started?tabs=bash
