from fastapi import FastAPI
from app.database import init_db
from app.routers import auth

app = FastAPI(
    title="Sports Injury Risk Detection API",
    description="Backend API for detecting and analyzing sports injury risks from video feeds.",
    version="0.1.0"
)

@app.on_event("startup")
async def startup_db_client():
    await init_db()

# Include routers
app.include_router(auth.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
