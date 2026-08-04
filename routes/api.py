"""
API Routes: Entry points for student profile evaluation and career guidance generation.
"""

import json
import os
from flask import Blueprint, request, jsonify

from engines.aps_engine import APSEngine
from engines.funding_engine import FundingEngine
from engines.career_match_engine import CareerMatchEngine
from services.ai_engine import AIEngine

api_bp = Blueprint("api", __name__, url_prefix="/api")

# Load static reference datasets
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_json_data(filename: str):
    """Safely loads JSON data files, returning an empty list if file is missing or invalid."""
    file_path = os.path.join(DATA_DIR, filename)
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"[Warning] Failed to read dataset {filename}: {e}")
    return []


@api_bp.route("/evaluate", methods=["POST"])
@api_bp.route("/recommend", methods=["POST"])  # Legacy route alias to prevent 404s
def evaluate_student():
    """
    Evaluates student details, calculates non-LO APS, evaluates NSFAS threshold eligibility,
    pre-filters careers by interest, and generates AI guidance schema.
    """
    try:
        payload = request.get_json(silent=True) or {}

        # Parse & sanitize inputs
        subjects = payload.get("subjects", {})
        user_interests = payload.get("user_interests") or payload.get("interests") or []
        
        try:
            household_income = float(payload.get("household_income", 0.0))
        except (ValueError, TypeError):
            household_income = 0.0

        has_disability = bool(payload.get("has_disability", False))
        is_sassa_recipient = bool(payload.get("is_sassa_recipient", False))
        location = payload.get("location", "Any")

        # Spec 1: Calculate APS excluding LO deterministically
        aps_result = APSEngine.calculate_aps(subjects)

        # Spec 3: Evaluate Funding & Household Income against R350,000 threshold limit
        funding_result = FundingEngine.evaluate_eligibility(
            household_income=household_income,
            has_disability=has_disability,
            is_sassa_recipient=is_sassa_recipient
        )

        # Load local datasets safely
        careers_db = load_json_data("careers.json")
        bursaries_db = load_json_data("bursaries.json")
        universities_db = load_json_data("universities.json")
        tvet_db = load_json_data("tvet.json")

        # Spec 2: Pre-filter top careers via user_interests prior to AI prompt injection
        filtered_careers = CareerMatchEngine.filter_by_interests(careers_db, user_interests)

        # Filter universities, TVET, and bursaries based on calculated APS score
        student_aps = aps_result.get("total_aps", 0)
        
        filtered_bursaries = [
            b for b in bursaries_db 
            if b.get("min_aps", 0) <= student_aps
        ]
        filtered_universities = [
            u for u in universities_db 
            if u.get("min_aps", 0) <= student_aps
        ]
        filtered_tvet = [
            t for t in tvet_db 
            if t.get("min_aps", 0) <= student_aps
        ]

        # Container for student profile configuration
        student_profile = {
            "user_interests": user_interests,
            "household_income": household_income,
            "location": location,
            "has_disability": has_disability,
            "is_sassa_recipient": is_sassa_recipient
        }

        # Specs 4-8: Generate AI Counselor Brief, Top 3 Careers, Universities, TVETs, and Bursaries
        ai_engine = AIEngine()
        guidance_response = ai_engine.generate_guidance(
            student_profile=student_profile,
            aps_result=aps_result,
            funding_result=funding_result,
            filtered_careers=filtered_careers,
            filtered_bursaries=filtered_bursaries,
            filtered_universities=filtered_universities,
            filtered_tvet=filtered_tvet
        )

        # Convert Pydantic model to dictionary output
        guidance_dict = guidance_response.model_dump() if hasattr(guidance_response, 'model_dump') else guidance_response.dict()

        return jsonify({
            "status": "success",
            "metrics": {
                "aps": aps_result,
                "funding": funding_result
            },
            "guidance": guidance_dict
        }), 200

    except Exception as e:
        print(f"[API Error]: {e}")
        return jsonify({
            "status": "error",
            "message": "An internal error occurred while processing student guidance.",
            "details": str(e)
        }), 500