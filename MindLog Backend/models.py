from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
