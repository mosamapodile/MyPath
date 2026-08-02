from pydantic import BaseModel
from typing import Dict, Optional

class UniversitySchema(BaseModel):
    id: str
    institution: str
    programme: str
    min_aps: int
    required_subjects: Optional[Dict[str, int]] = {}