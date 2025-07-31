from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class AttemptBase(BaseModel):
    """Schema base para tentativas"""
    ip: str = Field(..., min_length=7, max_length=45, description="IP address")
    data: Optional[str] = Field(None, max_length=10000, description="Connection data")

    @validator('ip')
    def validate_ip(cls, v):
        """Validação básica de IP"""
        if not v or len(v.strip()) == 0:
            raise ValueError('IP address cannot be empty')
        return v.strip()

    @validator('data')
    def validate_data(cls, v):
        """Limpar dados se necessário"""
        if v is not None:
            return v.strip()
        return v

class AttemptCreate(AttemptBase):
    """Schema para criação de tentativas"""
    pass

class Attempt(AttemptBase):
    """Schema completo de tentativa com dados do banco"""
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True  # SQLAlchemy 1.4 syntax
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class StatsResponse(BaseModel):
    """Schema para resposta de estatísticas"""
    total_attempts: int = Field(..., ge=0)
    unique_ips: int = Field(..., ge=0)
