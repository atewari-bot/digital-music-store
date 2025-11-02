#!/bin/bash
# Script to start the backend server

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    echo "Please run: ./setup.sh"
    exit 1
fi

# Check if FastAPI is installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "❌ FastAPI not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the server
echo "🚀 Starting backend server on http://localhost:8000"
python3 api/server.py

