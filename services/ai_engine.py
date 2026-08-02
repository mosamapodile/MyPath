"""
services/ai_engine.py
Communicates with OpenAI to generate dynamic career guidance based on deterministic facts.
Architecture Philosophy: AI is used for reasoning & communication, NOT for facts.
"""

import os
import json
from openai import OpenAI

class AIEngine:
    def __init__(self):
        # Initializes client using OPENAI_API_KEY environment variable
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate_guidance(self, prompt: str) -> dict:
        """
        Sends formatted facts to OpenAI and expects a structured JSON response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are the MyPath AI Career Advisor for South African students. "
                            "Given student profile data and pre-calculated deterministic facts, "
                            "provide detailed, empathetic career reasoning and personal guidance. "
                            "Do not recalculate admission rules or APS scores. "
                            "Return your complete response in valid JSON format."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            print(f"[AI ENGINE JSON ERROR]: Failed to parse OpenAI response: {str(e)}")
            return {
                "guidance": "We generated your recommendations, but encountered an issue parsing the detailed narrative response.",
                "eligible_universities": [],
                "funding_matches": []
            }
        except Exception as e:
            print(f"[AI ENGINE ERROR]: {str(e)}")
            return {
                "guidance": "We hit a snag computing your dynamic roadmap, but your core academic metrics were calculated successfully.",
                "eligible_universities": [],
                "funding_matches": []
            }