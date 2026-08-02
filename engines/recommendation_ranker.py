"""
engines/recommendation_ranker.py
Ranks career recommendations using deterministic scoring.
Architecture Rule: Python handles deterministic scoring and ranking.
"""

class RecommendationRanker:
    def __init__(self):
        # Comprehensive South African Career Knowledge Pool[cite: 1]
        self.career_pool = [
            # HEALTH & MEDICAL SCIENCES
            {
                "title": "Medical Practitioner / Doctor (MBChB)",
                "category": "Healthcare",
                "min_aps": 35,
                "keywords": ["health", "medicine", "doctor", "hospital", "patient care", "biology", "anatomy", "clinical"]
            },
            {
                "title": "Nursing Science Specialist",
                "category": "Healthcare",
                "min_aps": 28,
                "keywords": ["health", "medicine", "nursing", "patient care", "hospital", "healthcare", "biology"]
            },
            {
                "title": "Pharmacist",
                "category": "Healthcare & Sciences",
                "min_aps": 32,
                "keywords": ["health", "medicine", "pharmacy", "chemistry", "drugs", "patient care", "biology"]
            },
            {
                "title": "Biomedical Engineer",
                "category": "Healthcare & Technology",
                "min_aps": 33,
                "keywords": ["health", "medicine", "technology", "engineering", "devices", "biology", "coding"]
            },

            # TECHNOLOGY & COMPUTING
            {
                "title": "Software Engineer / Cloud Developer",
                "category": "Technology",
                "min_aps": 28,
                "keywords": ["coding", "technology", "software", "computers", "programming", "devops", "cloud", "problem-solving"]
            },
            {
                "title": "Data Scientist / AI Specialist",
                "category": "Technology & Data",
                "min_aps": 32,
                "keywords": ["data", "analytics", "math", "statistics", "coding", "ai", "technology", "problem-solving"]
            },

            # BUSINESS, FINANCE & LAW
            {
                "title": "Chartered Accountant (CA)",
                "category": "Finance & Business",
                "min_aps": 34,
                "keywords": ["finance", "accounting", "business", "money", "economics", "math", "auditing"]
            },
            {
                "title": "Legal Advisor / Attorney",
                "category": "Law & Humanities",
                "min_aps": 30,
                "keywords": ["law", "legal", "justice", "writing", "debate", "court", "policy", "humanities"]
            },

            # ENGINEERING & BUILT ENVIRONMENT
            {
                "title": "Civil / Structural Engineer",
                "category": "Engineering",
                "min_aps": 32,
                "keywords": ["building", "construction", "engineering", "infrastructure", "math", "physics", "design"]
            }
        ]

    def rank(self, student_data: dict, aps_excl_lo: int) -> list:
        """
        Ranks potential career paths deterministically based on student interests and APS (excl. LO)[cite: 1].
        """
        raw_interests = student_data.get("interests", [])
        
        # Standardize interest inputs (list or comma-separated string)
        if isinstance(raw_interests, str):
            user_interests = [i.strip().lower() for i in raw_interests.split(",") if i.strip()]
        elif isinstance(raw_interests, list):
            user_interests = [str(i).strip().lower() for i in raw_interests if str(i).strip()]
        else:
            user_interests = []

        scored_careers = []

        for career in self.career_pool:
            interest_match_count = 0
            
            # Check how many user interests match the career's keyword tag bank
            for interest in user_interests:
                for keyword in career["keywords"]:
                    if keyword in interest or interest in keyword:
                        interest_match_count += 1
                        break  # Match found for this interest item

            # If user specified interests, penalize careers with ZERO interest alignment
            if user_interests and interest_match_count == 0:
                continue

            # Deterministic fit score calculation[cite: 1]
            base_score = 40
            
            # Academic APS evaluation
            if aps_excl_lo >= career["min_aps"]:
                aps_score = 30
            else:
                aps_score = max(0, (aps_excl_lo / career["min_aps"]) * 20)

            # Interest match weight (30 points maximum)
            interest_score = min(interest_match_count * 15, 30)

            final_fit_score = min(round(base_score + aps_score + interest_score), 99)

            scored_careers.append({
                "title": career["title"],
                "category": career["category"],
                "min_aps": career["min_aps"],
                "fit_score": final_fit_score
            })

        # Sort descending by calculated fit score
        scored_careers.sort(key=lambda x: x["fit_score"], reverse=True)

        # Fallback if no specific keyword match was found
        if not scored_careers:
            return [{
                "title": "General Bachelor of Science / Health Sciences Entry",
                "category": "General Pathways",
                "min_aps": 26,
                "fit_score": 60
            }]

        return scored_careers[:4]  # Return top 4 tailored matches