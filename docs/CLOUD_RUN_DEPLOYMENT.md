# Cloud Run Deployment Guide

## Overview
This guide covers deploying NeuroNews to Google Cloud Run with automatic CI/CD via Cloud Build.

---

## Prerequisites

1. **Google Cloud Project** with billing enabled
2. **gcloud CLI** installed and configured
3. **Docker** installed locally (for testing)
4. **Git** repository pushed to GitHub/Cloud Source Repositories

---

## Step 1: Set Up Google Cloud Project

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com \
  secretmanager.googleapis.com
```

---

## Step 2: Store API Key as Secret

```bash
# Create secret for Google API key
echo -n "your-google-api-key" | gcloud secrets create google-api-key --data-file=-

# Grant Cloud Run service account access
gcloud secrets add-iam-policy-binding google-api-key \
  --member=serviceAccount:PROJECT_ID@appspot.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor
```

---

## Step 3: Deploy Using Cloud Build (Recommended)

### Option A: Deploy from GitHub

1. **Connect GitHub Repository**:
   ```bash
   gcloud builds connect --repository-name=news_agent --repository-owner=YOUR_GITHUB_USERNAME
   ```

2. **Create Cloud Build Trigger**:
   - Go to Cloud Console → Cloud Build → Triggers
   - Click "Create Trigger"
   - Select GitHub repository
   - Set branch: `main`
   - Build configuration: `cloudbuild.yaml`
   - Add substitution variable:
     - `_GOOGLE_API_KEY`: Your Google API key

3. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Cloud Run deployment files"
   git push origin main
   ```
   Cloud Build will automatically trigger and deploy!

### Option B: Manual Deployment

```bash
# Build and push image
gcloud builds submit --config=cloudbuild.yaml

# Or deploy directly
gcloud run deploy neuronews \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your-api-key \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600
```

---

## Step 4: Verify Deployment

```bash
# Get service URL
gcloud run services describe neuronews --region us-central1 --format='value(status.url)'

# Test the endpoint
curl https://neuronews-xxxxx.run.app/

# View logs
gcloud run services logs read neuronews --region us-central1 --limit 50
```

---

## Step 5: Configure Custom Domain (Optional)

```bash
# Map custom domain
gcloud run domain-mappings create \
  --service=neuronews \
  --domain=your-domain.com \
  --region=us-central1

# Update DNS records with provided CNAME
# (Check Cloud Console for exact CNAME value)
```

---

## Environment Variables

Set these in Cloud Run:

| Variable | Value |
|----------|-------|
| `GOOGLE_API_KEY` | Your Google Generative AI API key |
| `PORT` | 8080 (default) |
| `PYTHONUNBUFFERED` | 1 |

---

## Monitoring & Logs

```bash
# View real-time logs
gcloud run services logs read neuronews --region us-central1 --follow

# View metrics
gcloud monitoring dashboards list

# Set up alerts
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="NeuroNews Error Rate"
```

---

## Cost Optimization

### Always-Free Tier (No Cost)
- **2 million requests/month**
- **180,000 vCPU-seconds/month**
- **360,000 GB-seconds/month**

### Pricing (if exceeded)
- **$0.00002400 per vCPU-second**
- **$0.00000250 per GB-second**
- **$0.40 per 1M requests**

### Tips to Stay Free
1. Set `--memory 256Mi` (uses less memory)
2. Set `--cpu 1` (uses less CPU)
3. Use `--min-instances 0` (scales to zero when idle)
4. Monitor usage: `gcloud run services describe neuronews --region us-central1`

---

## Troubleshooting

### Service won't start
```bash
# Check logs
gcloud run services logs read neuronews --region us-central1 --limit 100

# Common issues:
# - Missing GOOGLE_API_KEY environment variable
# - Port not set to 8080
# - Memory/CPU limits too low
```

### High latency
```bash
# Increase CPU allocation
gcloud run services update neuronews \
  --cpu 2 \
  --region us-central1

# Increase minimum instances
gcloud run services update neuronews \
  --min-instances 1 \
  --region us-central1
```

### Authentication errors
```bash
# Verify API key is set
gcloud run services describe neuronews --region us-central1 --format='value(spec.template.spec.containers[0].env[*].value)'

# Update API key
gcloud run services update neuronews \
  --update-env-vars GOOGLE_API_KEY=new-key \
  --region us-central1
```

---

## Rollback

```bash
# View revision history
gcloud run revisions list --service=neuronews --region us-central1

# Rollback to previous revision
gcloud run services update-traffic neuronews \
  --to-revisions REVISION_NAME=100 \
  --region us-central1
```

---

## CI/CD Pipeline

The `cloudbuild.yaml` automatically:
1. Builds Docker image
2. Pushes to Container Registry
3. Deploys to Cloud Run
4. Sets environment variables

**Trigger on**: Push to `main` branch

---

## Files Included

- `Dockerfile` - Container image definition
- `.dockerignore` - Files to exclude from Docker build
- `cloudbuild.yaml` - Cloud Build CI/CD configuration
- `service.yaml` - Knative service configuration
- `requirements.txt` - Python dependencies

---

## Next Steps

1. ✅ Commit all files to git
2. ✅ Connect GitHub to Cloud Build
3. ✅ Create Cloud Build trigger
4. ✅ Push to main branch
5. ✅ Monitor deployment in Cloud Console
6. ✅ Test the live endpoint

---

## Support

For issues:
- Check Cloud Run logs: `gcloud run services logs read neuronews`
- View Cloud Build logs: `gcloud builds log --stream`
- Google Cloud documentation: https://cloud.google.com/run/docs
