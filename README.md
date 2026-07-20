# G Care Healthcare Backend — Ayesha Nazish's Modules

Backend API for the G Care Healthcare Website project (university group project).

## Owner
Ayesha Nazish — Backend Developer

## Modules Implemented


|
 Module 
|
 Endpoints 
|
 Status 
|
|
---
|
---
|
---
|
|
 Branches CRUD 
|
 GET, POST, PUT, DELETE 
|
 Complete & Tested 
|
|
 Booking Requests API 
|
 POST, GET, PATCH, DELETE 
|
 Complete & Tested 
|
|
 FAQs CRUD 
|
 GET, POST, PUT, DELETE 
|
 Complete & Tested 
|
|
 Testimonials CRUD 
|
 GET, POST, PUT, DELETE 
|
 Complete & Tested 
|
|
 Contact Messages API 
|
 POST, GET, PATCH, DELETE 
|
 Complete & Tested 
|
|
 Newsletter API 
|
 POST (subscribe/unsubscribe), GET, DELETE 
|
 Complete & Tested 
|
|
 Website Settings API 
|
 GET, PUT (WhatsApp numbers as array) 
|
 Complete & Tested 
|
|
 Rate Limiting 
|
 Applied to all public write endpoints 
|
 Complete & Tested 
|
|
 CORS 
|
 Configured for local + production origins 
|
 Complete 
|

## Tech Stack
- FastAPI
- SQLAlchemy 2.0
- Pydantic v2
- PostgreSQL (hosted on Neon)

## Project Structure

app/
├── models/ # Database table definitions
├── schemas/ # Request/response validation
├── api/v1/ # API route handlers
├── utils/ # Rate limiter and other shared utilities
└── main.py # App entry point, router registration, CORS setup


## Running Locally

1. Clone the repo
2. Create a virtual environment and activate it:

python -m venv venv
venv\Scripts\activate # Windows

3. Install dependencies:

pip install -r requirements.txt

4. Create a `.env` file with:

DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

5. Run the server:

uvicorn app.main:app --reload


## API Documentation (Swagger)

Once running locally, view all endpoints interactively at:

**http://127.0.0.1:8000/docs**

Health check: **http://127.0.0.1:8000/health**

## Testing

All 7 modules (26 endpoint test cases total) were tested manually via Swagger UI against the live Neon database. Full test results and screenshots are documented in the project development report.

## Merge Status

This repository contains my individually developed and tested modules. Merging into the main project repository requires reconciling `database.py` and `main.py` with the backend lead's version, and aligning on a consistent URL routing pattern across modules before final integration.

