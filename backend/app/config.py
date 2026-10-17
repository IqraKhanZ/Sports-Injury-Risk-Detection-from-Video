import os
from dotenv import load_dotenv

# Load .env file from the SIRD backend directory
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_env = os.path.join(backend_dir, ".env")
if os.path.exists(backend_env):
    load_dotenv(backend_env, override=True)
else:
    root_dir = os.path.dirname(os.path.dirname(backend_dir))
    load_dotenv(os.path.join(root_dir, ".env"))

class Settings:
    # --- Database ---
    # Must be set in .env — no credentials are hardcoded here.
    MONGODB_URL: str = os.getenv("MONGODB_URL", "")
    # Explicit database name; extracted from URI if not set.
    DB_NAME: str = os.getenv("DB_NAME", "sports_injury")

    # --- Security ---
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    # --- Google OAuth2 ---
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "").rstrip("/")

    # --- AI / External APIs ---
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # --- Service URLs ---
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "").rstrip("/")
    VITE_API_URL: str = os.getenv("VITE_API_URL", "").rstrip("/")

    # --- Server ---
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")

settings = Settings()
