from datetime import datetime, timezone, timedelta

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, AwareDatetime
# from sqlalchemy.orm import Session
from typing import List

import random

# from src.config import database
# from src.model import User

app = FastAPI()

# database.Base.metadata.create_all(bind=database.engine)


class UserRead(BaseModel):
    id: int
    token: str
    name: str
    address: str
    phone_number: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# GET 요청으로 모든 유저 정보 가져오기
# @app.get("/api/users/", response_model=List[UserRead])
# def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
#     print("read_users_hi")
#     users = db.query(User).offset(skip).limit(limit).all()
#     return users
#
#
# # 특정 유저 정보 가져오기
# @app.get("/api/users/{user_id}", response_model=UserRead)
# def read_user(user_id: int, db: Session = Depends(database.get_db)):
#     print("read_user_hi")
#     user = db.query(User).filter(User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


class CollectDays(BaseModel):
    weekday: int
    time: str


class CoffeeRequest(BaseModel):
    cafe_id: int
    collect_days: List[CollectDays]
    amount: int


class CoffeeHistory(BaseModel):
    history_id: int
    client_name: str
    time: AwareDatetime
    state: str
    amount: int


class CancelCoffee(BaseModel):
    history_id: int


@app.get("/health")
async def health_check():
    return {"message": "I'm healthy"}


@app.post("/api/coffee/collect", status_code=201)
async def coffee_collect(coffee_request: CoffeeRequest) -> dict:
    return {"history_id": random.randint(1, 100)}


@app.post("/api/coffee/cancel", status_code=204)
async def coffee_cancel(cancel_coffee: CancelCoffee):
    return None


@app.get("/api/coffee/history/{cafe_id}", status_code=200)
async def coffee_history(cafe_id: int) -> dict:
    coffeeHistory01 = CoffeeHistory(history_id=1, client_name="abc학교",
                                    time=datetime.now(tz=timezone(timedelta(hours=9))), state="READY"
                                    , amount=10 * random.randint(1, 10))
    coffeeHistory02 = CoffeeHistory(history_id=2, client_name="123시청",
                                    time=datetime.now(tz=timezone(timedelta(hours=9))), state="QUEUED"
                                    , amount=10 * random.randint(1, 10))
    coffeeHistory03 = CoffeeHistory(history_id=3, client_name="ㄱㄴㄷ회사",
                                    time=datetime.now(tz=timezone(timedelta(hours=9))), state="COMPLETED"
                                    , amount=10 * random.randint(1, 10))
    coffeeHistory04 = CoffeeHistory(history_id=5, client_name="ㄱㄴㄷ회사2",
                                    time=datetime.now(tz=timezone(timedelta(hours=9))), state="COMPLETED"
                                    , amount=10 * random.randint(1, 10))

    res = {"histories": [coffeeHistory01, coffeeHistory02, coffeeHistory03, coffeeHistory04]}

    print(res)
    return res
