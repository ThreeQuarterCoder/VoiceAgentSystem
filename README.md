# AI Voice Agent System (PoC-1)

A proof-of-concept voice assistant using Twilio, ElevenLabs, FastAPI, and PostgreSQL.

## Setup

1. **Setup a Virtual environment**: 
  ```bash 
   python -m venv venv 
   source ./venv/bin/activate
  ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up PostgreSQL**:
     * Install PostgreSQL locally.
     * Create a database: createdb voice_agent.
     * Update DATABASE_URL in .env
4. **Configure APIs**:
     * Sign up for Twilio (free-tier) and get TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER.
     * Sign up for ElevenLabs and get ELEVENLABS_API_KEY.
     * Run ngrok http 8000 to get a public URL and update NGROK_URL in .env.
5. **Set Environment Variables: Create a .env file with the above variables.**
6. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```
7. **Run Tests**:
   ```bash
   pytest
   ```


## Usage

1. Outbound calls
    ```bash
       curl -X POST http://localhost:8000/call -H "Content-Type: application/json" -d '{"to_number": "+1234567890", "message": "Hello, how can we assist you?"}'
    ```
    
    * Websocket Events: Connect to ws://localhost:8000/ws to receive real-time call events.
    * Transcripts: Stored in transcripts/ as .txt files.
    * Metadata: Stored in PostgreSQL calls table.

## Notes

1. Use ngrok for Twilio webhooks (free-tier).
2. Intent detection can be improved by using OpenAI

