from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from neo4j_db import init_neo4j_schema, close_neo4j
import api

# Initialize SQL tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Investigation Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_neo4j_schema()

@app.on_event("shutdown")
def shutdown_event():
    close_neo4j()

app.include_router(api.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Investigative Platform API"}
