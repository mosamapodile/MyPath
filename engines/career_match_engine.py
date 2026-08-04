"""
Career Match Engine: Handles interest-based pre-filtering and domain matching.
Rule: Careers are filtered through user_interests PRIOR to AI prompt injection.
"""

from typing import List, Dict, Any

class CareerMatchEngine:
    @staticmethod
    def filter_by_interests(
        careers_db: List[Dict[str, Any]], 
        user_interests: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Filters the full list of available careers based on user_interests before AI scoring.
        
        Args:
            careers_db: Full list of career dictionaries from dataset/database.
            user_interests: List of interest strings provided by the user (e.g. ['Software', 'Robotics']).
            
        Returns:
            Filtered list of career dictionaries matching interest criteria.
        """
        if not user_interests:
            return careers_db

        normalized_interests = [i.strip().lower() for i in user_interests]
        filtered_careers = []

        for career in careers_db:
            career_title = career.get("title", "").lower()
            career_field = career.get("field", "").lower()
            career_tags = [tag.lower() for tag in career.get("tags", [])]
            career_desc = career.get("description", "").lower()

            # Match against title, field, tags, or description
            is_match = False
            for interest in normalized_interests:
                if (
                    interest in career_title
                    or interest in career_field
                    or any(interest in tag for tag in career_tags)
                    or interest in career_desc
                ):
                    is_match = True
                    break

            if is_match:
                filtered_careers.append(career)

        # Fallback: If strict filtering returns zero results, return all careers to avoid complete match failure
        return filtered_careers if filtered_careers else careers_db