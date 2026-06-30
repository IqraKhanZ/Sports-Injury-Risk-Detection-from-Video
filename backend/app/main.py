from fastapi import FastAPI

app = FastAPI(
    title="Sports Injury Risk Detection API",
    description="Backend API for detecting and analyzing sports injury risks from video feeds.",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
