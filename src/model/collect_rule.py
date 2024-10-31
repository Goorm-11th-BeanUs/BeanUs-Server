from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, Integer, String, DateTime
from src.config.database import Base


class CollectRule(Base):
    __tablename__ = "collect_rule"

    id = Column(Integer, primary_key=True, index=True)
    cafe_id = Column(Integer, index=True)
    weekday = Column(Integer, primary_key=False, index=False)
    time = Column(String(5), index=False)
    amount = Column(Integer, index=False)
    position = Column(String(100), index=False)
    created_at = Column(DateTime, default=datetime.now(timezone(timedelta(hours=9))))
    updated_at = Column(DateTime, default=datetime.now(timezone(timedelta(hours=9))))

