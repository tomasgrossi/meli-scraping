from fastapi import FastAPI
from app.src.utils.settings import Settings
from fastapi.middleware.cors import CORSMiddleware
from .src.controllers import Router
from .src import models
from .src.utils.connection import db_engine

settings = Settings()

app = FastAPI()


models.Base.metadata.create_all(bind=db_engine)

# Cors
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Router)