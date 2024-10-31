from sqlalchemy import Column, Integer, String, DateTime
from ..config.database import Base
from datetime import datetime, timedelta, timezone


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Integer, primary_key=False, index=False)
    name = Column(String(100))
    address = Column(String(100))
    phone_number = Column(String(100))
    role = Column(String(100))
    created_at = Column(DateTime, default=datetime.now(timezone(timedelta(hours=9))))
    updated_at = Column(DateTime, default=datetime.now(timezone(timedelta(hours=9))))

