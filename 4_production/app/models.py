from sqlalchemy import Column, Integer, String, DateTime, Float
from app.database import Base

class AdzunaAd(Base):
    __tablename__ = 'adzuna_ads_all'

    job_offer_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    company = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    location = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    contract_type = Column(String, nullable=True)
    fixed_contract = Column(Integer, nullable=True)
    limited_contract = Column(Integer, nullable=True)
    contract_undefined = Column(Integer, nullable=True)

class AdzunaSalary(Base):
    __tablename__ = 'salary_m24'

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, index=True, nullable=False)
    location = Column(String, index=True, nullable=False)
    job_title = Column(String, index=True, nullable=False)
    salary = Column(Float, nullable=False)  # Assuming salary is a float
    
class AdzunaCategory(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, index=True, nullable=False)
    label = Column(String, index=True, nullable=False)
