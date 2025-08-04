from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Modelo de entrada para crear un registro de estado emocional
class EmotionEntryCreate(BaseModel):
    user_id: str
    emotions: List[str] = Field(..., min_items=1)
    note: Optional[str] = None
    created_at: Optional[datetime] = None

# Modelo que representa un registro completo con ID
class EmotionEntry(EmotionEntryCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
