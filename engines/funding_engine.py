"""
Funding Engine: Evaluates student financial eligibility and funding pathways.
Rule: Household income evaluated against the R350,000 NSFAS threshold limit.
"""

from typing import Dict, Any

NSFAS_THRESHOLD = 350000.0  # R350,000 threshold for South African NSFAS funding
NSFAS_DISABILITY_THRESHOLD = 600000.0  # R600,000 threshold for students with disabilities

class FundingEngine:
    @staticmethod
    def evaluate_eligibility(
        household_income: float, 
        has_disability: bool = False, 
        is_sassa_recipient: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluates NSFAS and alternative funding eligibility based on household income.
        
        Args:
            household_income: Annual household income in ZAR (R).
            has_disability: Boolean flag indicating disability status.
            is_sassa_recipient: Boolean flag indicating if household receives SASSA grants.
            
        Returns:
            Dict containing NSFAS status, income threshold breakdown, and funding recommendations.
        """
        threshold = NSFAS_DISABILITY_THRESHOLD if has_disability else NSFAS_THRESHOLD
        
        # SASSA grant recipients automatically qualify for NSFAS
        if is_sassa_recipient:
            nsfas_eligible = True
            funding_tier = "NSFAS Direct (SASSA Recipient)"
            reasoning = "Automatic qualification due to registered SASSA grant recipient status."
        elif household_income <= threshold:
            nsfas_eligible = True
            funding_tier = "NSFAS Eligible"
            reasoning = f"Annual household income (R{household_income:,.2f}) is within the R{threshold:,.2f} NSFAS threshold limit."
        else:
            nsfas_eligible = False
            funding_tier = "Missing Middle / Commercial & Corporate Bursaries"
            reasoning = f"Annual household income (R{household_income:,.2f}) exceeds the R{threshold:,.2f} NSFAS threshold limit."

        return {
            "household_income": household_income,
            "nsfas_threshold_limit": threshold,
            "nsfas_eligible": nsfas_eligible,
            "funding_tier": funding_tier,
            "reasoning": reasoning,
            "funding_pathways": FundingEngine._determine_pathways(nsfas_eligible, household_income)
        }

    @staticmethod
    def _determine_pathways(nsfas_eligible: bool, household_income: float) -> list:
        """Helper to return suggested funding application avenues."""
        if nsfas_eligible:
            return [
                "NSFAS (National Student Financial Aid Scheme)",
                "University Merit Bursaries",
                "Sector Education and Training Authority (SETA) Grants"
            ]
        elif household_income <= 600000.0:
            return [
                "IsuLami / Missing Middle Student Loans",
                "Corporate/Industry Sponsored Bursaries",
                "Bank Student Loans (Requires Guarantor)",
                "Work-Study University Programs"
            ]
        else:
            return [
                "Corporate Graduate / Cadetship Bursaries",
                "Commercial Bank Student Loans",
                "Private Sector Merit Scholarships"
            ]