import json, os
from config import Config
from engines.funding_engine import FundingEngine

class OpportunityService:
    def __init__(self):
        self.funding_engine = FundingEngine()

    def _load_json(self, filename: str) -> list:
        filepath = os.path.join(Config.DATA_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def get_funding_matches(self, aps_score: int, household_income: float) -> list:
        bursaries = self._load_json("bursaries.json")
        return self.funding_engine.find_funding_options(aps_score, household_income, bursaries)

    def get_learnerships(self) -> list:
        return self._load_json("learnerships.json")

    def get_other_opportunities(self) -> list:
        return self._load_json("opportunities.json")