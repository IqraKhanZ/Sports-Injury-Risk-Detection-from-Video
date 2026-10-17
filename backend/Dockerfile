# Dockerfile for Backend Service
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for OpenCV, FFmpeg, and MediaPipe EGL
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    libegl1 \
    libgles2 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
