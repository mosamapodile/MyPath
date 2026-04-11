import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    subjects = data.get('subjects', '').strip()
    interests = data.get('interests', '').strip()
    goal = data.get('goal', '').strip()

    if not subjects or not interests:
        return jsonify({"message": "The tide needs water to move. Please share your marks and interests."}), 400

    prompt = f"""
    You are 'MyPath', a wise and hopeful career mentor for South African students. 
    A student has shared their heart with you:
    
    - Subjects & Marks: {subjects}
    - What makes them come alive: {interests}
    - Their current life mission: {goal}

    Your task:
    1. Start with a deep, introspective sentence acknowledging their journey.
    2. Suggest 3 realistic career paths available in South Africa.
    3. For each path, explain the 'why' and the 'how' (qualifications needed).
    4. If marks are low, emphasize 'Hidden Channels' like TVET colleges or Higher Certificates.
    5. End with a strong note of hope, reminding them that the tide always turns.

    Tone: Oceanic, calm, professional, and poetic. Use Markdown for formatting.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a South African career expert with a poetic soul."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        advice = response.choices[0].message.content
        return jsonify({"message": advice})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "The sea is a bit rough (API Error). Check your key and connection!"}), 500

if __name__ == '__main__':
    app.run(debug=True)
# $5 openai api keys quota bill
