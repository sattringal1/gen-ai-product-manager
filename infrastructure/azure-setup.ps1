# =================================================================
# azure-setup.ps1
# One-time provisioning of all Azure resources for Gen-AI PM.
# Run this ONCE before pushing to GitHub (CI/CD handles deployments).
#
# Prerequisites:
#   - Azure CLI installed  (winget install Microsoft.AzureCLI)
#   - Logged in           (az login)
#   - Subscription set    (az account set --subscription "YOUR-SUB")
# =================================================================

$ErrorActionPreference = "Stop"

# ── Configurable variables ───────────────────────────────────────
$SUBSCRIPTION_ID  = ""                        # ← fill in (az account list)
$RESOURCE_GROUP   = "rg-genai-pm"
$LOCATION         = "eastus"
$ACR_NAME         = "genaipmacr"              # must be globally unique, lowercase
$ENV_NAME         = "genai-pm-env"
$BACKEND_APP      = "genai-pm-backend"
$FRONTEND_APP     = "genai-pm-frontend"
$GITHUB_REPO      = "sattringal1/gen-ai-product-manager"

# ── Secrets (fill before running) ───────────────────────────────
$OPENAI_API_KEY        = ""   # ← your OpenAI key
$APP_SECRET_KEY        = [System.Web.Security.Membership]::GeneratePassword(32,4)
$JIRA_API_TOKEN        = ""   # ← optional
$CONFLUENCE_API_TOKEN  = ""   # ← optional

# ────────────────────────────────────────────────────────────────
if (-not $SUBSCRIPTION_ID) { throw "Set SUBSCRIPTION_ID before running." }
if (-not $OPENAI_API_KEY)  { throw "Set OPENAI_API_KEY before running." }

function Banner($msg) {
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "  $msg" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
}

Banner "1/8  Setting subscription"
az account set --subscription $SUBSCRIPTION_ID
Write-Host "     OK" -ForegroundColor Green

Banner "2/8  Creating resource group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION --output table
Write-Host "     OK" -ForegroundColor Green

Banner "3/8  Creating Azure Container Registry: $ACR_NAME"
az acr create `
  --name $ACR_NAME `
  --resource-group $RESOURCE_GROUP `
  --sku Basic `
  --admin-enabled true `
  --output table
Write-Host "     OK" -ForegroundColor Green

$ACR_SERVER   = "$ACR_NAME.azurecr.io"
$ACR_USERNAME = (az acr credential show --name $ACR_NAME --query username -o tsv)
$ACR_PASSWORD = (az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

Banner "4/8  Creating Container Apps Environment: $ENV_NAME"
az containerapp env create `
  --name $ENV_NAME `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --output table
Write-Host "     OK" -ForegroundColor Green

Banner "5/8  Creating backend Container App (internal ingress)"
az containerapp create `
  --name $BACKEND_APP `
  --resource-group $RESOURCE_GROUP `
  --environment $ENV_NAME `
  --image "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest" `
  --registry-server $ACR_SERVER `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --ingress internal `
  --target-port 8000 `
  --min-replicas 0 `
  --max-replicas 5 `
  --cpu 0.5 `
  --memory 1Gi `
  --secrets "openai-key=$OPENAI_API_KEY" `
            "app-secret-key=$APP_SECRET_KEY" `
            "jira-api-token=$JIRA_API_TOKEN" `
            "confluence-api-token=$CONFLUENCE_API_TOKEN" `
  --env-vars `
    "LLM_PROVIDER=openai" `
    "OPENAI_MODEL=gpt-4o" `
    "APP_ENV=production" `
    "LOG_LEVEL=INFO" `
    "OPENAI_API_KEY=secretref:openai-key" `
    "SECRET_KEY=secretref:app-secret-key" `
    "JIRA_API_TOKEN=secretref:jira-api-token" `
    "CONFLUENCE_API_TOKEN=secretref:confluence-api-token" `
  --output table
Write-Host "     OK" -ForegroundColor Green

Banner "6/8  Creating frontend Container App (external ingress)"
az containerapp create `
  --name $FRONTEND_APP `
  --resource-group $RESOURCE_GROUP `
  --environment $ENV_NAME `
  --image "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest" `
  --registry-server $ACR_SERVER `
  --registry-username $ACR_USERNAME `
  --registry-password $ACR_PASSWORD `
  --ingress external `
  --target-port 80 `
  --min-replicas 0 `
  --max-replicas 3 `
  --cpu 0.25 `
  --memory 0.5Gi `
  --env-vars `
    "BACKEND_HOST=$BACKEND_APP" `
    "BACKEND_PORT=80" `
  --output table
Write-Host "     OK" -ForegroundColor Green

Banner "7/8  Creating GitHub Actions service principal"
$SP_JSON = az ad sp create-for-rbac `
  --name "sp-genai-pm-github" `
  --role contributor `
  --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP" `
  --sdk-auth

Write-Host ""
Write-Host "  ┌─────────────────────────────────────────────────────────┐" -ForegroundColor Yellow
Write-Host "  │  Copy this JSON into GitHub → Settings → Secrets        │" -ForegroundColor Yellow
Write-Host "  │  Secret name: AZURE_CREDENTIALS                         │" -ForegroundColor Yellow
Write-Host "  └─────────────────────────────────────────────────────────┘" -ForegroundColor Yellow
Write-Host $SP_JSON -ForegroundColor White

Banner "8/8  Summary — add these as GitHub Secrets"
$FRONTEND_URL = (az containerapp show `
  --name $FRONTEND_APP `
  --resource-group $RESOURCE_GROUP `
  --query "properties.configuration.ingress.fqdn" -o tsv)

Write-Host ""
Write-Host "  GitHub repo: https://github.com/$GITHUB_REPO/settings/secrets/actions" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Add these secrets:" -ForegroundColor Yellow
Write-Host "  ┌──────────────────────────┬────────────────────────────────────────┐"
Write-Host "  │ AZURE_CREDENTIALS        │ (JSON printed above)                   │"
Write-Host "  │ ACR_LOGIN_SERVER         │ $ACR_SERVER"
Write-Host "  │ ACR_USERNAME             │ $ACR_USERNAME"
Write-Host "  │ ACR_PASSWORD             │ $ACR_PASSWORD"
Write-Host "  │ OPENAI_API_KEY           │ (your key — already stored as secret)  │"
Write-Host "  └──────────────────────────┴────────────────────────────────────────┘"
Write-Host ""
Write-Host "  ✅ Your live app will be at:" -ForegroundColor Green
Write-Host "     https://$FRONTEND_URL" -ForegroundColor Green
Write-Host ""
Write-Host "  After adding secrets, push to main to trigger the first deployment." -ForegroundColor Cyan
Write-Host ""
