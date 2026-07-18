from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import branches, bookings, faqs, testimonials, contact, newsletter, settings

app = FastAPI(title="G Care Healthcare API", version="1.0.0")

# CORS — Section 12: restricted to known frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://gcare.com",
        "https://admin.gcare.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"

app.include_router(branches.router, prefix=API_PREFIX)
app.include_router(bookings.router, prefix=API_PREFIX)
app.include_router(faqs.router, prefix=API_PREFIX)
app.include_router(testimonials.router, prefix=API_PREFIX)
app.include_router(contact.router, prefix=API_PREFIX)
app.include_router(newsletter.router, prefix=API_PREFIX)
app.include_router(settings.router, prefix=API_PREFIX)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "G Care Backend"}