# AI News Generator - Deployment Guide

## Overview
This guide explains how to deploy the AI News Generator to Google Cloud using always-free instances.

---

## Google Cloud Always-Free Tier (Paid Account)

Even with a paid Google Cloud account, you get **always-free** resources that never expire:

### Compute Engine (Always Free)
- **1 e2-micro VM instance** (0.25-2 vCPU, 1GB RAM)
- **30 GB standard persistent disk storage**
- **1 GB outbound data transfer/month**
- **Available in**: us-central1, us-east1, us-west1
- **Cost**: $0/month (if within limits)

### Cloud Run (Always Free)
- **2 million requests/month**
- **180,000 vCPU-seconds/month**
- **360,000 GB-seconds/month**
- **Cost**: $0/month (if within limits)

### App Engine (Always Free)
- **28 instance hours/day**
- **1 GB outbound data transfer/day**
- **Cost**: $0/month (if within limits)

### Cloud Storage (Always Free)
- **5 GB storage**
- **1 GB outbound data transfer/month**
- **Cost**: $0/month (if within limits)

---

## Recommended: Compute Engine e2-micro (Always Free)

### Why e2-micro?
- ✅ Always free (never expires)
- ✅ Full control over environment
- ✅ Suitable for always-on applications
- ✅ No cold starts
- ✅ Persistent storage included

### Prerequisites
1. Google Cloud paid account (always-free tier available)
2. Google Cloud SDK installed
3. SSH key pair

### Step 1: Create Compute Engine Instance

```bash
# Set variables
export PROJECT_ID="your-project-id"
export INSTANCE_NAME="news-agent"
export REGION="us-central1"
export ZONE="us-central1-a"

# Set project
gcloud config set project $PROJECT_ID

# Create e2-micro instance
gcloud compute instances create $INSTANCE_NAME \
  --zone=$ZONE \
  --machine-type=e2-micro \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=30GB \
  --scopes=default
```

### Step 2: SSH into Instance

```bash
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
sudo apt-get install -y python3.10 python3-pip git

# Install Node.js (optional, for frontend)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 (process manager)
sudo npm install -g pm2
```

### Step 4: Clone and Setup Project

```bash
# Clone repository
git clone https://github.com/yourusername/news_agent.git
cd news_agent

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
echo "GOOGLE_API_KEY=your-api-key" > .env
```

### Step 5: Run Application

```bash
# Using PM2 for process management
pm2 start "uvicorn app:app --host 0.0.0.0 --port 8000" --name news-agent
pm2 startup
pm2 save

# Check status
pm2 status
```

### Step 6: Configure Firewall

```bash
# Allow HTTP traffic
gcloud compute firewall-rules create allow-http \
  --allow=tcp:80 \
  --source-ranges=0.0.0.0/0

# Allow HTTPS traffic
gcloud compute firewall-rules create allow-https \
  --allow=tcp:443 \
  --source-ranges=0.0.0.0/0

# Allow custom port (8000)
gcloud compute firewall-rules create allow-8000 \
  --allow=tcp:8000 \
  --source-ranges=0.0.0.0/0
```

### Step 7: Setup Nginx Reverse Proxy (Optional)

```bash
# Install Nginx
sudo apt-get install -y nginx

# Create config
sudo nano /etc/nginx/sites-available/default
```

Add this configuration:
```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable and restart Nginx
sudo systemctl enable nginx
sudo systemctl restart nginx
```

---

## Alternative: Cloud Run (Serverless)

### Advantages
- ✅ Auto-scaling
- ✅ No server management
- ✅ Pay-per-use

### Deploy

```bash
gcloud run deploy news-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY
```

---

## Cost Comparison (Always Free)

| Service | Always Free | Monthly Cost |
|---------|-------------|--------------|
| **Compute Engine e2-micro** | 730 hours | $0 |
| **Cloud Run** | 2M requests | $0 |
| **App Engine** | 28 hours/day | $0 |
| **Cloud Storage** | 5 GB | $0 |

---

## Monitoring

### View Logs
```bash
# SSH into instance
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE

# View PM2 logs
pm2 logs news-agent

# View system logs
sudo journalctl -u nginx -f
```

### Monitor Usage
```bash
# Check instance status
gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE

# Check billing
gcloud billing accounts list
```

---

## Custom Domain Setup

### Using Cloud DNS
```bash
# Create DNS zone
gcloud dns managed-zones create news-agent \
  --dns-name=yourdomain.com \
  --description="News Agent DNS"

# Get nameservers
gcloud dns managed-zones describe news-agent --format="value(nameServers)"

# Update domain registrar with these nameservers
```

### Using Let's Encrypt (Free SSL)
```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d yourdomain.com

# Auto-renew
sudo systemctl enable certbot.timer
```

---

## Security Best Practices

1. **Firewall Rules**: Only allow necessary ports
2. **SSH Keys**: Use key-based authentication
3. **API Keys**: Store in Secret Manager
4. **CORS**: Restrict to your domain
5. **HTTPS**: Always use SSL/TLS

---

## Troubleshooting

### Application won't start
```bash
# Check PM2 logs
pm2 logs news-agent --lines 100

# Check system resources
free -h
df -h
```

### High latency
- Check network bandwidth
- Monitor CPU/memory usage
- Optimize API calls

### Out of always-free quota
- Upgrade to paid tier
- Optimize resource usage
- Monitor billing alerts

---

## Next Steps

1. ✅ Create Compute Engine e2-micro instance
2. ✅ Deploy application
3. ✅ Configure Nginx reverse proxy
4. ✅ Setup custom domain
5. ✅ Enable HTTPS
6. ✅ Monitor performance

---

## Useful Links

- [Google Cloud Always Free](https://cloud.google.com/free/docs/free-cloud-features)
- [Compute Engine Pricing](https://cloud.google.com/compute/pricing)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Cloud SDK Documentation](https://cloud.google.com/sdk/docs)

