from datetime import datetime, timezone, timedelta

from fastapi import FastAPI
from pydantic import BaseModel, AwareDatetime

import random

app = FastAPI()


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
