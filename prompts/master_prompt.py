"""
Master Prompt: Formats inputs and system instructions for the AI Counselor.
Ensures generation matches the exact response schema and project specifications.
"""

from typing import Dict, Any, List
import json


class MasterPrompt:
    @staticmethod
    def build_prompt(
        student_profile: Dict[str, Any],
        aps_result: Dict[str, Any],
        funding_result: Dict[str, Any],
        filtered_careers: List[Dict[str, Any]],
        filtered_bursaries: List[Dict[str, Any]],
        filtered_universities: List[Dict[str, Any]],
        filtered_tvet: List[Dict[str, Any]]
    ) -> str:
        """
        Builds the complete master prompt string to send to the AI model.
        """
        
        prompt = f"""
You are an expert South African Higher Education and Career Guidance Counselor AI.
Analyze the following student profile, calculated APS metrics, and pre-filtered options to generate a personalized career roadmap.

==================================================
1. STUDENT PROFILE & PREFERENCES
==================================================
- Target Field / User Interests: {json.dumps(student_profile.get('user_interests', []))}
- Annual Household Income: ZAR {student_profile.get('household_income', 0):,.2f}
- Preferred Location / Region: {student_profile.get('location', 'Any')}

==================================================
2. DETERMINISTIC APS & ELIGIBILITY METRICS
==================================================
- Total APS Score (Strictly Top 6 Non-LO Subjects): {aps_result.get('total_aps')}
- Excluded Subjects from APS: {json.dumps(aps_result.get('excluded_subjects', []))}
- Top 6 Subjects Used: {json.dumps(aps_result.get('top_6_subjects', []))}
- NSFAS Funding Tier: {funding_result.get('funding_tier')}
- NSFAS Eligible: {funding_result.get('nsfas_eligible')} (Threshold limit: R350,000)

==================================================
3. PRE-FILTERED DATASETS
==================================================
- Filtered Interest-Based Careers: {json.dumps(filtered_careers[:10])}
- Eligible Universities & Courses: {json.dumps(filtered_universities[:10])}
- Eligible TVET Colleges & Courses: {json.dumps(filtered_tvet[:10])}
- Eligible Bursaries: {json.dumps(filtered_bursaries[:10])}

==================================================
STRICT INSTRUCTIONS & DELIVERABLES
==================================================
Generate a JSON object strictly matching the following criteria:

1. counselor_brief: 
   Write an intimate, high-impact narrative paragraph acting as an AI Counselor Brief & Roadmap. Address the student warmly and directly, summarizing their path forward based on their APS of {aps_result.get('total_aps')} and their specific interests.

2. top_careers: 
   Provide EXACTLY 3 top career options selected from the filtered careers list. Include:
   - career_title
   - fit_reasoning (Detailed explanation of alignment with interests and academic profile)
   - skill_targets (List of top technical/soft skills needed)

3. top_universities: 
   Provide EXACTLY 3 university recommendations. Include:
   - university_name
   - degree_or_diploma (Exact degree or diploma name)
   - application_fee (Exact fee string, e.g., 'R100' or 'Free (Online)')

4. top_tvet_courses: 
   Provide EXACTLY 3 TVET college recommendations. Include:
   - tvet_college
   - course_name
   - nqf_level (Explicit designation, e.g., 'NQF Level 4' or 'NQF Level 6')

5. top_bursaries: 
   Provide EXACTLY 3 eligible bursaries filtered by the student's APS score ({aps_result.get('total_aps')}) and interest alignment. Include:
   - bursary_name
   - eligibility_notes (Mention APS suitability and interest match)
   - coverage_details (What the bursary covers)

Respond strictly in valid JSON matching the target schema.
"""
        return prompt