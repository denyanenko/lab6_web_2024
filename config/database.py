from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Підключення до MySQL
DATABASE_URL = "mysql+mysqlconnector://root:Admin@localhost/stolencarsdb"

# Створення двигуна для підключення
engine = create_engine(DATABASE_URL, echo=True)

# Базовий клас для всіх моделей
Base = declarative_base()

# Створення сесії
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
