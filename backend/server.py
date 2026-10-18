import sys
import os

# Ensure the root directory is at the very front of sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import gradio as gr
from app.main import app as fastapi_app

# Visual dashboard rendered when opening the Hugging Face Space URL directly
with gr.Blocks(title="SIRD - Sports Injury Risk Detection API") as demo:
    gr.Markdown("# 🏃 SIRD - Sports Injury Risk Detection API")
    gr.Markdown(
        "### System Status: **Online & Operational** (Hugging Face Spaces - 16 GB RAM)\n\n"
        "Welcome to the SIRD Backend Service. The API is active and ready to handle biomechanical tracking, "
        "pose estimation, and machine learning injury risk analysis.\n\n"
        "#### Useful Quick Links:\n"
        "- 📖 **Interactive Swagger UI**: [View API Documentation](/docs)\n"
        "- 📑 **ReDoc Documentation**: [View ReDoc](/redoc)\n"
        "- 🩺 **Health Check**: [View Health Status](/api/health)\n"
    )

# Mount Gradio onto the existing FastAPI application
# All /api/... routes, static /storage files, and /docs take full priority.
app = gr.mount_gradio_app(fastapi_app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
