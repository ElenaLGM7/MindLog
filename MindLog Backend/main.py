from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models, schemas, utils
import os
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://elenalgm7.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "MindLog API online"}


@app.post("/entries/", response_model=schemas.EntryOut)
def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    return utils.create_entry(db, entry)


@app.get("/entries/", response_model=list[schemas.EntryOut])
def read_entries(db: Session = Depends(get_db)):
    return utils.get_entries(db)
