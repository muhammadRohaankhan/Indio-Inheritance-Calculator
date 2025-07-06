from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from backend.api.routes import router

app = FastAPI(title="Estate Inheritance Calculator MVP")
app.include_router(router)

frontend_path = Path(__file__).resolve().parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
