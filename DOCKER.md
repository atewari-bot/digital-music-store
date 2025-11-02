# Docker Setup Guide

This guide explains how to run the Digital Music Store AI Agent using Docker.

## Quick Start

1. **Create `.env` file:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

2. **Start all services:**
```bash
docker-compose up --build
```

3. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Docker Compose Files

### Production (`docker-compose.yml`)
- Optimized for production use
- Uses pre-built images
- Nginx serves static frontend files

### Development (`docker-compose.dev.yml`)
- Hot reload enabled
- Mounts source code as volumes
- Better for active development

## Common Commands

### Start Services
```bash
# Production mode
docker-compose up

# Development mode (with hot reload)
docker-compose -f docker-compose.dev.yml up

# Start in background
docker-compose up -d
```

### Stop Services
```bash
docker-compose down

# Remove volumes too
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild After Changes
```bash
# Rebuild all
docker-compose up --build

# Rebuild specific service
docker-compose build backend
docker-compose build frontend
```

### Check Status
```bash
# Running containers
docker-compose ps

# Container health
docker ps
```

## Services

### Backend Service
- **Container**: `digital-music-store-backend`
- **Port**: 8000
- **Health Check**: http://localhost:8000/health
- **Environment Variables**: Loaded from `.env` file

### Frontend Service
- **Container**: `digital-music-store-frontend`
- **Port**: 3000
- **Proxy**: Routes `/api/*` to backend
- **Build**: Uses multi-stage build with Nginx

## Environment Variables

Required environment variables (set in `.env` file):
- `OPENAI_API_KEY` or `TOGETHER_API_KEY` (at least one required)

Optional environment variables:
- `LANGSMITH_API_KEY` - For monitoring
- `LANGCHAIN_TRACING_V2` - Enable tracing
- `LANGCHAIN_ENDPOINT` - LangSmith endpoint
- `LANGCHAIN_PROJECT` - Project name for LangSmith

## Troubleshooting

### Port Already in Use
Change ports in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Backend on 8001
  - "3001:80"    # Frontend on 3001
```

### Container Won't Start
1. Check logs: `docker-compose logs backend`
2. Verify `.env` file exists with API keys
3. Check Docker is running: `docker ps`

### Frontend Can't Connect to Backend
1. Ensure backend is running: `docker-compose ps`
2. Check network: `docker network ls`
3. Verify API URL in frontend config

### Rebuild Everything
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### View Container Shell
```bash
# Backend
docker-compose exec backend /bin/bash

# Frontend
docker-compose exec frontend /bin/sh
```

## Development Workflow

1. **Start in development mode:**
```bash
docker-compose -f docker-compose.dev.yml up
```

2. **Make code changes** - Changes will automatically reload

3. **View logs:**
```bash
docker-compose -f docker-compose.dev.yml logs -f
```

4. **Rebuild if dependencies change:**
```bash
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up
```

## Production Deployment

For production deployment:

1. **Build images:**
```bash
docker-compose build
```

2. **Tag and push to registry:**
```bash
docker tag digital-music-store-backend:latest your-registry/backend:latest
docker tag digital-music-store-frontend:latest your-registry/frontend:latest
docker push your-registry/backend:latest
docker push your-registry/frontend:latest
```

3. **Update docker-compose.yml** with registry URLs

4. **Deploy with:**
```bash
docker-compose up -d
```

## Performance Tips

- Use `.dockerignore` to exclude unnecessary files
- Leverage Docker layer caching by copying dependencies before code
- Use multi-stage builds for smaller images
- Consider using Docker volumes for persistent data

