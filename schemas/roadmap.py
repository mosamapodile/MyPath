from pydantic import BaseModel
from typing import List

class RoadmapSchema(BaseModel):
    steps: List[str]
    estimated_years: int