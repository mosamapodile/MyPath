# MyPath
AI career navigation tool in the context of South Africa

MyPath

A simple AI-driven tool to help South African students map out career paths based on their actual results and interests.
The Goal

I built this for students who feel stuck after school—whether they didn't get the marks they wanted or just don't know what's out there. It takes your subjects and goals and gives you a realistic plan.
How it works

    Input: You enter your subjects, marks, and what you care about (Money, Passion, or Stability).

    Processing: A Flask backend sends this data to the OpenAI API with a custom prompt focused on the SA education system.

    Output: You get 3 career options, the required qualifications, and—most importantly—advice on what to do if your marks aren't high enough yet.

Tech Used

    Python/Flask - Backend logic

    Vanilla JS - Handling the frontend requests

    Pico.css - Minimalist styling

    OpenAI API - The "brain" behind the career suggestions

Build Log

    Day 1: Wireframes and UI flow.

    Day 2: Building the basic HTML/CSS shell.

    Day 3: Setting up the Flask server.

    Day 4: Prompt engineering and API integration.

    Day 5: Connecting the frontend to the backend.

    Day 6: Cleanup and bug fixes.

    Day 7: Final testing and demo.

Setup

    Clone the repo.

    Create a virtual environment: python -m venv venv.

    Install requirements: pip install -r requirements.txt.

    Create a .env file with your OPENAI_API_KEY.

    Run python app.py.

License

MIT