def detect_intent(transcript: str) -> str:
    transcript = transcript.lower()
    if "schedule" in transcript or "callback" in transcript:
        return "schedule_callback"
    elif "issue" in transcript or "problem" in transcript:
        return "resolve_issue"
    elif "question" in transcript or "help" in transcript:
        return "inquiry"
    return "unknown"
