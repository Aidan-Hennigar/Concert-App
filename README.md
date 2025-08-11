# Concert App

A modern concert management application with health monitoring.

## Health & Readiness Probes

The application includes comprehensive health monitoring:

### Endpoints

- **`/healthz`** - Health check endpoint that indicates the process is running
- **`/readyz`** - Readiness check endpoint that verifies:
  - Database connectivity (PostgreSQL)
  - MinIO storage connectivity

### Docker Health Checks

All services include Docker health checks:

- **PostgreSQL**: Uses `pg_isready` to verify database availability
- **MinIO**: Checks the MinIO health endpoint
- **Backend**: Uses the `/readyz` endpoint to verify full system readiness

### Usage

```bash
# Check if the process is running
curl http://localhost:8001/healthz

# Check if the system is ready to serve requests
curl http://localhost:8001/readyz

# View Docker service health status
docker compose ps
```

## API Endpoints

- **`/`** - Root endpoint with API status
- **`/healthz`** - Health check
- **`/readyz`** - Readiness check
- **`/users`** - User management (GET: list users, POST: add user)

## Troubleshooting

### Port Conflicts & Reset

If you encounter port conflicts or need a fresh start:

**Quick Reset (just stop everything):**
```bash
./quick-reset.sh
```

**Full Reset (clean slate):**
```bash
./reset.sh
```

**Manual Reset:**
```bash
# Stop containers
docker compose down

# Kill any remaining processes
sudo pkill -f "uvicorn" || true
sudo pkill -f "python.*800" || true

# Start fresh
docker compose up -d --build
```

### Common Issues

- **Port already in use**: Run `./reset.sh` to clear everything
- **Import errors**: Ensure you're using the reset scripts to avoid stale containers
- **Health check failures**: Wait for all services to be healthy before testing endpoints