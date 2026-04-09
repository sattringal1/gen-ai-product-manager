# Deployment Guide — Gen-AI Product Manager

## Prerequisites

| Tool | Minimum Version | Purpose |
|------|----------------|---------|
| Python | 3.12 | Backend runtime |
| Node.js | 20 | Frontend build |
| Docker | 27 | Container build & run |
| kubectl | 1.29 | Kubernetes management |
| OpenAI API Key | — | LLM access |

---

## Option 1 — Local Development (Fastest)

### 1.1 Backend

```bash
cd c:\AKS\MIT\NEWPRODUCT-AKS\backend

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy ..\\.env.example ..\\.env
# Edit .env — set OPENAI_API_KEY at minimum

# Start development server
python main.py
# → API running at http://localhost:8000
# → Swagger UI at http://localhost:8000/docs
```

### 1.2 Frontend

```bash
cd c:\AKS\MIT\NEWPRODUCT-AKS\frontend

npm install
npm run dev
# → UI running at http://localhost:5173
```

---

## Option 2 — Docker Compose (Recommended for Teams)

```bash
cd c:\AKS\MIT\NEWPRODUCT-AKS

# 1. Copy and fill environment file
copy .env.example .env
# Edit .env: set OPENAI_API_KEY (required)

# 2. Build and start all services
docker-compose up --build -d

# 3. Verify services are healthy
docker-compose ps
docker-compose logs -f backend

# Services available:
#   Frontend:  http://localhost:3000
#   Backend:   http://localhost:8000
#   API Docs:  http://localhost:8000/docs

# 4. Stop
docker-compose down
```

### Rebuilding after code changes

```bash
docker-compose up --build -d --no-deps backend
docker-compose up --build -d --no-deps frontend
```

---

## Option 3 — Kubernetes / AKS (Production)

### 3.1 Build and Push Docker Images

```bash
# Set your registry
REGISTRY=your-acr.azurecr.io   # Azure Container Registry
TAG=v1.0.0

# Build images
docker build -t $REGISTRY/genai-pm-backend:$TAG ./backend
docker build -t $REGISTRY/genai-pm-frontend:$TAG ./frontend

# Push to registry
az acr login --name your-acr
docker push $REGISTRY/genai-pm-backend:$TAG
docker push $REGISTRY/genai-pm-frontend:$TAG
```

### 3.2 Update Image References

Edit [k8s/backend-deployment.yaml](k8s/backend-deployment.yaml) and [k8s/frontend-deployment.yaml](k8s/frontend-deployment.yaml):
```yaml
image: your-acr.azurecr.io/genai-pm-backend:v1.0.0
```

### 3.3 Configure Values

Edit [k8s/configmap.yaml](k8s/configmap.yaml):
- Set `JIRA_BASE_URL`, `JIRA_EMAIL`, `CONFLUENCE_BASE_URL`, etc.
- Set `CORS_ORIGINS` to your domain

Edit [k8s/ingress.yaml](k8s/ingress.yaml):
- Replace `genai-pm.your-domain.com` with your actual domain

### 3.4 Create Secrets

```bash
# NEVER commit secrets to git — create them via kubectl
kubectl create secret generic genai-pm-secrets \
  --from-literal=OPENAI_API_KEY=sk-... \
  --from-literal=JIRA_API_TOKEN=your-jira-token \
  --from-literal=CONFLUENCE_API_TOKEN=your-confluence-token \
  --from-literal=SECRET_KEY=$(openssl rand -hex 32) \
  -n genai-pm
```

### 3.5 Deploy to Kubernetes

```bash
# Connect to your AKS cluster
az aks get-credentials --resource-group your-rg --name your-aks-cluster

# Apply all manifests in order
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f k8s/ingress.yaml

# Watch rollout
kubectl rollout status deployment/genai-pm-backend -n genai-pm
kubectl rollout status deployment/genai-pm-frontend -n genai-pm

# Check pod status
kubectl get pods -n genai-pm
```

### 3.6 Verify Deployment

```bash
# Check all pods are Running
kubectl get pods -n genai-pm

# Tail backend logs
kubectl logs -f deployment/genai-pm-backend -n genai-pm

# Test health endpoint
kubectl port-forward svc/backend 8000:8000 -n genai-pm
curl http://localhost:8000/health
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_PROVIDER` | Yes | `openai` | `openai` or `azure_openai` |
| `OPENAI_API_KEY` | If provider=openai | — | OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o` | Model name |
| `AZURE_OPENAI_API_KEY` | If provider=azure_openai | — | Azure key |
| `AZURE_OPENAI_ENDPOINT` | If provider=azure_openai | — | Azure endpoint URL |
| `AZURE_OPENAI_DEPLOYMENT` | No | `gpt-4o` | Azure deployment name |
| `JIRA_BASE_URL` | For Jira push | — | `https://org.atlassian.net` |
| `JIRA_EMAIL` | For Jira push | — | Service account email |
| `JIRA_API_TOKEN` | For Jira push | — | Jira API token |
| `JIRA_PROJECT_KEY` | No | `PM` | Default Jira project key |
| `CONFLUENCE_BASE_URL` | For Confluence push | — | `https://org.atlassian.net/wiki` |
| `CONFLUENCE_EMAIL` | For Confluence push | — | Service account email |
| `CONFLUENCE_API_TOKEN` | For Confluence push | — | Confluence API token |
| `CONFLUENCE_SPACE_KEY` | No | `PROD` | Default space key |
| `APP_PORT` | No | `8000` | Backend port |
| `CORS_ORIGINS` | Yes in prod | `http://localhost:5173` | Comma-separated origins |
| `SECRET_KEY` | Yes in prod | dev key | JWT signing key |
| `LOG_LEVEL` | No | `INFO` | `DEBUG`, `INFO`, `WARNING` |

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `422 Unprocessable Entity` | Validation error | Check request body matches schema |
| `500 Internal Server Error` | LLM API failure | Check OPENAI_API_KEY in .env |
| Frontend shows "Backend unreachable" | Backend not running | Start backend first |
| Jira push returns empty keys | Missing Jira credentials | Set JIRA_* vars in .env |
| Pod stuck in CrashLoopBackOff | Secret missing | Check `kubectl describe pod` |
| CORS error in browser | Origin not allowed | Add frontend URL to CORS_ORIGINS |
