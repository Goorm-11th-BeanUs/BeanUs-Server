from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, Integer, String, DateTime
from src.config.database import Base


class CollectTransaction(Base):
    __tablename__ = "collect_transaction"

    id = Column(Integer, primary_key=True, index=True)
    cafe_id = Column(Integer, index=True)
    client_name = Column(String(100), index=False)
    time = Column(DateTime, index=True)
    amount = Column(Integer, index=False)
    status = Column(String(100), index=True)
    created_at = Column(DateTime, default=datetime.now(timezone(timedelta(hours=9))))
    updated_at = Column(DateTime, default=datetime.now(timezone(timedelta(hours=9))))

