from typing import List
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, get_db, Base
from . import models, schemas
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Honeypot API", version="1.0.0")

# Configuração CORS - mais permissiva para desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    """Criar tabelas no startup"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

@app.get("/health")
async def health_check():
    """Health check silencioso para Docker"""
    return {"status": "ok"}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Honeypot API is running"}

@app.get("/attempts/", response_model=List[schemas.Attempt])
async def get_attempts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obter tentativas de conexão"""
    try:
        attempts = db.query(models.Attempt).order_by(
            models.Attempt.timestamp.desc()
        ).offset(skip).limit(limit).all()
        return attempts
    except Exception as e:
        logger.error(f"Error fetching attempts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/attempts/", status_code=201)
async def create_attempt(attempt: schemas.AttemptCreate, db: Session = Depends(get_db)):
    """Criar nova tentativa de conexão"""
    try:
        db_attempt = models.Attempt(ip=attempt.ip, data=attempt.data)
        db.add(db_attempt)
        db.commit()
        db.refresh(db_attempt)
        logger.info(f"New attempt logged: {attempt.ip} - {attempt.data}")
        return {"status": "success", "id": db_attempt.id}
    except Exception as e:
        logger.error(f"Error creating attempt: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/stats/")
async def get_stats(db: Session = Depends(get_db)):
    """Obter estatísticas dos ataques"""
    try:
        total_attempts = db.query(models.Attempt).count()
        unique_ips = db.query(models.Attempt.ip).distinct().count()
        return {
            "total_attempts": total_attempts,
            "unique_ips": unique_ips
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
