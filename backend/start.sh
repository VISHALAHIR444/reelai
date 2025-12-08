#!/bin/bash
# GRAVIXAI Backend Quick Start Script

echo "🚀 GRAVIXAI Backend Setup"
echo "======================="
echo ""

# 1. Create Python virtual environment
echo "1️⃣  Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Initialize database
echo "2️⃣  Initializing database..."
python3 -c "
from app.core.database import engine
from app.models import Base
Base.metadata.create_all(bind=engine)
print('✓ Database initialized')
"

# 3. Configure environment
echo "3️⃣  Environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file (update with your credentials)"
fi

# 4. Start Redis (optional)
echo "4️⃣  Redis server..."
if command -v redis-server &> /dev/null; then
    redis-server --daemonize yes
    echo "✓ Redis started"
else
    echo "⚠️  Redis not installed (optional for job queue)"
fi

# 5. Start FastAPI server
echo "5️⃣  Starting FastAPI server..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo ""
echo "✅ Backend ready at http://localhost:8000"
echo "📚 API docs at http://localhost:8000/docs"
