"""
utils/validators.py
Input validation logic for incoming student payload data.
"""

def validate_student_request(data):
    """
    Validates payload against MyPath schema.
    Returns tuple: (is_valid: bool, error_message: str | None)
    """
    if not isinstance(data, dict):
        return False, "Payload must be a valid JSON object"

    required_fields = ["name", "grade", "household_income", "subjects", "interests"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: '{field}'"

    if not isinstance(data.get("subjects"), dict) or len(data["subjects"]) == 0:
        return False, "At least one subject with a valid mark is required"

    if not isinstance(data.get("interests"), list):
        return False, "Field 'interests' must be a list of strings"

    return True, None