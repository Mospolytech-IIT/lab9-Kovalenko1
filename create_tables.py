from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "postgresql+psycopg2://postgres:Crossfiri1@localhost:5432/testdb"

engine = create_engine(DATABASE_URL)

def create_tables():
    """Создаёт все таблицы, определённые в модели Base.

    Использует SQLAlchemy для создания таблиц в базе данных,
    указанной в DATABASE_URL.
    """
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()
