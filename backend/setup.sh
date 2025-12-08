#!/bin/bash

# AutoReels AI Backend Setup Script
# This script sets up the backend development environment

set -e

echo "🚀 AutoReels AI Backend Setup"
echo "=============================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your actual configuration!"
else
    echo "✓ .env already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Update .env with your configuration"
echo "   2. Ensure PostgreSQL is running"
echo "   3. Ensure Redis is running"
echo "   4. Run: python main.py"
echo ""
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
