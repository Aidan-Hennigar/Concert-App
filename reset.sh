#!/bin/bash

echo "🧹 Resetting Concert App environment..."

# Stop and remove all Docker containers
echo "Stopping Docker containers..."
docker-compose down --remove-orphans

# Remove all containers, networks, and volumes (nuclear option)
echo "Cleaning up Docker completely..."
docker system prune -f
docker volume prune -f

# Kill any remaining processes on common ports
echo "Killing processes on ports 8000, 8001, 5432, 9000..."
sudo pkill -f "uvicorn" || true
sudo pkill -f "python.*8000" || true
sudo pkill -f "python.*8001" || true
sudo pkill -f "postgres" || true
sudo pkill -f "minio" || true

# Wait a moment for processes to fully terminate
sleep 2

# Check if ports are free
echo "Checking port availability..."
if ss -tlnp | grep -q ":8000"; then
    echo "⚠️  Port 8000 still in use"
else
    echo "✅ Port 8000 is free"
fi

if ss -tlnp | grep -q ":8001"; then
    echo "⚠️  Port 8001 still in use"
else
    echo "✅ Port 8001 is free"
fi

if ss -tlnp | grep -q ":5432"; then
    echo "⚠️  Port 5432 still in use"
else
    echo "✅ Port 5432 is free"
fi

if ss -tlnp | grep -q ":9000"; then
    echo "⚠️  Port 9000 still in use"
else
    echo "✅ Port 9000 is free"
fi

echo ""
echo "🎯 Reset complete! You can now run:"
echo "  docker compose up -d"
echo ""
echo "Or to start fresh with rebuild:"
echo "  docker compose up -d --build"
