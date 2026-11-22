# GitHub Setup for Cloud Run Deployment

## Files to Add to GitHub

All these files are now ready in your repository:

### Essential Files
- ✅ `Dockerfile` - Container image definition
- ✅ `.dockerignore` - Docker build exclusions
- ✅ `cloudbuild.yaml` - Cloud Build CI/CD pipeline
- ✅ `service.yaml` - Knative service configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `CLOUD_RUN_DEPLOYMENT.md` - Detailed deployment guide
- ✅ `.gitignore` - Git exclusions

### Application Files
- ✅ `app.py` - FastAPI application
- ✅ `main.py` - Agent orchestration
- ✅ `index.html` - Landing page
- ✅ `token_tracker.py` - Token usage tracking
- ✅ `assets/logo.png` - NeuroNews logo
- ✅ `news_generation/` - Agent definitions
- ✅ `.env.example` - Environment variables template

---

## Step 1: Create .env.example

```bash
# Create template for environment variables
cat > .env.example << 'EOF'
# Google Generative AI API Key
GOOGLE_API_KEY=your-api-key-here

# Optional: Server configuration
PORT=8000
HOST=127.0.0.1
EOF
```

---

## Step 2: Commit to Git

```bash
# Stage all files
git add .

# Commit with descriptive message
git commit -m "feat: Add Cloud Run deployment configuration

- Add Dockerfile for containerization
- Add cloudbuild.yaml for CI/CD pipeline
- Add service.yaml for Knative configuration
- Add comprehensive deployment documentation
- Add .dockerignore for optimized builds
- Update requirements.txt with all dependencies"

# Push to GitHub
git push origin main
```

---

## Step 3: GitHub Repository Setup

### Add GitHub Secrets (for Cloud Build)

1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Add these secrets:
   - `GCP_PROJECT_ID`: Your Google Cloud project ID
   - `GCP_SA_KEY`: Service account JSON key (base64 encoded)

### Create GitHub Actions Workflow (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v1
      with:
        project_id: ${{ secrets.GCP_PROJECT_ID }}
        service_account_key: ${{ secrets.GCP_SA_KEY }}
    
    - name: Configure Docker
      run: gcloud auth configure-docker
    
    - name: Build and Push
      run: |
        docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/neuronews:latest .
        docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/neuronews:latest
    
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy neuronews \
          --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/neuronews:latest \
          --platform managed \
          --region us-central1 \
          --allow-unauthenticated \
          --set-env-vars GOOGLE_API_KEY=${{ secrets.GOOGLE_API_KEY }}
```

---

## Step 4: Add README.md

Your main README should include:
- Project description
- Features
- Tech stack
- Local setup
- Deployment instructions
- API endpoints
- Contributing guidelines

---

## Files NOT to Commit

These are already in `.gitignore`:
- `.env` (use `.env.example` instead)
- `__pycache__/`
- `*.pyc`
- `.venv/` or `venv/`
- `.idea/`, `.vscode/`
- `*.log`
- `uv.lock` (optional, depends on your preference)

---

## Deployment Flow

```
GitHub Push (main branch)
    ↓
Cloud Build Trigger Activated
    ↓
Build Docker Image
    ↓
Push to Container Registry
    ↓
Deploy to Cloud Run
    ↓
Service Live at: https://neuronews-xxxxx.run.app
```

---

## Quick Start for Cloud Run

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/news_agent.git
cd news_agent

# 2. Set up Cloud Build trigger
gcloud builds connect --repository-name=news_agent --repository-owner=YOUR_USERNAME

# 3. Create trigger in Cloud Console
# - Source: GitHub
# - Branch: main
# - Build config: cloudbuild.yaml
# - Add substitution: _GOOGLE_API_KEY=your-api-key

# 4. Push to trigger deployment
git push origin main

# 5. Monitor deployment
gcloud builds log --stream

# 6. Get service URL
gcloud run services describe neuronews --region us-central1 --format='value(status.url)'
```

---

## Environment Variables for Cloud Run

Set in Cloud Console or via gcloud:

```bash
gcloud run services update neuronews \
  --update-env-vars GOOGLE_API_KEY=your-api-key \
  --region us-central1
```

---

## Monitoring

```bash
# View logs
gcloud run services logs read neuronews --region us-central1 --limit 50

# View metrics
gcloud run services describe neuronews --region us-central1

# Set up alerts
# Go to Cloud Console → Monitoring → Alerting
```

---

## Troubleshooting

### Build fails
```bash
# Check Cloud Build logs
gcloud builds log --stream

# Common issues:
# - Missing requirements.txt
# - Dockerfile syntax error
# - Missing .dockerignore
```

### Service won't start
```bash
# Check Cloud Run logs
gcloud run services logs read neuronews --region us-central1 --limit 100

# Common issues:
# - Missing GOOGLE_API_KEY
# - Port not 8080
# - Memory/CPU too low
```

### High costs
```bash
# Reduce resource allocation
gcloud run services update neuronews \
  --memory 256Mi \
  --cpu 1 \
  --region us-central1

# Set min instances to 0 (scales to zero when idle)
gcloud run services update neuronews \
  --min-instances 0 \
  --region us-central1
```

---

## Next Steps

1. ✅ All deployment files created
2. ⏳ Commit and push to GitHub
3. ⏳ Connect GitHub to Cloud Build
4. ⏳ Create Cloud Build trigger
5. ⏳ Deploy to Cloud Run
6. ⏳ Monitor and optimize

---

## Support

- Cloud Run Docs: https://cloud.google.com/run/docs
- Cloud Build Docs: https://cloud.google.com/build/docs
- GitHub Actions: https://docs.github.com/en/actions
