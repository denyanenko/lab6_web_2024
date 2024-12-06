from fastapi import APIRouter, HTTPException, Depends, Path, Body
from sqlalchemy.orm import Session
from models.Car import Car, CarBase
from config.database import SessionLocal
from typing import Dict
from fastapi import Query
from doc import *

router = APIRouter()


# Функція для отримання сесії з бази даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Створення нового запису (POST)
@router.post("/cars", response_model=CarBase)
async def create_car(car: CarBase, db: Session = Depends(get_db)):
    db_car = Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


# Отримання всіх записів (GET)
@router.get("/cars", response_model=list[CarBase])
async def get_cars(db: Session = Depends(get_db)):
    cars = db.query(Car).all()
    return cars


@router.get("/cars/limited", response_model=dict, summary="Get cars with pagination", responses=response_paginate)
async def get_limited_cars(limit: int = Query(10, description="Number of cars to get per page", ge=1),
                           page: int = Query(1, description="Page number to get", ge=1),
                           db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    cars = db.query(Car).offset(offset).limit(limit).all()
    total_count = db.query(Car).count()
    total_pages = (total_count + limit - 1) // limit  # Загальна кількість сторінок

    # Перетворення об'єктів SQLAlchemy на Pydantic моделі
    cars_pydantic = [CarBase.from_orm(car) for car in cars]

    return {"cars": cars_pydantic, "totalPages": total_pages}


# Отримання одного запису за car_number (GET)
@router.get("/cars/{car_number}", response_model=CarBase, responses=responses_get_by_num)
async def get_car_by_number(car_number: str, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.car_number == car_number).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


# Оновлення інформації про автомобіль
@router.put(
    "/cars/{car_number}",
    summary="Update car information",
    description="Update specific fields of a car identified by its car number.",
    responses=responses_update
)
async def update_car(
        car_number: str = Path(..., description="Car number from URL"),
        car_data: Dict[str, str] = Body(
            ...,
            description="Partial car data to update. Provide fields you want to update.",
            openapi_examples=examples_update
        ),
        db: Session = Depends(get_db)
):
    # Шукаємо автомобіль у базі даних
    db_car = db.query(Car).filter(Car.car_number == car_number).first()

    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    # Оновлюємо передані поля
    updated_fields = 0
    for key, value in car_data.items():
        if hasattr(db_car, key) and getattr(db_car, key) != value:
            setattr(db_car, key, value)
            updated_fields += 1

    if updated_fields == 0:
        raise HTTPException(status_code=400, detail="No changes were made to the car")

    # Зберігаємо зміни у базі даних
    db.commit()
    db.refresh(db_car)

    return {"message": "Car updated successfully", "updated_car": db_car}


# Видалення запису (DELETE)
@router.delete("/cars/{car_number}", response_model=dict, responses=responses_delete)
async def delete_car(car_number: str, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.car_number == car_number).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(db_car)
    db.commit()
    return {"message": "Car deleted"}
