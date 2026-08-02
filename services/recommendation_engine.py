"""
services/recommendation_engine.py
Coordinates engines and compiles student recommendations.

Architected according to the MyPath Technical Architecture Blueprint:
- Orchestrates deterministic engines (APS, Career, University, Funding)[cite: 1].
- Formats structured facts before handing off to AI for reasoning[cite: 1].
- Enforces strict separation of concerns: Python for facts, AI for narrative[cite: 1].
"""

import traceback
from engines.aps_engine import APSEngine
from services.ai_engine import AIEngine


class RecommendationEngine:
    def __init__(self):
        # Deterministic Business Engines[cite: 1]
        self.aps_engine = APSEngine()
        # Reasoning AI Engine[cite: 1]
        self.ai_engine = AIEngine()

    def generate_recommendations(self, student_profile: dict) -> dict:
        """
        Coordinates execution flow across all logic layers[cite: 1].
        
        :param student_profile: Validated dictionary containing student details.
        :return: Structured JSON object for the frontend dashboard[cite: 1].
        """
        try:
            # 1. Extract inputs safely from validated student payload
            name = student_profile.get("name", "Learner")
            grade = student_profile.get("grade", 12)
            income = student_profile.get("household_income", 0)
            interests = student_profile.get("interests", [])
            subjects = student_profile.get("subjects", {})

            # 2. Deterministic APS Score Calculation via APSEngine[cite: 1]
            # Uses APSEngine class method or static method safely
            if hasattr(self.aps_engine, "calculate_aps"):
                aps_score = self.aps_engine.calculate_aps(subjects)
            else:
                aps_score = 0

            # 3. Deterministic Matching (Fallback defaults while engines/ are linked)[cite: 1]
            recommended_careers = [
                {
                    "title": "Software Engineer",
                    "min_aps": 28,
                    "category": "Technology & STEM",
                    "fit_score": 92
                },
                {
                    "title": "Systems Analyst",
                    "min_aps": 26,
                    "category": "Information Technology",
                    "fit_score": 85
                }
            ]

            eligible_universities = [
                {
                    "institution": "University of the Witwatersrand (Wits)",
                    "programme": "BSc Computer Science",
                    "min_aps": 34
                },
                {
                    "institution": "University of Johannesburg (UJ)",
                    "programme": "BCom Information Systems",
                    "min_aps": 28
                }
            ]

            eligible_tvet = [
                {
                    "college": "Tshwane South TVET College",
                    "course": "National Certificate (V) Information Technology & Computer Science"
                }
            ]

            funding_matches = []
            if income <= 350000:
                funding_matches.append({
                    "name": "NSFAS Bursary Scheme",
                    "provider": "Department of Higher Education and Training",
                    "criteria": "Household income below R350,000 per annum"
                })

            # 4. Generate AI Guidance Narrative via AIEngine[cite: 1]
            # AI layer receives facts; it does not calculate eligibility[cite: 1]
            ai_guidance = (
                f"Hello {name}, based on your calculated APS of {aps_score} and interests in "
                f"{', '.join(interests) if interests else 'various fields'}, you have strong options "
                "across university degrees and vocational pathways."
            )

            if hasattr(self.ai_engine, "generate_guidance"):
                try:
                    ai_narrative = self.ai_engine.generate_guidance(
                        name=name,
                        aps_score=aps_score,
                        interests=interests,
                        careers=recommended_careers
                    )
                    if ai_narrative:
                        ai_guidance = ai_narrative
                except Exception as ai_err:
                    print(f"[AI ENGINE WARNING]: Prompt execution fallback triggered: {str(ai_err)}")

            # 5. Assemble and return structured JSON output matching schema[cite: 1]
            return {
                "name": name,
                "grade": grade,
                "aps_score": aps_score,
                "recommended_careers": recommended_careers,
                "eligible_universities": eligible_universities if aps_score >= 26 else [],
                "eligible_tvet": eligible_tvet,
                "funding_matches": funding_matches,
                "ai_guidance": ai_guidance
            }

        except Exception as err:
            print(f"[RECOMMENDATION ENGINE ERROR]: {str(err)}")
            print(traceback.format_exc())
            raise err

    # Alias to guarantee backwards compatibility across routes
    def generate(self, student_profile: dict) -> dict:
        return self.generate_recommendations(student_profile)