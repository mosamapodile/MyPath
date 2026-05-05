MyPath

MyPath is an AI-powered career guidance application built for South African students who are trying to make sense of their academic reality and translate it into something meaningful, practical, and achievable.

It is not just a tool. It is a direction system.

Why MyPath Exists

MyPath comes from a personal place.

It was shaped through a journey that includes stepping away from university, experiencing a loss of direction, and then choosing to rebuild purpose through software engineering and career exploration.

At its core, MyPath is about regaining control.

It reflects a shift from feeling powerless in uncertain systems to actively building something that helps others find clarity inside those same systems.

This is why the focus is specifically on South African students — where access to guidance, opportunity, and structured career support is often limited or unclear.

What MyPath Does

MyPath takes a student’s subjects, interests, and goals, and transforms them into structured, realistic career pathways.

Each response is built around three core directions:

a stability-oriented path
a growth-oriented path
an experimental or alternative path

These paths are not generic suggestions. They are grounded in real-world constraints, education routes, and opportunities relevant to South Africa.

The goal is to help students move from confusion to structured clarity, and from clarity to action.

System Design

MyPath is being built as a full-stack, modular application rather than a simple chatbot interface.

The system is designed to separate intelligence, state, and presentation so that it can scale properly over time.

Backend (Core Intelligence Layer)
FastAPI for API structure and performance
OpenAI API (GPT-4o-mini) for reasoning and career generation
Pydantic for strict input/output structure and validation
Data Layer (Memory & Control)
PostgreSQL for user accounts and persistent career history
Rate-limited generation system (users can generate career paths a limited number of times per day per account)
Designed to reduce token usage while encouraging intentional use of the system
Frontend (User Experience Layer)
React for a structured, component-based interface
Tailwind CSS for clean, modern styling while maintaining a calm ocean-inspired visual identity
System Flow

The system follows a structured pipeline:

User input (subjects, interests, goals)
→ API request
→ structured AI reasoning
→ validated JSON output
→ frontend rendering of three career paths

The system is designed to produce consistent outputs rather than open-ended conversation.

Core Feature: The Three Path System

Every analysis generates three structured career directions:

Stability Path

A practical route focused on predictable progression, structured education, and long-term security.

Growth Path

A balanced route focused on skill development, opportunity building, and gradual career expansion.

Experimental Path

A flexible route exploring alternative pathways such as entrepreneurship, technology, content creation, or unconventional learning routes.

Each path includes:

reasoning behind why it fits the student
how to realistically pursue it in a South African context
limitations or challenges to consider
first actionable steps
Usage Design & Constraints

MyPath is intentionally designed with controlled usage in mind.

Each user account is limited to a small number of career generation requests per day.

This is not a restriction for limitation’s sake, but a design choice to encourage:

thoughtful input
meaningful reflection
reduced unnecessary API usage
sustainable system scaling

It also ensures the system remains focused on quality over quantity.

Developer

MyPath is built by Mogau Mapodile, a WeThinkCode software engineering student.

The project is deeply personal.

It comes from lived experience — from stepping out of a traditional academic path, facing uncertainty, and choosing to build a system that helps others navigate similar moments with more clarity than was available.

It is both a technical project and a personal statement of direction.

Vision

MyPath aims to evolve into a full career navigation ecosystem for South African students.

The long-term goal is not just to recommend careers, but to help users track their progression over time, understand their evolving interests, and make better long-term decisions with structured guidance.

It sits at the intersection of:

education
artificial intelligence
personal development
and real-world opportunity access
Tech Stack (Evolving Architecture)

The system is being upgraded into a scalable production-grade application:

FastAPI (backend services)
PostgreSQL (user accounts and persistent memory)
Redis (optional session state handling)
React (frontend application layer)
Tailwind CSS (design system and UI consistency)
OpenAI API (GPT-4o-mini for structured reasoning)

License

MIT

# project structure 
mypath/
│
├── backend/
│   ├── app/
│   │
│   ├── main.py                  # FastAPI entry point
│   │
│   ├── core/
│   │   ├── config.py            # env + settings
│   │   ├── prompts.py           # MyPath system prompt (clean version)
│   │   ├── ai_engine.py         # OpenAI wrapper
│   │   ├── rate_limiter.py      # 3 generations/day logic (Redis)
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── analyze.py       # main /generate paths endpoint
│   │   │   ├── user.py          # user profile + history
│   │   │   ├── auth.py          # optional later
│   │
│   ├── services/
│   │   ├── profile_service.py   # builds structured student profile
│   │   ├── path_service.py      # generates 3-path logic layer
│   │   ├── memory_service.py    # PostgreSQL interactions
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── career_session.py    # stores 3-path results
│   │
│   ├── db/
│   │   ├── database.py          # connection setup
│   │   ├── base.py              # SQLAlchemy base
│   │   ├── repositories.py      # DB queries clean layer
│   │
│   ├── schemas/
│   │   ├── request.py           # input validation (Pydantic)
│   │   ├── response.py          # structured AI output format
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── validators.py
│   │
│   ├── requirements.txt
│   └── .env
│
│
├── frontend/
│   ├── src/
│   │
│   │   ├── components/
│   │   │   ├── PathCard.jsx         # core UI (your 3 paths)
│   │   │   ├── InputForm.jsx
│   │   │   ├── Header.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Results.jsx
│   │   │
│   │   ├── services/
│   │   │   ├── api.js               # fetch FastAPI
│   │   │
│   │   ├── styles/
│   │   │   ├── theme.css            # ocean theme (your identity stays here)
│   │   │
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │
│   ├── tailwind.config.js
│   ├── package.json
│
│
├── database/
│   ├── schema.sql                   # users, sessions, usage_limits
│
├── redis/
│   ├── rate_limit.py
│
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   ├── docker-compose.yml
│
├── docs/
│   ├── architecture.md
│   ├── api_spec.md
│
├── README.md
└── .gitignore