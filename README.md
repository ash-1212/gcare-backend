# G Care Healthcare Backend — Ayesha Nazish's Modules

Backend API for the G Care Healthcare Website project (university group project).

## Owner
Ayesha Nazish — Backend Developer

## Modules Implemented
- Branches CRUD
- Booking Requests API
- FAQs CRUD
- Testimonials CRUD
- Contact Messages API
- Newsletter Subscribe/Unsubscribe API
- Website Settings API (WhatsApp numbers, phone, social links)
- Rate Limiting (public write endpoints)
- CORS configuration

## Tech Stack
- FastAPI
- SQLAlchemy 2.0
- Pydantic v2
- PostgreSQL (hosted on Neon)

## Running Locally

1. Clone the repo
2. Create a virtual environment and activate it:
python -m venv venv
venv\Scripts\activate   # Windows
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