import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    NGROK_URL = os.getenv("NGROK_URL")
    TRANSCRIPT_DIR = "transcripts"

settings = Settings()
