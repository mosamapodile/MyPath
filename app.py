from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # We will connect OpenAI here on Day 4
    data = request.json
    print(f"Received data: {data}") 
    return jsonify({"status": "success", "message": "I'm listening! AI coming soon."})

if __name__ == '__main__':
    app.run(debug=True)