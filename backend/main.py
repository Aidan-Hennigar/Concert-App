from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from app.db import engine, AsyncSessionLocal, minio_client
from botocore.exceptions import ClientError

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Database is now managed by Alembic migrations
    pass

@app.get("/healthz")
async def health_check():
    """Health check endpoint - process is up"""
    return {"status": "healthy", "message": "Process is running"}

@app.get("/readyz")
async def readiness_check():
    """Readiness check endpoint - checks DB connection and MinIO bucket"""
    try:
        # Check database connection
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        
        # Check MinIO bucket (try to list buckets to verify connection)
        try:
            minio_client.list_buckets()
        except ClientError as e:
            raise HTTPException(status_code=503, detail=f"MinIO connection failed: {str(e)}")
        
        return {"status": "ready", "message": "Database and MinIO are accessible"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Live Life backend API is running."}

@app.post("/users")
async def add_user(username: str, email: str):
    async with AsyncSessionLocal() as session:
        try:
            await session.execute(
                text("INSERT INTO users (username, email) VALUES (:username, :email)"),
                {"username": username, "email": email},
            )
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    return {"status": "user added"}

@app.get("/users")
async def list_users():
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT id, username, email FROM users"))
            users = result.fetchall()
            print(f"Found {len(users)} users in database")
            # Convert Row objects to dictionaries
            return [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    except Exception as e:
        print(f"Error in list_users: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Phase 0 placeholders

@app.post("/events")
async def create_event(event_name: str, description: str = None):
    # Placeholder: You will add DB insert logic here later
    return {"message": f"Event '{event_name}' created (placeholder)."}

@app.get("/events")
async def list_events():
    # Placeholder: You will query DB and return list of events later
    return []

@app.get("/events/{event_id}/timeline")
async def event_timeline(event_id: int):
    # Placeholder: return empty timeline for now
    return {"event_id": event_id, "timeline": []}

