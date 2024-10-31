from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, Integer, String, DateTime
from src.config.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String(100), primary_key=True, index=True)
    cafe_id = Column(Integer, index=True)
    password = Column(String, nullable=False)
    name = Column(String(100))
    address = Column(String(100))
    phone_number = Column(String(100))
    created_at = Column(DateTime, default=datetime.now(timezone(timedelta(hours=9))))
    updated_at = Column(DateTime, default=datetime.now(timezone(timedelta(hours=9))))

