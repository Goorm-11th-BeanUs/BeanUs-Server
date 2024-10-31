from datetime import datetime, timezone, timedelta

from fastapi import FastAPI, Depends, HTTPException, Cookie, status
from pydantic import BaseModel, AwareDatetime
from sqlalchemy.orm import Session
from typing import List

from src.config import database
from src.model.user import User
from src.model.collect_rule import CollectRule
from src.model.collect_transaction import CollectTransaction

app = FastAPI(version="1.0.0", docs_url="/api/swagger", redoc_url="/api/docs")


database.Base.metadata.create_all(bind=database.engine)


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


class RuleRead(BaseModel):
    cafe_id: int
    weekday: int
    time: str
    amount: int

    class Config:
        orm_mode = True


class HistoryRead(BaseModel):
    id: int
    cafe_id: int
    client_name: str
    time: datetime
    status: str
    amount: int

    class Config:
        orm_mode = True


class AccountRequest(BaseModel):
    user_id: str
    password: str


class AccountOtherInfo(BaseModel):
    name: str
    phone_number: str
    address: str


@app.post("/api/account/join", status_code=200)
async def account_join(account_request: AccountRequest, db: Session = Depends(database.get_db)) -> dict:
    user = db.query(User).filter(User.id == account_request.user_id).first()

    if user:
        raise HTTPException(status_code=403, detail="id already exists")

    db.add(User(id=account_request.user_id, password=account_request.password))
    db.commit()

    user = db.query(User).filter(User.id == account_request.user_id).first()

    return {"msg": f"{account_request.user_id} 님, 환영합니다!", "cafe_id": user.cafe_id}


@app.post("/api/account/login", status_code=200)
async def account_login(account_request: AccountRequest, db: Session = Depends(database.get_db)) -> dict:
    user = db.query(User).filter(User.id == account_request.user_id
                                 , User.password == account_request.password).first()

    if user is None:
        raise HTTPException(status_code=404, detail="not found")

    if user.name and user.phone_number and user.address:
        return {"msg": f"{account_request.user_id} 님, 어서오세요!", "cafe_id": user.cafe_id}

    raise HTTPException(status_code=401, detail="unauthorized")


@app.post("/api/account/info/{user_id}", status_code=201)
async def account_join(user_id: str, other_info: AccountOtherInfo, db: Session = Depends(database.get_db)) -> dict:
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="not found")

    user.name = other_info.name
    user.phone_number = other_info.phone_number
    user.address = other_info.address

    db.commit()
    db.refresh(user)

    return {"msg": f"{user_id} 님, 정보 업데이트 완료!", "cafe_id": user.cafe_id}



@app.get("/api/users", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    print("read_users_hi")
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/api/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    print("read_user_hi")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


class CollectDays(BaseModel):
    weekday: int
    time: str


class CoffeeRequest(BaseModel):
    collect_days: List[CollectDays]
    amount: int
    position: str


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


@app.get("/api/coffee/rules", status_code=200, response_model=List[RuleRead])
async def get_coffee_rules(db: Session = Depends(database.get_db)) -> dict:
    rules = db.query(CollectRule).all()

    return rules


@app.get("/api/coffee/{cafe_id}/rule", status_code=200, response_model=List[RuleRead])
async def get_coffee_rule(cafe_id: int, db: Session = Depends(database.get_db)) -> dict:
    rules = db.query(CollectRule).filter(CollectRule.cafe_id == cafe_id).all()
    if not rules:
        raise HTTPException(status_code=404, detail="User not found")

    return rules


@app.post("/api/coffee/{cafe_id}/rule", status_code=201)
async def post_coffee_rule(cafe_id: int, coffee_request: CoffeeRequest, db: Session = Depends(database.get_db)) -> dict:
    # old_rules = db.query(CollectRule).filter(CollectRule.cafe_id == cafe_id).all()
    #
    # for old_rule in old_rules:
    #     db.delete(old_rule)

    collect_days = coffee_request.collect_days

    for collect_day in collect_days:
        db.add(CollectRule(cafe_id=cafe_id, weekday=collect_day.weekday, time=collect_day.time))

    db.commit()

    return {}


@app.get("/api/coffee/{cafe_id}/transaction", status_code=200, response_model=List[HistoryRead])
async def coffee_history(cafe_id: int, db: Session = Depends(database.get_db)) -> dict:
    histories = db.query(CollectTransaction).filter(CollectTransaction.cafe_id == cafe_id).all()

    return histories


@app.post("/api/coffee/{cafe_id}/transaction", status_code=201)
async def coffee_history(cafe_id: int, coffee_history: CoffeeHistory, db: Session = Depends(database.get_db)) -> dict:
    db.add(CollectTransaction(cafe_id=cafe_id, client_name=coffee_history.client_name,
                              time=coffee_history.time, amount=coffee_history.amount, status="Waiting"))

    db.commit()
    return {}


@app.delete("/api/coffee/{cafe_id}/transaction", status_code=204)
async def coffee_cancel(cafe_id: int, cancel_coffee: CancelCoffee, db: Session = Depends(database.get_db)):
    histories = db.query(CollectTransaction).filter(CollectTransaction.cafe_id == cafe_id,
                                                    CollectTransaction.id == cancel_coffee.history_id).all()

    db.delete(histories)
    db.commit()

    return None


@app.get("/api/coffee/{cafe_id}/carbon", status_code=200)
async def carbon(cafe_id: int, db: Session = Depends(database.get_db)) -> dict:
    histories = db.query(CollectTransaction).filter(CollectTransaction.cafe_id == cafe_id
                                                    , CollectTransaction.status == "COMPLETED").all()

    amount = 0

    for history in histories:
        amount += history.amount

    return {"carbon": amount}
