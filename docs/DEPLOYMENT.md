# Deployment Guide

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- OpenAI API Key

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/autoagenthire.git
cd autoagenthire
```

### 2. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Generate using: `openssl rand -hex 32`

### 3. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
# Run database setup script
python scripts/setup_db.py

# Or use Docker
docker-compose up -d postgres
python scripts/setup_db.py
```

### 5. Run the Application

**Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Frontend (Streamlit):**
```bash
streamlit run frontend/streamlit/app.py
```

**Access the application:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:8501

## Docker Deployment

### 1. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose -f docker/docker-compose.yml up --build

# Run in detached mode
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

### 2. Access Services

- Backend API: http://localhost:8000
- Streamlit Frontend: http://localhost:8501
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- ChromaDB: http://localhost:8001

## Production Deployment

### AWS Deployment

#### 1. Setup EC2 Instance

```bash
# Launch EC2 instance (Ubuntu 22.04)
# Security groups: 22 (SSH), 80 (HTTP), 443 (HTTPS)

# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. Deploy Application

```bash
# Clone repository
git clone https://github.com/yourusername/autoagenthire.git
cd autoagenthire

# Configure environment
cp .env.example .env
nano .env  # Add production credentials

# Start services
docker-compose -f docker/docker-compose.yml up -d
```

#### 3. Setup Nginx Reverse Proxy

```bash
# Install Nginx
sudo apt install nginx -y

# Configure Nginx
sudo nano /etc/nginx/sites-available/autoagenthire
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/autoagenthire /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. Setup SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal (added automatically)
sudo systemctl status certbot.timer
```

### Google Cloud Platform (GCP) Deployment

#### 1. Setup Cloud SQL (PostgreSQL)

```bash
# Create Cloud SQL instance
gcloud sql instances create autoagenthire-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1

# Create database
gcloud sql databases create autoagenthire \
    --instance=autoagenthire-db

# Create user
gcloud sql users create appuser \
    --instance=autoagenthire-db \
    --password=secure-password
```

#### 2. Deploy to Cloud Run

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT_ID/autoagenthire-backend

# Deploy backend
gcloud run deploy autoagenthire-backend \
    --image gcr.io/PROJECT_ID/autoagenthire-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars DATABASE_URL=postgresql://... \
    --add-cloudsql-instances PROJECT_ID:us-central1:autoagenthire-db
```

### Kubernetes Deployment

#### 1. Create Kubernetes Manifests

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: autoagenthire-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: autoagenthire-backend
  template:
    metadata:
      labels:
        app: autoagenthire-backend
    spec:
      containers:
      - name: backend
        image: autoagenthire/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
```

#### 2. Deploy to Kubernetes

```bash
# Apply configurations
kubectl apply -f k8s/

# Expose service
kubectl expose deployment autoagenthire-backend \
    --type=LoadBalancer \
    --port=80 \
    --target-port=8000
```

## Database Migrations

### Using Alembic

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Monitoring & Logging

### Setup Sentry

```bash
# Add to .env
SENTRY_DSN=your-sentry-dsn
```

### Setup Prometheus + Grafana

```yaml
# Add to docker-compose.yml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
```

## Backup & Recovery

### Database Backup

```bash
# Backup PostgreSQL
docker exec autoagenthire-db pg_dump -U postgres autoagenthire > backup.sql

# Restore
docker exec -i autoagenthire-db psql -U postgres autoagenthire < backup.sql
```

### Vector Database Backup

```bash
# Backup ChromaDB
docker cp autoagenthire-chromadb:/chroma/chroma ./chroma-backup

# Restore
docker cp ./chroma-backup autoagenthire-chromadb:/chroma/chroma
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check PostgreSQL is running
   docker-compose ps postgres
   
   # Check logs
   docker-compose logs postgres
   ```

2. **OpenAI API Error**
   ```bash
   # Verify API key
   echo $OPENAI_API_KEY
   
   # Test API
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

3. **Port Already in Use**
   ```bash
   # Find process using port
   lsof -i :8000
   
   # Kill process
   kill -9 <PID>
   ```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database connectivity
docker exec -it autoagenthire-db psql -U postgres -c "SELECT 1"

# Redis connectivity
docker exec -it autoagenthire-redis redis-cli ping
```

## Performance Optimization

1. **Enable Redis Caching**
   - Cache frequent queries
   - Store session data

2. **Database Indexing**
   - Add indices on frequently queried columns
   - Optimize query patterns

3. **Vector Database Tuning**
   - Adjust embedding dimensions
   - Optimize collection size

4. **API Rate Limiting**
   - Implement request throttling
   - Use Redis for distributed rate limiting

## Security Checklist

- [ ] Change default passwords
- [ ] Enable HTTPS/SSL
- [ ] Implement rate limiting
- [ ] Use secrets management (Vault, AWS Secrets Manager)
- [ ] Enable database encryption
- [ ] Setup firewall rules
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Implement CORS properly
- [ ] Use environment-specific configs

## Scaling Considerations

1. **Horizontal Scaling**
   - Multiple backend instances
   - Load balancer (Nginx, AWS ALB)
   - Shared session storage (Redis)

2. **Database Scaling**
   - Read replicas
   - Connection pooling
   - Query optimization

3. **Async Processing**
   - Celery workers
   - Task queue (Redis, RabbitMQ)
   - Background job scheduling

## Support

For deployment issues:
- Check logs: `docker-compose logs -f`
- Review documentation: `docs/`
- Open issue: GitHub Issues
- Email: support@autoagenthire.com
