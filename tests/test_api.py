import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db_connection

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_connection():
    with get_db_connection() as conn:
        yield conn
        conn.rollback()

@pytest.mark.asyncio
async def test_initiate_call(client, mocker):
    mocker.patch("app.voice_service.VoiceService.initiate_outbound_call", return_value="CALL123")
    response = client.post("/call", json={"to_number": "+1234567890", "message": "Hello"})
    assert response.status_code == 200
    assert response.json() == {"call_sid": "CALL123"}

@pytest.mark.asyncio
async def test_handle_transcription(client, db_connection):
    response = client.post(
        "/transcription",
        data={"CallSid": "CALL123", "TranscriptionText": "I need a callback", "From": "+1234567890"}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "processed"}
    with db_connection.cursor() as cur:
        cur.execute("SELECT * FROM calls WHERE caller_number = %s", ("+1234567890",))
        call = cur.fetchone()
        assert call["intent"] == "schedule_callback"
