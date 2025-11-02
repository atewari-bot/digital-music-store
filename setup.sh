#!/bin/bash
# Setup script for Digital Music Store AI Agent

set -e

echo "🎵 Digital Music Store AI Agent - Setup"
echo "========================================"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Python dependencies installed!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Start the backend server:"
echo "   python api/server.py"
echo ""
echo "3. (In another terminal) Install frontend dependencies:"
echo "   cd frontend && npm install"
echo ""
echo "4. Start the frontend:"
echo "   npm run dev"

