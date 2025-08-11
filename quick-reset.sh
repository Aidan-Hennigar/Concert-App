#!/bin/bash

echo "🛑 Quick reset - stopping everything..."

# Stop Docker containers
docker-compose down

# Kill any obvious processes
sudo pkill -f "uvicorn" || true
sudo pkill -f "python.*800" || true

echo "✅ Quick reset done!"
echo "Run 'docker-compose up -d' to start again"
