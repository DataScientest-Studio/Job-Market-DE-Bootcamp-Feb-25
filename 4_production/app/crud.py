# Contains functions that perform database operations
from sqlalchemy.orm import Session
from app.models import AdzunaAd, AdzunaSalary, AdzunaCategory
from typing import Optional

def get_ads(db: Session, skip: int = 0, limit: Optional[int] = None):
    query = db.query(AdzunaAd).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

def get_salary(db: Session, skip: int = 0, limit: Optional[int] = None):
    query = db.query(AdzunaSalary).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

def get_category(db: Session, skip: int = 0, limit: Optional[int] = None):
    query = db.query(AdzunaCategory).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

'''
def get_ads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AdzunaAd).offset(skip).limit(limit).all()

def get_salary(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AdzunaSalary).offset(skip).limit(limit).all()

def get_category(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AdzunaCategory).offset(skip).limit(limit).all()
'''