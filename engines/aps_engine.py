"""
APS Engine: Handles deterministic calculation of the Admission Point Score (APS).
Rule: Life Orientation (LO) is strictly EXCLUDED from the APS calculation.
The score is the sum of the top 6 non-LO subjects.
"""

from typing import Dict, List, Any

# Standard NSC Level to APS Point Mapping
NSC_SCALE = {
    7: (80, 100),
    6: (70, 79),
    5: (60, 69),
    4: (50, 59),
    3: (40, 49),
    2: (30, 39),
    1: (0, 29)
}

LO_ALIASES = {
    "life orientation",
    "lo",
    "life-orientation",
    "life_orientation"
}

class APSEngine:
    @staticmethod
    def percentage_to_aps(percentage: float) -> int:
        """Convert a percentage score to an NSC APS point scale (1-7)."""
        pct = round(percentage)
        if pct >= 80:
            return 7
        elif pct >= 70:
            return 6
        elif pct >= 60:
            return 5
        elif pct >= 50:
            return 4
        elif pct >= 40:
            return 3
        elif pct >= 30:
            return 2
        else:
            return 1

    @classmethod
    def calculate_aps(cls, subjects: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates APS score deterministically.
        
        Args:
            subjects: Dictionary mapping subject names to percentages (e.g. {"Mathematics": 75, "Life Orientation": 85})
            
        Returns:
            Dict containing total_aps, breakdown per subject, and excluded subjects.
        """
        valid_subject_scores = []
        excluded_subjects = []

        for subject_name, score in subjects.items():
            normalized_name = subject_name.strip().lower()
            
            # Rule 1: Strictly exclude Life Orientation
            if normalized_name in LO_ALIASES:
                excluded_subjects.append({
                    "subject": subject_name,
                    "score": score,
                    "reason": "Life Orientation (LO) excluded from APS total"
                })
                continue

            # Convert percentage score to APS point if score > 7 (meaning it's given as percentage)
            aps_points = score if score <= 7 else cls.percentage_to_aps(score)
            valid_subject_scores.append((subject_name, aps_points, score))

        # Sort non-LO subjects by APS points descending
        valid_subject_scores.sort(key=lambda x: x[1], reverse=True)

        # Rule 1: Sum top 6 non-LO subjects
        top_6 = valid_subject_scores[:6]
        overflow = valid_subject_scores[6:]

        total_aps = sum(item[1] for item in top_6)

        return {
            "total_aps": total_aps,
            "top_6_subjects": [
                {"subject": item[0], "aps_points": item[1], "percentage": item[2]}
                for item in top_6
            ],
            "excluded_subjects": excluded_subjects,
            "additional_subjects": [
                {"subject": item[0], "aps_points": item[1], "percentage": item[2]}
                for item in overflow
            ]
        }