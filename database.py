from models import Base
from config import engine


def create_table():
    Base.metadata.create_all(engine)
    print("Создана таблица в БД")

def delete_table():
    Base.metadata.drop_all(engine)
    print("Таблица очищена")