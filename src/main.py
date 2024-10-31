from datetime import datetime, timezone, timedelta

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, AwareDatetime
from sqlalchemy.orm import Session
from typing import List

import random

from src.config import database
from src.model import User

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)


class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


# GET 요청으로 모든 유저 정보 가져오기
@app.get("/api/users/", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    print("read_users_hi")
    users = db.query(User).offset(skip).limit(limit).all()
    return users


# 특정 유저 정보 가져오기
@app.get("/api/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    print("read_user_hi")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


class CoffeeRequest(BaseModel):
    cafe_id: int
    request_datetime: AwareDatetime
    amount: int


class CoffeeHistory(BaseModel):
    history_id: int
    cafe_id: int
    request_datetime: AwareDatetime
    amount: int


@app.get("/health")
async def health_check():
    return {"message": "I'm healthy"}


@app.post("/api/coffee/collect", status_code=201)
async def coffee_collect(coffee_request: CoffeeRequest) -> dict:
    print(coffee_request)

    return {"history_id": random.randint(1, 100), "msg": "created"}


@app.get("/api/coffee/history", status_code=200)
async def coffee_collect(cafe_id: int) -> dict:
    CoffeeHistory01 = CoffeeHistory(history_id=1, cafe_id=cafe_id,
                                    request_datetime=datetime.now(tz=timezone(timedelta(hours=9))), amount=500)
    CoffeeHistory02 = CoffeeHistory(history_id=2, cafe_id=cafe_id,
                                    request_datetime=datetime.now(tz=timezone(timedelta(hours=9))), amount=1000)

    return {"history": [CoffeeHistory01, CoffeeHistory02]}
