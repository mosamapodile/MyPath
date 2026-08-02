from pydantic import BaseModel
from typing import List, Optional

class CareerPathSchema(BaseModel):
    id: str
    title: str
    category: str
    fit_score: float
    automation_risk: Optional[str] = "Low"
    industry_growth: Optional[str] = "Moderate"