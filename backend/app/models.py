from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Attempt(Base):
    """Modelo para armazenar tentativas de conexão no honeypot"""
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String(45), index=True, nullable=False)  # IPv6 pode ter até 45 chars
    data = Column(Text, nullable=True)  # Usar Text para dados maiores
    timestamp = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        index=True  # Index para ordenação por timestamp
    )

    def __repr__(self):
        return f"<Attempt(id={self.id}, ip='{self.ip}', timestamp='{self.timestamp}')>"
