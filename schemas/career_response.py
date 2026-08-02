from pydantic import BaseModel
from typing import List, Dict, Any

class CareerResponseSchema(BaseModel):
    student_name: str
    aps_score: int
    recommended_careers: List[Dict[str, Any]]
    eligible_universities: List[Dict[str, Any]]
    eligible_tvet: List[Dict[str, Any]]
    funding_matches: List[Dict[str, Any]]
    learnerships: List[Dict[str, Any]]
    ai_guidance: str