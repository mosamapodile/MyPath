import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mypath-secret-key-change-in-prod")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")