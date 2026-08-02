from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class StudentModel:
    name: str
    grade: int
    subjects: Dict[str, int]
    interests: List[str]
    household_income: float = 0.0
    aps_score: int = 0