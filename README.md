---
title: MonoScrum Face API
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 7860
---

# MonoScrum Face API

FastAPI-based face recognition service for the MonoScrum Attendance Kiosk.

## Endpoints

- GET /health — Health check
- POST /api/v1/scan/enroll — Enroll a face for a user
- POST /api/v1/scan/verify — Verify a face against enrolled faces

## Environment Variables

Set these as **Secrets** in Hugging Face Spaces settings:

| Variable | Description |
|----------|-------------|
| PINECONE_API_KEY | Your Pinecone API key |
| PINECONE_ENV | Pinecone region (e.g. us-east-1) |
| PINECONE_INDEX_NAME | Pinecone index name (e.g. monoscrum-faces) |

## Local Development

To run the application locally on your machine without using ngrok, use the following commands:

1. **Activate the virtual environment (Windows):**
   ```bash
   venv\Scripts\activate
   ```

2. **Run the FastAPI server using Uvicorn:**
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
   ```
   
*(Ensure that `FACE_API_URL="http://localhost:8001"` is updated in the `mono-scrum-api` `.env` file.)*
