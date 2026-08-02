"""
services/student_profile.py
Builds and enriches the student profile object.
"""
from engines.aps_engine import calculate_aps

def build_student_profile(raw_data: dict) -> dict:
    subjects = raw_data.get("subjects", {})
    
    # Calculate APS score standardizing logic
    aps_score = calculate_aps(subjects)
    
    profile = {
        "name": raw_data.get("name", ""),
        "grade": raw_data.get("grade", 12),
        "household_income": raw_data.get("household_income", 0),
        "interests": raw_data.get("interests", []),
        "subjects": subjects,
        "aps_score": aps_score
    }
    
    return profile