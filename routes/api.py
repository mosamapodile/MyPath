from flask import Blueprint, request, jsonify
from utils.validators import validate_student_request # or Pydantic ValidationError
from services.recommendation_engine import RecommendationEngine

api_bp = Blueprint('api', __name__)
recommendation_engine = RecommendationEngine()

@api_bp.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    
    # Check if JSON exists
    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400

    # Ensure required fields exist in payload
    required_fields = ["name", "grade", "household_income", "subjects", "interests"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Ensure subjects is a valid dictionary and not empty
    if not isinstance(data.get("subjects"), dict) or len(data["subjects"]) == 0:
        return jsonify({"error": "At least one valid subject with a mark is required"}), 400

    try:
        # Process through deterministic business logic and AI layer
        result = recommendation_engine.generate(data)
        return jsonify(result), 200

    except Exception as e:
        print(f"[API ERROR]: {str(e)}")
        return jsonify({"error": str(e)}), 500