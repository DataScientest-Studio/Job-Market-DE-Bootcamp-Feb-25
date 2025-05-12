from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas, crud
from app.database import SessionLocal, engine
from app.schemas import AdzunaAdSchema, AdzunaSalarySchema, AdzunaCategorySchema
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/ads/", response_model=list[schemas.AdzunaAdSchema])
def read_ads(skip: int = 0, limit: Optional[int] = None, db: Session = Depends(get_db)):
    ads = crud.get_ads(db, skip=skip, limit=limit)
    return ads

@app.get("/salary/", response_model=list[schemas.AdzunaSalarySchema])
def read_salary(skip: int = 0, limit: Optional[int] = None, db: Session = Depends(get_db)):
    ads = crud.get_salary(db, skip=skip, limit=limit)
    return ads

@app.get("/category/", response_model=list[schemas.AdzunaCategorySchema])
def read_salary(skip: int = 0, limit: Optional[int] = None, db: Session = Depends(get_db)):
    ads = crud.get_category(db, skip=skip, limit=limit)
    return ads
