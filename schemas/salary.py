from pydantic import BaseModel

class SalarySchema(BaseModel):
    entry_level_zar: float
    mid_level_zar: float
    senior_level_zar: float