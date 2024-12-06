from sqlalchemy import Column, String, Enum
from config.database import Base
from pydantic import BaseModel
from typing import Literal


# SQLAlchemy модель для таблиці StolenCars
class Car(Base):
    __tablename__ = "StolenCars"

    car_number = Column(String(20), primary_key=True, index=True)
    brand = Column(String(50), nullable=False)
    status = Column(Enum('Викрадений', 'Знайдений', name='status_enum'), default='Викрадений')
    owner_surname = Column(String(100), nullable=False)


# Pydantic модель для відповіді
class CarBase(BaseModel):
    car_number: str
    brand: str
    status: Literal['Викрадений', 'Знайдений'] = 'Викрадений'
    owner_surname: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "car_number": "AA1234BB",
                "status": "Викрадений",
                "brand": "Toyota",
                "model": "Corolla"
            }
        }