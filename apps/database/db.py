from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем подключение
DATABASE_URL = "postgresql://postgres:5441@localhost:5434/scopus-server"
engine = create_engine(DATABASE_URL)

# Определяем базовый класс для ORM
Base = declarative_base()

# Определяем модель таблицы
class Request(Base):
    __tablename__ = 'request'

    id = Column(BigInteger, primary_key=True)
    folder_id = Column(String(60), nullable=False)
    first_status = Column(String(50), default='false')
    second_status = Column(String(50), default='false')
    search_type = Column(String(50))
    query = Column(Text)
    result = Column(JSONB)

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем все таблицы в базе данных (если они еще не существуют)
Base.metadata.create_all(bind=engine)


def add_request(folder_id: str, first_status: str, second_status: str, search_type: str, query: str, result: dict):
    """
    Функция для добавления новой записи в таблицу request.
    """
    # Создаем сессию
    session = SessionLocal()

    try:
        # Создаем новый объект Request
        new_request = Request(
            folder_id=folder_id,
            first_status=first_status,
            second_status=second_status,
            search_type=search_type,
            query=query,
            result=result
        )

        # Добавляем запись в базу
        session.add(new_request)
        session.commit()
        print(f"Запись с ID {new_request.id} успешно добавлена.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении записи: {e}")
    finally:
        session.close()


def get_result_db(folder_id: str):
    """
    Функция для получения всех записей из таблицы request.
    """
    session = SessionLocal()

    try:
        # Получаем все записи
        req = session.query(Request).filter(Request.folder_id == folder_id).order_by(Request.id.desc()).first()
        return req.result
    except Exception as e:
        print(f"Ошибка при чтении данных: {e}")
        return []
    finally:
        session.close()


def get_last_request_by_folder_id(folder_id: str):
    """
    Функция для получения последней записи по folder_id.
    """
    session = SessionLocal()

    try:
        # Получаем последнюю запись для указанного folder_id, сортируя по id в убывающем порядке
        last_request = session.query(Request).filter(Request.folder_id == folder_id).order_by(Request.id.desc()).first()
        return last_request
    except Exception as e:
        print(f"Ошибка при чтении последней записи: {e}")
        return None
    finally:
        session.close()


def update_request(folder_id: str, result_value: dict, status_field: str):
    """
    Функция для обновления записи по folder_id:
    - Обновляет поле result.
    - Устанавливает first_status или second_status равным 'true'.

    :param folder_id: Идентификатор папки для поиска записи.
    :param result_value: Значение, которое нужно установить в поле result.
    :param status_field: Поле статуса, которое нужно обновить ('first_status' или 'second_status').
    """
    session = SessionLocal()

    try:
        request = session.query(Request).filter(Request.folder_id == folder_id).order_by(Request.id.desc()).first()
        
        if not request:
            return False

        # Обновляем поле result
        if result_value != []:
            request.result = result_value

        # Устанавливаем статус в true
        if status_field == "first_status":
            request.first_status = "true"
        elif status_field == "second_status":
            request.second_status = "true"
        else:
            return False

        # Сохраняем изменения
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()


def get_status(folder_id: str, status_number: str):
    """
    Функция для получения последней записи по folder_id.
    """
    session = SessionLocal()

    try:
        # Получаем последнюю запись для указанного folder_id, сортируя по id в убывающем порядке
        last_request = session.query(Request).filter(Request.folder_id == folder_id).order_by(Request.id.desc()).first()
        if status_number == "1":
            return last_request.first_status
        else:
            return last_request.second_status
    except Exception as e:
        print(f"Ошибка при чтении последней записи: {e}")
        return None
    finally:
        session.close()
