# MyPath — South African AI Career Intelligence Platform

> **Version:** 1.0  
> **Author:** Mosa Mapodile  
> **Project Status:** Active Development  
> **Target Deployment:** Docker / Google Cloud Run

[[_TOC_]]

---

# 1. Project Overview

**MyPath** is an AI-powered career intelligence platform engineered specifically for South African learners. 

Rather than functioning as a standard, generic chatbot, MyPath integrates structured South African educational data, deterministic business logic, and large language models to deliver accurate, personalized career guidance.

WARNING: **Anti-Hallucination Policy:** The system strictly separates data processing from text generation. AI models are strictly prohibited from performing APS score calculations or determining institutional admission thresholds directly.

### Key Questions Answered for Students
* **What can I study?**
* **Which universities or TVET colleges am I eligible for?**
* **What careers align with my interests and academic performance?**
* **Which bursaries, NSFAS opportunities, learnerships, and certifications should I apply for?**
* **What practical steps should I take next?**

**Long-Term Vision:** To establish South Africa's primary Career Intelligence Platform grounded in local educational context and labor market realities.

---

# 2. Technology Stack

### Backend
* **Language:** Python 3.12
* **Framework:** Flask, Gunicorn
* **Middleware:** Flask-CORS
* **Integrations:** OpenAI API (`gpt-4o`)
* **Configuration:** `python-dotenv`

### Frontend
* **Current:** HTML5, CSS3, JavaScript (Vanilla ES6+)
* **Planned:** React / Next.js, Tailwind CSS

### Infrastructure & Deployment
* **Containerization:** Docker
* **Cloud Platform:** Google Cloud Run
* **Target Persistence Layer:** PostgreSQL, Redis, Google Cloud Storage

---

# 3. Development Philosophy & Architecture Principles

MyPath explicitly divides system execution into two primary execution tiers: **Deterministic Python Computation** and **Generative AI Reasoning**.

```mermaid
graph TD
    A[Student Input] --> B[Deterministic Python Engines]
    B -->|APS Score, Eligibility, Matches| C[Fact Payload]
    C --> D[OpenAI Prompt Engine]
    D --> E[Empathetic Guidance Output]


# project structure 

mypath/
├── app.py                       # Core Flask Application Entrypoint
├── config.py                    # Environment Configuration & Flags
├── Dockerfile                   # Containerization Deployment Blueprint
├── requirements.txt             # Python Dependencies List
├── prompts/
│   └── master_prompt.py         # AI Context Assembly & Prompt Engineering
├── routes/
│   └── api.py                   # API Endpoint Controllers & Input Guards
├── services/
│   ├── ai_engine.py             # OpenAI REST Client Interface
│   ├── student_profile.py       # Input Adapter & Data Normalizer
│   ├── recommendation_engine.py # Core Pipeline Orchestration Service
│   ├── university_engine.py     # Higher Education Logic Service
│   └── opportunity_engine.py    # Funding & Training Service
├── engines/
│   ├── aps_engine.py            # NSC Point Calculation Engine
│   ├── career_match_engine.py   # Subject & Interest Scoring Engine
│   ├── eligibility_engine.py    # Institution Admission Logic
│   ├── funding_engine.py        # Bursary & NSFAS Requirement Matcher
│   ├── recommendation_ranker.py # Deterministic Option Ranking System
│   └── scoring_engine.py        # Profile Fit Metric Generator
├── models/
│   └── student.py               # Domain Data Model Definitions
├── schemas/
│   ├── career_response.py       # Response DTO
│   ├── career_path.py           # Career Schema DTO
│   ├── salary.py                # Economic Benchmark DTO
│   ├── roadmap.py               # Path Progression DTO
│   ├── student_request.py       # API Request Validation Schema
│   └── university.py            # Academic Institution DTO
├── utils/
│   ├── validators.py            # Input Validation Functions
│   └── helpers.py               # General String/Data Utilities
├── data/
│   ├── universities.json        # South African University APS Rules Database
│   ├── careers.json             # Career Taxonomy Matrix
│   ├── aps.json                 # NSC Subject Point Lookups
│   ├── salaries.json            # Local Market Remuneration Benchmarks
│   ├── bursaries.json           # Active Bursary Requirements DB
│   ├── learnerships.json        # Learnership Directory
│   ├── opportunities.json       # Extracurricular & Skills Directory
│   └── tvet.json                # TVET College Requirements DB
├── templates/
│   └── index.html               # Main Dashboard HTML Template
├── static/
│   ├── css/                     # Platform Stylesheet Definitions
│   └── js/                      # Main Client UI Controller
└── tests/                       # Unit & Integration Test Suites
