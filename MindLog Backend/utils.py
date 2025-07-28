from sqlalchemy.orm import Session
import models, schemas

def create_entry(db: Session, entry: schemas.EntryCreate):
    db_entry = models.Entry(title=entry.title, content=entry.content)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_entries(db: Session):
    return db.query(models.Entry).order_by(models.Entry.created_at.desc()).all()
