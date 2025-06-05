from fastapi import FastAPI, WebSocket
from fastapi.responses import PlainTextResponse
from app.voice_service import VoiceService
from app.models import CallRequest, CallEvent
from app.config import settings
import json

app = FastAPI()
voice_service = VoiceService()
websocket_connections = []

@app.on_event("startup")
async def startup_event():
    voice_service.db.init_db()

@app.post("/call", response_model=dict)
async def initiate_call(request: CallRequest):
    call_sid = voice_service.initiate_outbound_call(request.to_number, request.message)
    event = CallEvent(event_type="call_initiated", call_sid=call_sid, caller_number=request.to_number)
    await broadcast_event(event)
    return {"call_sid": call_sid}

@app.post("/voice", response_class=PlainTextResponse)
async def handle_voice():
    return voice_service.handle_inbound_call("unknown")

@app.post("/recording", response_class=PlainTextResponse)
async def handle_recording():
    resp = VoiceResponse()
    resp.say("Thank you. Your request is being processed.")
    return str(resp)

@app.post("/transcription")
async def handle_transcription(CallSid: str, TranscriptionText: str, From: str):
    intent, ticket_id = voice_service.save_transcript(CallSid, TranscriptionText, From)
    event = CallEvent(
        event_type="transcription_processed",
        call_sid=CallSid,
        caller_number=From,
        transcript=TranscriptionText,
        intent=intent
    )
    await broadcast_event(event)
    return {"status": "processed"}

@app.post("/call_status")
async def handle_call_status(CallSid: str, CallStatus: str):
    event = CallEvent(event_type=f"call_{CallStatus}", call_sid=CallSid)
    await broadcast_event(event)
    return {"status": "processed"}

@app.get("/audio/{filename}", response_class=PlainTextResponse)
async def serve_audio(filename: str):
    with open(f"{settings.TRANSCRIPT_DIR}/{filename}", "rb") as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        websocket_connections.remove(websocket)

async def broadcast_event(event: CallEvent):
    for connection in websocket_connections:
        await connection.send_text(json.dumps(event.dict()))
