from app.database import Base, engine
from app.models.branch import Branch
from app.models._test_service_placeholder import Service
from app.models.booking import BookingRequest
from app.models.contact import ContactMessage
from app.models.settings import WebsiteSetting
from app.models.faq import FAQ
from app.models.testimonial import Testimonial
from app.models.newsletter import NewsletterSubscriber

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully in Neon DB")