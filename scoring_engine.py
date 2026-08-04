class ScoringEngine:
    def calculate_fit_score(self, student_subjects: dict, student_interests: list, career: dict) -> float:
        """
        Calculates a deterministic career compatibility fit score between 0.0 and 100.0.
        """
        score = 50.0 # Base score

        # Subject alignment calculation
        req_marks = career.get("min_subject_marks", {})
        if req_marks:
            marks_diff = []
            for subj, min_mark in req_marks.items():
                actual = student_subjects.get(subj, 0)
                marks_diff.append(actual - min_mark)
            avg_diff = sum(marks_diff) / len(marks_diff)
            score += min(25.0, max(-20.0, avg_diff * 0.5))

        # Interest alignment calculation
        student_ints = set(i.lower() for i in student_interests)
        career_tags = set(t.lower() for t in career.get("interest_tags", []))
        if career_tags:
            overlap = student_ints.intersection(career_tags)
            interest_ratio = len(overlap) / len(career_tags)
            score += interest_ratio * 25.0

        return round(min(100.0, max(0.0, score)), 2)