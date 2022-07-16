from fastapi import FastAPI
from app.src.utils.settings import Settings
from .src.controllers import Router

settings = Settings()

app = FastAPI()

app.include_router(Router)



