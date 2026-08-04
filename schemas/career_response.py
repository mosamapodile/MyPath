"""
Pydantic Schemas for AI Counselor Output.
Defines structured response format for gpt-4o / AI engine generation.
"""

from typing import List
from pydantic import BaseModel, Field


class CareerItem(BaseModel):
    career_title: str = Field(description="Title of the career")
    fit_reasoning: str = Field(description="Detailed explanation of why this career fits the student's profile")
    skill_targets: List[str] = Field(description="List of key technical and soft skills targeted for this role")


class UniversityItem(BaseModel):
    university_name: str = Field(description="Name of the university (e.g. Wits University, UCT)")
    degree_or_diploma: str = Field(description="Exact degree or diploma name")
    application_fee: str = Field(description="Exact application fee string (e.g. 'R100', 'Free (Online)')")


class TVETItem(BaseModel):
    tvet_college: str = Field(description="Name of the TVET College (e.g. False Bay TVET College)")
    course_name: str = Field(description="Name of the course or programme")
    nqf_level: str = Field(description="Explicit NQF Level designation (e.g. 'NQF 4', 'NQF 6')")


class BursaryItem(BaseModel):
    bursary_name: str = Field(description="Name of the bursary or funding body")
    eligibility_notes: str = Field(description="Notes on APS requirement and interest alignment")
    coverage_details: str = Field(description="Details of what the bursary covers (e.g. Tuition, Accommodation, Allowance)")


class CareerGuidanceResponse(BaseModel):
    counselor_brief: str = Field(
        description="An intimate high-impact narrative paragraph acting as the AI Counselor Brief & Roadmap."
    )
    top_careers: List[CareerItem] = Field(
        description="Top 3 careers matched to user interests and profile",
        min_items=3,
        max_items=3
    )
    top_universities: List[UniversityItem] = Field(
        description="Top 3 universities with exact course and application fee",
        min_items=3,
        max_items=3
    )
    top_tvet_courses: List[TVETItem] = Field(
        description="Top 3 TVET college courses with explicit NQF Level",
        min_items=3,
        max_items=3
    )
    top_bursaries: List[BursaryItem] = Field(
        description="Top 3 eligible bursaries based on calculated APS score and interest alignment",
        min_items=3,
        max_items=3
    )