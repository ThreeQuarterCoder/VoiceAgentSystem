from pydantic import BaseModel

class CallRequest(BaseModel):
    to_number: str
    message: str

class CallEvent(BaseModel):
    event_type: str
    call_sid: str
    caller_number: str | None = None
    transcript: str | None = None
    intent: str | None = None
