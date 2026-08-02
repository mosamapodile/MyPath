"""
engines/aps_engine.py
Calculates NSC Admission Point Score (APS) excluding Life Orientation.
"""

class APSEngine:
    @staticmethod
    def convert_percentage_to_aps(mark: float) -> int:
        if mark >= 80:
            return 7
        elif mark >= 70:
            return 6
        elif mark >= 60:
            return 5
        elif mark >= 50:
            return 4
        elif mark >= 40:
            return 3
        elif mark >= 30:
            return 2
        else:
            return 1

    @classmethod
    def calculate_aps(cls, subjects: dict) -> int:
        valid_scores = []
        for subject, mark in subjects.items():
            if subject.strip().lower() in ["life orientation", "lo", "life-orientation"]:
                continue
            try:
                numeric_mark = float(mark)
                valid_scores.append(cls.convert_percentage_to_aps(numeric_mark))
            except (ValueError, TypeError):
                continue

        valid_scores.sort(reverse=True)
        return sum(valid_scores[:6])