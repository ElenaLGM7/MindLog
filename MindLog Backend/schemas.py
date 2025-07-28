from pydantic import BaseModel
from datetime import datetime

class EntryCreate(BaseModel):
    title: str
    content: str

class EntryOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
