# 🚀 Deployment Guide - AI Policy Trends Dashboard

This guide covers how to deploy the AI Policy Trends Dashboard to various platforms.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Streamlit Cloud](#streamlit-cloud)
4. [AWS Deployment](#aws-deployment)
5. [Azure Deployment](#azure-deployment)
6. [Production Setup](#production-setup)
7. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Local Development

### Quick Start (Windows)

```bash
# Run the setup script
setup.bat

# Or manually:
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate.bat

# 2. Install dependencies
pip install -r requirements.txt

# 3. Preprocess data
python preprocess_data.py

# 4. Run dashboard
streamlit run app.py
```

### Quick Start (Linux/macOS)

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# Or manually:
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Preprocess data
python preprocess_data.py

# 4. Run dashboard
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

---

## Docker Deployment

### Prerequisites

- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose (optional, for multi-container setups)

### Build and Run

```bash
# Build the Docker image
docker build -t ai-policy-dashboard .

# Run the container
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  ai-policy-dashboard

# On Windows (PowerShell):
docker run -p 8501:8501 `
  -v ${PWD}/data:/app/data `
  -v ${PWD}/models:/app/models `
  ai-policy-dashboard
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f dashboard

# Stop services
docker-compose down

# Rebuild image
docker-compose up -d --build
```

### Docker Configuration

Edit `docker-compose.yml` to customize:
- Port mapping (default: 8501)
- Volume mounts for data persistence
- Environment variables
- Resource limits

---

## Streamlit Cloud

Streamlit Cloud is the easiest way to deploy Streamlit apps.

### Prerequisites

1. GitHub account with your repository
2. Streamlit Cloud account (free tier available)

### Deployment Steps

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "Create app"
   - Select your GitHub repo, branch, and `app.py` as the main file

3. **Configure Secrets** (if needed)
   - In the app settings, add secrets if you have sensitive data
   - These will be available in `streamlit.secrets` in your app

4. **Deploy**
   - Click "Deploy" and wait for the build to complete
   - Your app will be live at `https://your-username-projectname.streamlit.app`

### Streamlit Cloud Configuration

Create `.streamlit/secrets.toml` for sensitive data:

```toml
# .streamlit/secrets.toml
database_url = "your-database-url"
api_key = "your-api-key"
```

**Note**: Never commit `secrets.toml` to GitHub. Use Streamlit Cloud's secrets management instead.

---

## AWS Deployment

### Option 1: EC2 Instance

```bash
# 1. Launch EC2 Instance (Ubuntu 22.04)
# - t3.medium or larger recommended
# - Allow inbound traffic on port 8501 and 22

# 2. SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# 3. Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv git

# 4. Clone repository
git clone your-repo-url
cd dashboard_project

# 5. Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python preprocess_data.py

# 6. Run with process manager (using supervisor)
sudo apt-get install -y supervisor

# 7. Create supervisor config
sudo nano /etc/supervisor/conf.d/streamlit.conf
```

**Supervisor Configuration** (`/etc/supervisor/conf.d/streamlit.conf`):

```ini
[program:streamlit]
directory=/home/ubuntu/dashboard_project
command=/home/ubuntu/dashboard_project/venv/bin/streamlit run app.py --server.port 8501
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/streamlit.log
user=ubuntu
```

```bash
# Enable and start service
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start streamlit
```

### Option 2: Elastic Beanstalk

```bash
# 1. Install EB CLI
pip install awsebcli

# 2. Initialize EB app
eb init -p python-3.11 ai-policy-dashboard --region us-east-1

# 3. Create .ebextensions/python.config
mkdir -p .ebextensions
```

Create `.ebextensions/python.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /var/app/current:$PYTHONPATH
  aws:autoscaling:launchconfiguration:
    InstanceType: t3.medium
```

```bash
# 4. Create environment and deploy
eb create production
eb deploy

# 5. View logs
eb logs
```

### Option 3: ECS with Fargate

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name ai-policy-dashboard

# 2. Build and push image
docker build -t ai-policy-dashboard .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com
docker tag ai-policy-dashboard:latest your-account-id.dkr.ecr.us-east-1.amazonaws.com/ai-policy-dashboard:latest
docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/ai-policy-dashboard:latest

# 3. Create ECS cluster and service (use AWS Console or CLI)
# 4. Configure task definition with ECR image
# 5. Scale as needed
```

---

## Azure Deployment

### Azure Container Instances

```bash
# 1. Login to Azure
az login

# 2. Create resource group
az group create --name dashboard-rg --location eastus

# 3. Create container registry
az acr create --resource-group dashboard-rg --name dashboardregistry --sku Basic

# 4. Build and push image
az acr build --registry dashboardregistry --image ai-policy-dashboard:v1 .

# 5. Deploy container
az container create \
  --resource-group dashboard-rg \
  --name ai-policy-dashboard \
  --image dashboardregistry.azurecr.io/ai-policy-dashboard:v1 \
  --registry-login-server dashboardregistry.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --ports 8501 \
  --memory 2
```

### Azure App Service

```bash
# 1. Create App Service plan
az appservice plan create \
  --name dashboardplan \
  --resource-group dashboard-rg \
  --sku B2 \
  --is-linux

# 2. Create web app
az webapp create \
  --resource-group dashboard-rg \
  --plan dashboardplan \
  --name ai-policy-dashboard \
  --deployment-container-image-name dashboardregistry.azurecr.io/ai-policy-dashboard:v1

# 3. Configure settings
az webapp config appsettings set \
  --resource-group dashboard-rg \
  --name ai-policy-dashboard \
  --settings WEBSITES_PORT=8501
```

---

## Production Setup

### 1. Web Server (Nginx/Apache)

**Nginx Configuration** (`/etc/nginx/sites-available/dashboard`):

```nginx
upstream streamlit {
    server localhost:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    client_max_body_size 100M;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 2. SSL Certificate (Let's Encrypt)

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

### 3. System Service (systemd)

Create `/etc/systemd/system/streamlit-dashboard.service`:

```ini
[Unit]
Description=Streamlit AI Policy Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/dashboard_project
Environment="PATH=/home/ubuntu/dashboard_project/venv/bin"
ExecStart=/home/ubuntu/dashboard_project/venv/bin/streamlit run app.py \
    --server.port 8501 \
    --server.address localhost
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit-dashboard
sudo systemctl start streamlit-dashboard
sudo systemctl status streamlit-dashboard
```

### 4. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp     # SSH
sudo ufw allow 80/tcp     # HTTP
sudo ufw allow 443/tcp    # HTTPS
sudo ufw enable
```

---

## Monitoring & Maintenance

### Logging

```bash
# View Streamlit logs
sudo journalctl -u streamlit-dashboard -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Backup Strategy

```bash
# Backup data directory
sudo tar -czf /backups/dashboard_data_$(date +%Y%m%d).tar.gz /path/to/data/

# Automated backup with cron
0 2 * * * /home/ubuntu/backup.sh
```

### Updates and Dependencies

```bash
# Update Python packages
pip install --upgrade -r requirements.txt

# Check for outdated packages
pip list --outdated

# Update NLTK data (if changed)
python -m nltk.downloader vader_lexicon punkt stopwords
```

### Performance Monitoring

Monitor with tools like:
- **Prometheus** for metrics
- **Grafana** for dashboards
- **CloudWatch** (AWS) or **Azure Monitor** (Azure)
- **New Relic** for APM

### Health Checks

```bash
# Simple health check
curl -s http://localhost:8501/_stcore/health

# Include in monitoring tools
# AWS: CloudWatch Alarms
# Azure: Application Insights
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find and kill process using port 8501
# Linux/Mac:
sudo lsof -ti:8501 | xargs kill -9

# Windows (PowerShell):
Get-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess | Stop-Process
```

### Memory Issues

```bash
# Increase VM memory or adjust Streamlit config
# In .streamlit/config.toml:
# [client]
# maxMessageSize = 200

# Reduce data sample size in app.py
texts = df['full_text'].fillna('').values[:5000]
```

### Database Connection

```python
# Use connection pooling
import psycopg2.pool

connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20, "dbname=policy user=admin password=secret"
)
```

---

## Scaling Recommendations

| Component | Scaling Strategy |
|-----------|-----------------|
| Web Server | Load balancer (ALB, Azure LB) |
| Streamlit App | Horizontal scaling with multiple instances |
| Database | Read replicas, connection pooling |
| Cache | Redis or Memcached |
| Storage | S3 (AWS), Blob Storage (Azure), GCS (Google) |
| CDN | CloudFront, Azure CDN, CloudFlare |

---

## Security Checklist

- [ ] Enable SSL/TLS (HTTPS)
- [ ] Configure firewall rules
- [ ] Use environment variables for secrets
- [ ] Implement authentication if needed
- [ ] Enable logging and monitoring
- [ ] Regular security updates
- [ ] Backup strategy in place
- [ ] Rate limiting configured
- [ ] SQL injection prevention (if applicable)
- [ ] CORS properly configured

---

For questions or issues, refer to the main [README.md](README.md) or contact the development team.
