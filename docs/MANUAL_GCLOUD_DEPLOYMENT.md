# Manual gcloud Deployment Guide

Simple step-by-step guide to deploy NeuroNews to Google Cloud Run using gcloud CLI.

---

## Prerequisites

1. **Google Cloud Account** (with billing enabled)
2. **gcloud CLI** installed: https://cloud.google.com/sdk/docs/install
3. **Docker** installed (optional, for local testing)
4. **Google Generative AI API Key**: https://aistudio.google.com/app/apikey

---

## Step 1: Set Up gcloud

```bash
# Initialize gcloud
gcloud init

# Set your project
gcloud config set project thomas2025

# Verify setup
gcloud config list
```

---

## Step 2: Enable Required APIs

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Verify
gcloud services list --enabled
```

---

## Step 3: Build Docker Image Locally (Optional)

```bash
# Build image locally
docker build -t neuronews:latest .

# Test locally
docker run -p 8000:8080 \
  -e GOOGLE_API_KEY=your-api-key \
  neuronews:latest

# Visit http://localhost:8000
```

---

## Step 4: Deploy to Cloud Run (Simplest Method)

```bash
# Deploy directly from source code
gcloud run deploy neuronews \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your-google-api-key \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600
```

**What this does:**
- Builds Docker image from current directory
- Pushes to Container Registry
- Deploys to Cloud Run
- Sets environment variables
- Allocates 512MB memory and 1 CPU
- Allows public access (no authentication)

---

## Step 5: Get Service URL

```bash
# View deployed service
gcloud run services describe neuronews --region us-central1

# Get just the URL
gcloud run services describe neuronews \
  --region us-central1 \
  --format='value(status.url)'
```

Your app is now live! 🎉

---

## Step 6: Test the Deployment

```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe neuronews \
  --region us-central1 \
  --format='value(status.url)')

# Test the landing page
curl $SERVICE_URL

# Test API endpoint
curl -X POST $SERVICE_URL/generate_news \
  -H "Content-Type: application/json" \
  -d '{"topic": "Technology", "country": "India"}'
```

---

## Common Commands

### View Logs
```bash
# Real-time logs
gcloud run services logs read neuronews --region us-central1 --follow

# Last 50 lines
gcloud run services logs read neuronews --region us-central1 --limit 50
```

### Update Environment Variables
```bash
gcloud run services update neuronews \
  --update-env-vars GOOGLE_API_KEY=new-api-key \
  --region us-central1
```

### Update Resource Allocation
```bash
# Increase memory
gcloud run services update neuronews \
  --memory 1Gi \
  --region us-central1

# Increase CPU
gcloud run services update neuronews \
  --cpu 2 \
  --region us-central1
```

### Scale Configuration
```bash
# Set minimum instances (keeps service warm)
gcloud run services update neuronews \
  --min-instances 1 \
  --region us-central1

# Set maximum instances
gcloud run services update neuronews \
  --max-instances 100 \
  --region us-central1
```

### Delete Service
```bash
gcloud run services delete neuronews --region us-central1
```

---

## Troubleshooting

### Deployment fails
```bash
# Check build logs
gcloud builds log --stream

# Common issues:
# - Missing requirements.txt
# - Dockerfile syntax error
# - Port not set to 8080
```

### Service won't start
```bash
# View logs
gcloud run services logs read neuronews --region us-central1 --limit 100

# Common issues:
# - Missing GOOGLE_API_KEY environment variable
# - Application error in app.py
# - Port binding issue
```

### High latency
```bash
# Increase CPU
gcloud run services update neuronews --cpu 2 --region us-central1

# Set minimum instances to 1 (keeps service warm)
gcloud run services update neuronews --min-instances 1 --region us-central1
```

### Check service status
```bash
gcloud run services describe neuronews --region us-central1
```

---

## Cost Optimization

### Always-Free Tier
- **2 million requests/month** ✅ Free
- **180,000 vCPU-seconds/month** ✅ Free
- **360,000 GB-seconds/month** ✅ Free

### Stay within free tier
```bash
# Use minimum resources
gcloud run services update neuronews \
  --memory 256Mi \
  --cpu 1 \
  --min-instances 0 \
  --region us-central1
```

### Monitor usage
```bash
# View metrics
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/request_count"'
```

---

## Custom Domain (Optional)

```bash
# Map custom domain
gcloud run domain-mappings create \
  --service=neuronews \
  --domain=your-domain.com \
  --region=us-central1

# Update DNS records with provided CNAME
# (Check Cloud Console for exact CNAME)
```

---

## Rollback to Previous Version

```bash
# View revision history
gcloud run revisions list --service=neuronews --region us-central1

# Rollback to previous revision
gcloud run services update-traffic neuronews \
  --to-revisions REVISION_NAME=100 \
  --region us-central1
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Deploy | `gcloud run deploy neuronews --source . --platform managed --region us-central1 --allow-unauthenticated --set-env-vars GOOGLE_API_KEY=key` |
| View logs | `gcloud run services logs read neuronews --region us-central1 --follow` |
| Get URL | `gcloud run services describe neuronews --region us-central1 --format='value(status.url)'` |
| Update env vars | `gcloud run services update neuronews --update-env-vars KEY=value --region us-central1` |
| Delete | `gcloud run services delete neuronews --region us-central1` |

---

## Next Steps

1. ✅ Install gcloud CLI
2. ✅ Run `gcloud init`
3. ✅ Deploy with single command
4. ✅ Test the endpoint
5. ✅ Monitor logs
6. ✅ Optimize as needed

---

## Support

- Cloud Run Docs: https://cloud.google.com/run/docs
- gcloud CLI Reference: https://cloud.google.com/sdk/gcloud/reference
- Pricing: https://cloud.google.com/run/pricing
