import json, os
from config import Config
from engines.eligibility_engine import EligibilityEngine

class UniversityService:
    def __init__(self):
        self.eligibility_engine = EligibilityEngine()

    def _load_json(self, filename: str) -> list:
        filepath = os.path.join(Config.DATA_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_eligible_universities(self, aps_score: int, subjects: dict) -> list:
        programmes = self._load_json("universities.json")
        return self.eligibility_engine.check_eligibility(aps_score, subjects, programmes)

    def get_eligible_tvet(self, aps_score: int, subjects: dict) -> list:
        programmes = self._load_json("tvet.json")
        return self.eligibility_engine.check_eligibility(aps_score, subjects, programmes)