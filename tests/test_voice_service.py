import pytest
from app.voice_service import VoiceService
from app.intent import detect_intent
from unittest.mock import patch

@pytest.fixture
def voice_service():
    return VoiceService()

def test_detect_intent():
    assert detect_intent("I need a callback") == "schedule_callback"
    assert detect_intent("I have an issue") == "resolve_issue"
    assert detect_intent("What's this?") == "inquiry"
    assert detect_intent("Hello") == "unknown"

@patch("app.voice_service.ElevenLabs")
def test_generate_tts_audio(mock_elevenlabs, voice_service, tmp_path):
    mock_elevenlabs.return_value.text_to_speech.convert.return_value = b"audio_data"
    audio_path = voice_service.generate_tts_audio("Hello")
    assert audio_path.startswith("transcripts/prompt_")
    assert audio_path.endswith(".mp3")
    assert os.path.exists(audio_path)
