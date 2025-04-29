from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AdzunaAdSchema(BaseModel):
    id: int
    title: str
    company: str
    category: str
    location: str
    created: datetime  # datetime is fine, Pydantic will serialize it
    salary_min: Optional[float] = None  # Allow None
    salary_max: Optional[float] = None  # Allow None
    contract_type: Optional[str] = None  # Allow None

    class Config:
        from_attributes = True  # correct if you're using Pydantic v2
        # For Pydantic v1.x, use: orm_mode = True
        
class AdzunaSalarySchema(BaseModel):
    id: int
    month: str
    location: str
    job_title: str
    salary: float

    class Config:
        from_attributes = True  # correct if you're using Pydantic v2
        # For Pydantic v1.x, use: orm_mode = True



