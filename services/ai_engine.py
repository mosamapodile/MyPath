"""
AI Engine: Handles interaction with OpenAI GPT models using Structured Outputs.
Converts MasterPrompt payloads into validated CareerGuidanceResponse objects.
"""

import json
import os
from typing import Dict, Any, Optional
from openai import OpenAI

from prompts.master_prompt import MasterPrompt
from schemas.career_response import CareerGuidanceResponse


class AIEngine:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def generate_guidance(
        self,
        student_profile: Dict[str, Any],
        aps_result: Dict[str, Any],
        funding_result: Dict[str, Any],
        filtered_careers: list,
        filtered_bursaries: list,
        filtered_universities: list,
        filtered_tvet: list
    ) -> CareerGuidanceResponse:
        """
        Generates structured career guidance narrative, university/TVET recommendations, 
        and bursary pairings using GPT-4o.
        """
        # Construct the detailed prompt
        prompt_content = MasterPrompt.build_prompt(
            student_profile=student_profile,
            aps_result=aps_result,
            funding_result=funding_result,
            filtered_careers=filtered_careers,
            filtered_bursaries=filtered_bursaries,
            filtered_universities=filtered_universities,
            filtered_tvet=filtered_tvet
        )

        if not self.client:
            # Mock / Fallback response for offline or unauthenticated testing environments
            return self._fallback_guidance(student_profile, aps_result)

        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a specialized South African career guidance AI counselor that strictly adheres to schema formatting."
                    },
                    {
                        "role": "user",
                        "content": prompt_content
                    }
                ],
                response_format=CareerGuidanceResponse,
                temperature=0.7
            )
            return response.choices[0].message.parsed

        except Exception as e:
            # Fallback to standard json completion if beta parsing encounters issues
            return self._raw_json_fallback(prompt_content)

    def _raw_json_fallback(self, prompt_content: str) -> CareerGuidanceResponse:
        """Fallback handling using standard JSON parsing mode."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Return only valid JSON matching the requested schema."
                },
                {"role": "user", "content": prompt_content}
            ],
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return CareerGuidanceResponse(**data)

    def _fallback_guidance(self, student_profile: Dict[str, Any], aps_result: Dict[str, Any]) -> CareerGuidanceResponse:
        """Fallback payload when API key is not present."""
        aps = aps_result.get("total_aps", 0)
        interests = ", ".join(student_profile.get("user_interests", ["Tech"]))
        
        return CareerGuidanceResponse(
            counselor_brief=(
                f"Based on your calculated non-LO APS score of {aps} and interest in {interests}, "
                "you possess a strong academic foundation for technical degree and diploma pathways. "
                "Focus on solidifying core practical skill sets while submitting university and bursary applications early."
            ),
            top_careers=[
                {"career_title": "Software Developer", "fit_reasoning": "High alignment with technical interest area.", "skill_targets": ["Python", "Git", "SQL"]},
                {"career_title": "Systems Analyst", "fit_reasoning": "Matches analytical problem-solving skills.", "skill_targets": ["Requirements Analysis", "UML", "Databases"]},
                {"career_title": "Network Engineer", "fit_reasoning": "Strong potential fit based on math and physics metrics.", "skill_targets": ["Cisco Routing", "Linux", "TCP/IP"]}
            ],
            top_universities=[
                {"university_name": "University of the Witwatersrand", "degree_or_diploma": "BSc Computer Science", "application_fee": "R100"},
                {"university_name": "University of Johannesburg", "degree_or_diploma": "Diploma in Information Technology", "application_fee": "R200"},
                {"university_name": "University of Pretoria", "degree_or_diploma": "BIT Information Systems", "application_fee": "R300"}
            ],
            top_tvet_courses=[
                {"tvet_college": "Central Johannesburg TVET College", "course_name": "National Diploma in Information Technology", "nqf_level": "NQF Level 6"},
                {"tvet_college": "False Bay TVET College", "course_name": "NCV Information Technology and Computer Science", "nqf_level": "NQF Level 4"},
                {"tvet_college": "Tshwane South TVET College", "course_name": "Higher Certificate in Software Development", "nqf_level": "NQF Level 5"}
            ],
            top_bursaries=[
                {"bursary_name": "NSFAS", "eligibility_notes": "Eligible based on household income limits.", "coverage_details": "Tuition, Accommodation, Books, Living Allowance"},
                {"bursary_name": "ISFAP Bursary", "eligibility_notes": "Matches STEM focus area and APS score.", "coverage_details": "Full tuition, accommodation, and stipend"},
                {"bursary_name": "SITA Bursary Scheme", "eligibility_notes": "Aligned with ICT study interest.", "coverage_details": "Tuition fees and prescribed learning materials"}
            ]
        )