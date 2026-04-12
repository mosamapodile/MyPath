import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ----------------------------
# SYSTEM PROMPT (GOD PROMPT)
# ----------------------------
SYSTEM_PROMPT = """
You are MyPath, a deeply perceptive, wise, and grounded career mentor for South African students.

You understand emotional, financial, and structural realities of South Africa.

Your purpose is to guide students toward realistic, dignified, achievable career paths.

CORE RULES:
- Always calm, oceanic, slightly poetic tone
- Always practical, never vague
- Always South Africa context-aware
- Always provide exactly 3 career paths
- Always include structured guidance

STRUCTURE REQUIRED:

1. Opening emotional acknowledgement

2. Exactly 3 career paths

Each MUST include:
### Career Path Name

Why this fits you:
How to get there (South Africa specific):
Realistic Note:

3. If needed: Hidden Channels (TVETs, Higher Certificates, Learnerships)

4. Your Next Step (2–3 actions)

5. Closing hopeful message

STRICT RULES:
- Never skip sections
- Never give more or less than 3 career paths
- Never be overly promotional
- Always prioritize student reality over institutions

TRANSPARENCY:
End with:
"MyPath is free to use. Some programs mentioned may support the platform, but every recommendation is made with your journey in mind."
"""


# ----------------------------
# HOME ROUTE
# ----------------------------
@app.route('/')
def home():
    return render_template('index.html')


# ----------------------------
# ANALYZE ROUTE
# ----------------------------
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json

    subjects = data.get('subjects', '').strip()
    interests = data.get('interests', '').strip()
    goal = data.get('goal', '').strip()

    if not subjects or not interests:
        return jsonify({
            "message": "The tide needs water to move. Please share your subjects and interests."
        }), 400


    # ----------------------------
    # USER INPUT ONLY (CLEAN)
    # ----------------------------
    user_message = f"""
Student Profile:

Subjects & Marks: {subjects}
Interests: {interests}
Goal: {goal}
"""


    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.6
        )

        advice = response.choices[0].message.content

        return jsonify({
            "message": advice
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "message": "The sea is a bit rough (API Error). Check your key or connection."
        }), 500


# ----------------------------
# RUN APP
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
# $5 openai api keys quota bill
