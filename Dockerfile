# Backend Dockerfile for Digital Music Store AI Agent
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Create images directory if it doesn't exist
RUN mkdir -p images && \
    chmod -R 755 images

# Expose port
EXPOSE 8000

# Healthcheck will be handled by docker-compose

# Command to run the application
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]

