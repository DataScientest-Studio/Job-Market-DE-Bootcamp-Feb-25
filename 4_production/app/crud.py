from sqlalchemy.orm import Session
from app.models import AdzunaAd

def get_ads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AdzunaAd).offset(skip).limit(limit).all()

