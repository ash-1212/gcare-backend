from app.database import Base, engine
from app.models.branch import Branch
from app.models._test_service_placeholder import Service
from app.models.booking import BookingRequest

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully in Neon DB")