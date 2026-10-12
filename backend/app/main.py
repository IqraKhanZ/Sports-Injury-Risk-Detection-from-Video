import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Database, seed_demo_accounts
from app.seed_12_athletes import seed_all_12_athletes
import os
import traceback
from fastapi.staticfiles import StaticFiles
from app.routes import (
    auth_routes, user_routes, video_routes,
    prediction_routes, recommendation_routes,
    notification_routes, report_routes, system_routes
)
from app.engines.ml_prediction_engine import MLPredictionEngine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure storage paths exist
    os.makedirs("storage/processed", exist_ok=True)
    # Connect database on startup
    await Database.connect_db()
    # Seed demo users if they do not exist
    await seed_demo_accounts()
    # Seed full athlete profiles with baseline telemetry & predictions
    await seed_all_12_athletes()
    # Load ML models
    MLPredictionEngine.load_models()
    yield
    # Close database connection on shutdown
    await Database.close_db()

app = FastAPI(
    title="SIRD - Sports Injury Risk Detection API",
    description="Backend API services for user auth, biomechanics, ML predictions, recommendations & system metrics",
    version="3.0.0",
    lifespan=lifespan
)

class CORSStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

# Resolve storage static files directory
storage_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage")
os.makedirs(storage_dir, exist_ok=True)
os.makedirs(os.path.join(storage_dir, "processed"), exist_ok=True)

# Mount storage static files with CORS headers
app.mount("/storage", CORSStaticFiles(directory=storage_dir), name="storage")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ],
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(video_routes.router)
app.include_router(prediction_routes.router)
app.include_router(recommendation_routes.router)
app.include_router(notification_routes.router)
app.include_router(report_routes.router)
app.include_router(system_routes.router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("GLOBAL EXCEPTION DETECTED:")
    traceback.print_exc()
    
    response = JSONResponse(
        status_code=500,
        content={
            "detail": f"Internal Server Error: {str(exc)}",
            "traceback": traceback.format_exc()
        }
    )
    origin = request.headers.get("origin", "*")
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.get("/")
async def root():
    return {
        "app": "SIRD (Sports Injury Risk Detection)",
        "status": "online",
        "version": "3.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
