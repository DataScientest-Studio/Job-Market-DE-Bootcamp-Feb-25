from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine
from app.schemas import AdzunaAdSchema
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
def read_ads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    ads = crud.get_ads(db, skip=skip, limit=limit)
    return ads
