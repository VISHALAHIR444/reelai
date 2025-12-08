#!/bin/bash

# AutoReels AI Backend - Complete Setup and Deployment Guide
# Run this on your Linux VPS (210.79.129.253)

set -e

echo "🚀 AutoReels AI Backend - Setup Script"
echo "======================================"

# 1. System Dependencies
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y redis-server
sudo apt install -y ffmpeg
sudo apt install -y git curl

# 2. Create Python Virtual Environment
echo "🐍 Creating virtual environment..."
cd /home/ubuntu/autoreels-ai/backend
python3.11 -m venv venv
source venv/bin/activate

# 3. Install Python Dependencies
echo "📚 Installing Python packages..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 4. Setup PostgreSQL Database
echo "🗄️  Setting up PostgreSQL..."
sudo systemctl start postgresql
sudo -u postgres psql << EOF
CREATE DATABASE autoreels_db;
CREATE USER autoreels_user WITH PASSWORD 'autoreels_secure_pass_123';
ALTER ROLE autoreels_user SET client_encoding TO 'utf8';
ALTER ROLE autoreels_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE autoreels_user SET default_transaction_deferrable TO on;
ALTER ROLE autoreels_user SET default_transaction_readonly TO off;
GRANT ALL PRIVILEGES ON DATABASE autoreels_db TO autoreels_user;
EOF

# 5. Setup Redis
echo "🔴 Starting Redis..."
sudo systemctl start redis-server
sudo systemctl enable redis-server

# 6. Create .env file
echo "⚙️  Creating .env file..."
cp .env.example .env

cat > .env << 'ENVEOF'
# Application
APP_NAME=AutoReels AI Backend
APP_VERSION=1.0.0
DEBUG=False
ENVIRONMENT=production
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Database
DATABASE_URL=postgresql://autoreels_user:autoreels_secure_pass_123@localhost:5432/autoreels_db
DATABASE_ECHO=False

# Redis & RQ
REDIS_URL=redis://localhost:6379/0
RQ_REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-change-this-to-random-64-char-key-in-production-!!!
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Storage Paths
STORAGE_BASE_PATH=/videos
TEMP_PATH=/tmp/autoreels

# FFmpeg
FFMPEG_PATH=/usr/bin/ffmpeg
FFPROBE_PATH=/usr/bin/ffprobe

# Video Processing
CHUNK_DURATION=35
REEL_WIDTH=1080
REEL_HEIGHT=1920
VIDEO_QUALITY=high
MAX_VIDEO_SIZE_MB=500

# Job Configuration
MAX_RETRIES=3
JOB_TIMEOUT=3600

# YouTube
YOUTUBE_API_KEY=your-youtube-api-key-here
YT_DLP_COOKIES_FILE=

# Google Cloud Speech-to-Text
GOOGLE_APPLICATION_CREDENTIALS=/path/to/google-credentials.json
GOOGLE_CLOUD_PROJECT=your-project-id

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-pro

# Instagram
INSTAGRAM_BUSINESS_ACCOUNT_ID=your-instagram-app-id
INSTAGRAM_GRAPH_API_VERSION=v18.0

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://210.79.129.253:3000,http://210.79.129.253:8000

# Logging
LOG_LEVEL=INFO
ENVEOF

echo "✅ .env file created. Update API keys manually!"

# 7. Create storage directories
echo "📁 Creating storage directories..."
mkdir -p /videos
mkdir -p /tmp/autoreels
chmod 755 /videos /tmp/autoreels

# 8. Initialize database
echo "🗄️  Initializing database..."
python3 -c "
from app.db.database import engine
from app.db.base import Base
Base.metadata.create_all(bind=engine)
print('✅ Database tables created')
"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your API keys"
echo "2. Run: python main.py (Backend server)"
echo "3. Run: rq worker (In another terminal for background jobs)"
echo "4. Backend will be available at: http://210.79.129.253:8000"
echo "5. API Docs: http://210.79.129.253:8000/docs"
