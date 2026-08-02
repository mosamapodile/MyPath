class FundingEngine:
    def find_funding_options(self, aps_score: int, household_income: float, bursaries: list) -> list:
        matched_funding = []
        for bursary in bursaries:
            min_aps = bursary.get("min_aps", 0)
            max_income = bursary.get("max_household_income", float("inf"))

            if aps_score >= min_aps and household_income <= max_income:
                matched_funding.append(bursary)
                
        return matched_funding