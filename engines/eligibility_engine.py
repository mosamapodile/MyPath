class EligibilityEngine:
    def check_eligibility(self, aps_score: int, student_subjects: dict, programmes: list) -> list:
        eligible = []
        for prog in programmes:
            if aps_score < prog.get("min_aps", 0):
                continue

            req_subjects = prog.get("required_subjects", {})
            meets_requirements = True
            for subj, min_mark in req_subjects.items():
                if student_subjects.get(subj, 0) < min_mark:
                    meets_requirements = False
                    break

            if meets_requirements:
                eligible.append(prog)
                
        return eligible