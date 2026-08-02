from pydantic import BaseModel, Field
from typing import Dict, List

class StudentRequest(BaseModel):
    name: str
    grade: int
    household_income: float
    subjects: Dict[str, int]  # Key: Subject Name, Value: Mark %
    interests: List[str]