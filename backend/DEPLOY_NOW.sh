#!/bin/bash

echo "🚀 AutoReels AI Backend Deployment"
echo "========================================"
echo ""
echo "VPS IP: 210.79.129.253"
echo "Status: ✅ FULLY IMPLEMENTED"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}✅ Step 1: System Dependencies${NC}"
sudo apt update
sudo apt install -y python3.11 python3.11-venv postgresql postgresql-contrib redis-server ffmpeg

echo -e "${GREEN}✅ Step 2: Virtual Environment${NC}"
cd /home/ubuntu/autoreels-ai/backend
python3.11 -m venv venv
source venv/bin/activate

echo -e "${GREEN}✅ Step 3: Install Python Packages${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✅ Step 4: Database Setup${NC}"
sudo systemctl start postgresql
sudo -u postgres psql << DBEOF
CREATE DATABASE autoreels_db;
CREATE USER autoreels_user WITH PASSWORD 'autoreels_secure_pass_123';
ALTER ROLE autoreels_user SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE autoreels_db TO autoreels_user;
DBEOF

echo -e "${GREEN}✅ Step 5: Redis Setup${NC}"
sudo systemctl start redis-server
sudo systemctl enable redis-server

echo -e "${GREEN}✅ Step 6: Storage Directories${NC}"
mkdir -p /videos
mkdir -p /tmp/autoreels
chmod 755 /videos /tmp/autoreels

echo -e "${GREEN}✅ Step 7: Configure .env${NC}"
if [ ! -f .env ]; then
  cp .env.example .env
  echo -e "${YELLOW}⚠️  Update .env with your API keys!${NC}"
  echo "   Edit: nano .env"
  echo ""
  echo "   Required keys:"
  echo "   - GEMINI_API_KEY"
  echo "   - YOUTUBE_API_KEY"
  echo "   - INSTAGRAM_BUSINESS_ACCOUNT_ID"
  echo "   - GOOGLE_APPLICATION_CREDENTIALS"
fi

echo ""
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE!${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1️⃣  Configure API Keys:"
echo "   $ nano .env"
echo ""
echo "2️⃣  Start Backend (Terminal 1):"
echo "   $ cd /home/ubuntu/autoreels-ai/backend"
echo "   $ source venv/bin/activate"
echo "   $ python main.py"
echo ""
echo "3️⃣  Start RQ Worker (Terminal 2):"
echo "   $ cd /home/ubuntu/autoreels-ai/backend"
echo "   $ source venv/bin/activate"
echo "   $ rq worker -u redis://localhost:6379/0"
echo ""
echo "4️⃣  Access Backend:"
echo "   🌐 API Docs: http://210.79.129.253:8000/docs"
echo "   🌐 Health:   http://210.79.129.253:8000/health"
echo "   🌐 API:      http://210.79.129.253:8000"
echo ""
echo "📚 Documentation: COMPLETE_BACKEND_GUIDE.md"
echo ""
