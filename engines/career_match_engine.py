"""
engines/career_match_engine.py
Matches careers based on student interests, subjects, and performance.

Architected according to the MyPath Technical Architecture Blueprint:
- Pure deterministic business logic[cite: 1].
"""

class CareerMatchEngine:
    """
    Ranks and matches career paths against student interests and academic inputs.
    """

    CAREER_DATABASE = [
        {
            "title": "Software Engineer",
            "category": "Technology & STEM",
            "min_aps": 28,
            "keywords": ["software", "coding", "programming", "technology", "computers", "math", "maths", "tech", "development"]
        },
        {
            "title": "Data Analyst / Scientist",
            "category": "Technology & Analytics",
            "min_aps": 30,
            "keywords": ["data", "statistics", "math", "maths", "analytics", "numbers", "technology", "research"]
        },
        {
            "title": "Civil Engineer",
            "category": "Engineering & Construction",
            "min_aps": 32,
            "keywords": ["engineering", "building", "physics", "math", "maths", "construction", "design"]
        },
        {
            "title": "Accountant / Auditor",
            "category": "Finance & Commerce",
            "min_aps": 28,
            "keywords": ["accounting", "finance", "business", "math", "maths", "money", "auditing", "numbers"]
        },
        {
            "title": "Biomedical Specialist",
            "category": "Health & Life Sciences",
            "min_aps": 30,
            "keywords": ["biology", "science", "medicine", "health", "life sciences", "research", "lab"]
        }
    ]

    def match_careers(self, interests: list, subjects: dict, aps_score: int) -> list:
        """
        Calculates career match confidence and returns ranked list of careers.
        """
        matched_results = []
        
        # Normalize input interests and subject keys
        normalized_interests = [i.strip().lower() for i in interests]
        normalized_subjects = [s.strip().lower() for s in subjects.keys()]
        combined_user_tokens = set(normalized_interests + normalized_subjects)

        for career in self.CAREER_DATABASE:
            # 1. Base check: APS eligibility threshold
            if aps_score < career["min_aps"] - 4:
                # Skip careers where APS is drastically below requirement
                continue

            # 2. Interest and keyword overlap score
            keyword_matches = 0
            for kw in career["keywords"]:
                for token in combined_user_tokens:
                    if kw in token or token in kw:
                        keyword_matches += 1
                        break

            # 3. Calculate fit percentage score
            base_fit = 60  # Default baseline match
            calculated_fit = base_fit + (keyword_matches * 12)
            
            # Boost fit score if student exceeds min APS requirement
            if aps_score >= career["min_aps"]:
                calculated_fit += 10
            
            # Clamp between 50% and 98%
            final_fit_score = min(98, max(50, calculated_fit))

            matched_results.append({
                "title": career["title"],
                "category": career["category"],
                "min_aps": career["min_aps"],
                "fit_score": final_fit_score
            })

        # Sort descending by fit score
        matched_results.sort(key=lambda x: x["fit_score"], reverse=True)

        return matched_results if matched_results else [
            {
                "title": "General Bachelor of Science / Commerce Path",
                "category": "General Studies",
                "min_aps": 26,
                "fit_score": 75
            }
        ]