import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from elevenlabs.client import ElevenLabs
from app.config import settings
from app.db import save_call_metadata
from app.intent import detect_intent

class VoiceService:
    def __init__(self):
        self.twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.elevenlabs_client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        os.makedirs(settings.TRANSCRIPT_DIR, exist_ok=True)

    def generate_tts_audio(self, text: str) -> str:
        audio = self.elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        audio_path = f"{settings.TRANSCRIPT_DIR}/prompt_{hash(text)}.mp3"
        with open(audio_path, "wb") as f:
            f.write(audio)
        return audio_path

    def initiate_outbound_call(self, to_number: str, message: str) -> str:
        audio_url = f"{settings.NGROK_URL}/audio/prompt_{hash(message)}.mp3"
        call = self.twilio_client.calls.create(
            to=to_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            url=f"{settings.NGROK_URL}/voice",
            method="POST",
            status_callback=f"{settings.NGROK_URL}/call_status",
            status_callback_method="POST"
        )
        # Save audio file for Twilio to access
        self.generate_tts_audio(message)
        return call.sid

    def handle_inbound_call(self, caller_number: str) -> str:
        resp = VoiceResponse()
        resp.say("Welcome to the support line. Please state your issue.")
        resp.record(
            action=f"{settings.NGROK_URL}/recording",
            method="POST",
            timeout=10,
            transcribe=True,
            transcribe_callback=f"{settings.NGROK_URL}/transcription"
        )
        return str(resp)

    def save_transcript(self, call_sid: str, transcript: str, caller_number: str):
        intent = detect_intent(transcript)
        ticket_id = f"TICKET_{call_sid}" if intent == "resolve_issue" else None
        call_id = save_call_metadata(caller_number, "inbound", intent, ticket_id)
        transcript_path = f"{settings.TRANSCRIPT_DIR}/transcript_{call_id}.txt"
        with open(transcript_path, "w") as f:
            f.write(transcript)
        return intent, ticket_id
