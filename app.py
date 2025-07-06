from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Estate Inheritance Calculator MVP")
app.include_router(router)