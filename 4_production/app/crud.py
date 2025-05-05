# Contains functions that perform database operations
from sqlalchemy.orm import Session
from app.models import AdzunaAd, AdzunaSalary, AdzunaCategory

def get_ads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AdzunaAd).offset(skip).limit(limit).all()

def get_salary(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AdzunaSalary).offset(skip).limit(limit).all()

def get_category(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AdzunaCategory).offset(skip).limit(limit).all()

