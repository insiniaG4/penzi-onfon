# Penzi Project Deployment Guide

## Overview
This document explains the complete deployment process of the Penzi dating application on AWS EC2 using Docker.

## Server Information
- **Server IP**: 52.48.121.185
- **SSH Key**: lawrence
- **Server Location**: ~/lawrence/penzi_project/
- **Operating System**: Ubuntu 24.04.2 LTS

## Application Architecture
- **Frontend**: React + Vite (served by Nginx)
- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Containerization**: Docker + Docker Compose

## Port Configuration
- **Frontend**: Port 8080 (external) → Port 80 (internal nginx)
- **Backend**: Port 8000 (external) → Port 5000 (internal flask)
- **Database**: Internal only (port 5432, not exposed externally)

## Deployment Steps Completed

### 1. Initial Setup
- Connected to server via SSH: `ssh -i lawrence ubuntu@52.48.121.185`
- Located project in: `~/lawrence/penzi_project/`
- Project was extracted from: `penzi_project.zip`

### 2. Docker Configuration Issues Fixed

#### Frontend Dockerfile Issues
**Problem**: Build was failing with Node.js module errors
**Solution**: Updated Dockerfile from:
```dockerfile
FROM node:18-alpine
RUN npm ci --only=production
```
To:
```dockerfile
FROM node:20-alpine
RUN npm install
```

**Key Changes**:
- Upgraded Node.js from v18 to v20 for better ES module support
- Changed from `npm ci --only=production` to `npm install` to include devDependencies needed for Vite build
- Added `.dockerignore` file to prevent copying local node_modules

#### Port Conflicts Resolution
**Problem**: Port 3000 was showing friend's application instead of yours
**Solution**: Changed ports to avoid conflicts:
- Frontend: 3000 → 8080
- Backend: 5000 → 8000

### 3. Database Connection Issues Fixed

#### Problem
Backend was failing to connect to PostgreSQL with error:
```
connection to server at "db" (172.19.0.2), port 5432 failed: Connection refused
```

#### Solution
Added health checks and proper dependency management in docker-compose.yml:
```yaml
services:
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U penzi_user -d penzi_project"]
      interval: 5s
      timeout: 5s
      retries: 5
  
  backend:
    depends_on:
      db:
        condition: service_healthy
```

### 4. API Configuration Updates

#### Frontend API Configuration
Updated `frontend/src/utils/api.js`:
```javascript
// Changed from:
const API_BASE_URL = 'http://localhost:5000';

// To:
const API_BASE_URL = 'http://52.48.121.185:8000';
```

### 5. File Ownership Issues
**Problem**: Permission denied when copying files
**Solution**: Changed ownership of project files:
```bash
sudo chown -R ubuntu:ubuntu ~/lawrence/penzi_project
```

## Final Docker Compose Configuration

```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: penzi_project
      POSTGRES_USER: penzi_user
      POSTGRES_PASSWORD: penzi123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - penzi-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U penzi_user -d penzi_project"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:5000"
    environment:
      - FLASK_ENV=production
      - FLASK_APP=run.py
      - DATABASE_URL=postgresql://penzi_user:penzi123@db:5432/penzi_project
    volumes:
      - ./backend:/app
    depends_on:
      db:
        condition: service_healthy
    networks:
      - penzi-network
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "8080:80"
    depends_on:
      - backend
    networks:
      - penzi-network
    restart: unless-stopped

networks:
  penzi-network:
    driver: bridge

volumes:
  postgres_data:
```

## Current Status

### ✅ Working Components
1. **Database**: PostgreSQL running and healthy
2. **Backend**: Flask application running on port 8000
3. **Frontend**: React app built and served by Nginx on port 8080
4. **Local Access**: Both services respond correctly to localhost requests

### ⚠️ Remaining Issue: AWS Security Group

**Problem**: External access blocked by AWS firewall
**Evidence**: 
- `curl -I http://localhost:8080` returns HTTP 200 ✅
- `curl -I http://localhost:8000` returns HTTP 404 ✅ (normal for root path)
- `ss -tlnp | grep -E "(8080|8000)"` shows ports listening on 0.0.0.0 ✅
- Browser access to `http://52.48.121.185:8080` times out ❌

**Solution Required**: Update AWS Security Group to allow inbound traffic on ports 8080 and 8000

## AWS Security Group Configuration Needed

### Steps to Fix External Access:
1. Go to AWS Console → EC2 → Instances
2. Select instance `ip-172-31-12-169`
3. Click Security tab → Click Security Group link
4. Click "Edit inbound rules"
5. Add two rules:
   - **Rule 1**: Custom TCP, Port 8080, Source 0.0.0.0/0
   - **Rule 2**: Custom TCP, Port 8000, Source 0.0.0.0/0
6. Save rules

## Application URLs (After Security Group Fix)
- **Frontend**: http://52.48.121.185:8080
- **Backend API**: http://52.48.121.185:8000/api/users/stats
- **SMS Processing**: http://52.48.121.185:8000/api/sms/process-incoming

## Useful Commands for Management

### Check Container Status
```bash
cd ~/lawrence/penzi_project
sudo docker-compose ps
```

### View Logs
```bash
sudo docker-compose logs
sudo docker-compose logs frontend
sudo docker-compose logs backend
sudo docker-compose logs db
```

### Restart Services
```bash
sudo docker-compose down
sudo docker-compose up -d
```

### Rebuild After Changes
```bash
sudo docker-compose down
sudo docker-compose up --build -d
```

### Check Port Status
```bash
ss -tlnp | grep -E "(8080|8000)"
```

### Test Local Access
```bash
curl -I http://localhost:8080
curl -I http://localhost:8000/api/users/stats
```

## Project Structure on Server
```
~/lawrence/penzi_project/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   │   └── utils/
│   │       └── api.js
│   └── nginx.conf
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── run.py
│   └── app/
└── README.md (this file)
```

## Troubleshooting

### If Frontend Build Fails
```bash
cd ~/lawrence/penzi_project/frontend
sudo docker build -t test-frontend . --no-cache
```

### If Backend Can't Connect to Database
```bash
sudo docker-compose logs db
sudo docker-compose logs backend
```

### If Ports Are Not Accessible
```bash
ss -tlnp | grep -E "(8080|8000)"
curl -I http://localhost:8080
```

## Security Considerations
- Database is not exposed externally (good security practice)
- Frontend and backend use separate containers
- All services run in isolated Docker network
- Environment variables used for database credentials

## Next Steps After Security Group Fix
1. Test frontend access: http://52.48.121.185:8080
2. Test backend API: http://52.48.121.185:8000/api/users/stats
3. Verify SMS processing functionality
4. Monitor application logs for any issues
5. Consider setting up SSL/HTTPS for production use

---

**Note**: The application is fully functional and ready to serve users once the AWS Security Group is configured to allow external access to ports 8080 and 8000.