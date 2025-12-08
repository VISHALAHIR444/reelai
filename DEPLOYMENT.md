# AutoReels AI - Deployment Guide

## 🚀 Quick Start for Development

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd autoreels-ai

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local

# Update .env.local with your configuration
# NEXT_PUBLIC_API_URL=http://localhost:3001/api
# NEXT_PUBLIC_INSTAGRAM_CLIENT_ID=your_app_id
# NEXT_PUBLIC_INSTAGRAM_REDIRECT_URI=http://localhost:3000/connect-instagram

# Start development server
npm run dev
```

Visit `http://localhost:3000`

---

## 🖥️ VPS Deployment (Linux)

### Prerequisites
- Ubuntu 20.04+ or similar Linux distribution
- Root or sudo access
- Domain name (optional but recommended)

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install npm packages globally
sudo npm install -g pm2

# Verify installation
node -v
npm -v
pm2 -v
```

### Step 2: Clone and Setup Application

```bash
# Create app directory
sudo mkdir -p /var/www/autoreels-ai
cd /var/www/autoreels-ai

# Clone repository
sudo git clone <repository-url> .

# Install dependencies
sudo npm install --production

# Build the application
sudo npm run build
```

### Step 3: Environment Configuration

```bash
# Create .env.local
sudo nano .env.local

# Add your configuration:
# NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
# NEXT_PUBLIC_INSTAGRAM_CLIENT_ID=your_instagram_app_id
# NEXT_PUBLIC_INSTAGRAM_REDIRECT_URI=https://yourdomain.com/connect-instagram
# NODE_ENV=production
```

### Step 4: Setup PM2 Process Manager

```bash
# Start application with PM2
sudo pm2 start npm --name "autoreels-ai" -- start

# Configure PM2 startup
sudo pm2 startup
sudo pm2 save

# Check status
sudo pm2 status
```

### Step 5: Setup Nginx Reverse Proxy

```bash
# Install Nginx
sudo apt install -y nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/autoreels-ai

# Add the following configuration:
```

```nginx
upstream autoreels_backend {
    server localhost:3000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://autoreels_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/autoreels-ai /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### Step 6: Setup SSL Certificate (HTTPS)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renew certificates
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Verify renewal
sudo certbot renew --dry-run
```

### Step 7: Firewall Configuration

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

---

## 📦 Docker Deployment

### Dockerfile

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application
COPY . .

# Build application
RUN npm run build

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: autoreels-ai
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
      - NEXT_PUBLIC_INSTAGRAM_CLIENT_ID=${INSTAGRAM_CLIENT_ID}
      - NEXT_PUBLIC_INSTAGRAM_REDIRECT_URI=https://yourdomain.com/connect-instagram
    restart: always
    networks:
      - autoreels-network

networks:
  autoreels-network:
    driver: bridge
```

### Deploy with Docker

```bash
# Build image
docker build -t autoreels-ai:latest .

# Run container
docker run -d \
  --name autoreels-ai \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api \
  autoreels-ai:latest

# Using Docker Compose
docker-compose up -d
```

---

## ☁️ Vercel Deployment (Recommended)

### Step 1: Connect Repository

1. Go to [Vercel.com](https://vercel.com)
2. Sign up or log in
3. Click "Add New" → "Project"
4. Import your Git repository

### Step 2: Configure Environment

1. In the Vercel dashboard
2. Go to Settings → Environment Variables
3. Add:
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_INSTAGRAM_CLIENT_ID`
   - `NEXT_PUBLIC_INSTAGRAM_REDIRECT_URI`

### Step 3: Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy production
vercel --prod
```

---

## 🔧 Maintenance

### View Logs

```bash
# PM2 logs
sudo pm2 logs autoreels-ai

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Update Application

```bash
# Pull latest code
cd /var/www/autoreels-ai
sudo git pull origin main

# Install dependencies
sudo npm install --production

# Build
sudo npm run build

# Restart application
sudo pm2 restart autoreels-ai
```

### Monitor Performance

```bash
# Monitor with PM2
sudo pm2 monit

# Check system resources
sudo htop
```

### Backup

```bash
# Create backup
sudo tar -czf autoreels-ai-backup-$(date +%Y%m%d).tar.gz /var/www/autoreels-ai

# Restore backup
sudo tar -xzf autoreels-ai-backup-20240101.tar.gz -C /var/www/
```

---

## 🔒 Security Best Practices

### 1. Environment Variables
- Never commit `.env.local` to Git
- Use `.env.example` for template
- Rotate secrets regularly

### 2. CORS Configuration
- Configure CORS in backend for frontend domain
- Use HTTPS only in production

### 3. Dependencies
- Keep dependencies updated
- Use `npm audit` regularly
- Use `npm ci` for exact versions

### 4. Database
- Use strong passwords
- Enable SSL connections
- Regular backups

### 5. Monitoring
- Setup uptime monitoring
- Enable error tracking (Sentry)
- Monitor API rate limits

---

## 📊 Performance Optimization

### Build Optimization
```bash
# Analyze bundle size
npm install -g next-bundle-analyzer

# Build with analysis
npm run build
```

### Caching
- Enable browser caching in Nginx
- Configure Next.js ISR
- Use CDN for static assets

### Compression
```nginx
gzip on;
gzip_types text/css text/javascript application/javascript;
```

---

## 🚨 Troubleshooting

### Application won't start
```bash
# Check Node version
node -v

# Check logs
pm2 logs autoreels-ai

# Rebuild
npm run build
```

### Port already in use
```bash
# Kill process on port 3000
sudo lsof -ti:3000 | xargs kill -9
```

### Build fails
```bash
# Clear cache
rm -rf .next
npm cache clean --force

# Rebuild
npm run build
```

### SSL certificate issues
```bash
# Check certificate
sudo certbot certificates

# Renew manually
sudo certbot renew --force-renewal
```

---

## 📞 Support

For issues or questions:
- Check logs: `sudo pm2 logs autoreels-ai`
- Review documentation
- Contact: support@autoreels-ai.com

---

**Last Updated**: December 2024
