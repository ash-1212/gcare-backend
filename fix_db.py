"""
One-time fix script: drops broken tables and mismatched enum types,
so they can be recreated correctly by SQLAlchemy.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS booking_requests;"))
    conn.execute(text("DROP TYPE IF EXISTS bookingstatus;"))
    conn.execute(text("DROP TYPE IF EXISTS booking_status;"))

    conn.execute(text("DROP TABLE IF EXISTS contact_messages;"))
    conn.execute(text("DROP TYPE IF EXISTS contactstatus;"))
    conn.execute(text("DROP TYPE IF EXISTS contact_status;"))

    conn.execute(text("DROP TABLE IF EXISTS website_settings;"))

    conn.commit()

print("✅ Old tables and enum types dropped successfully")