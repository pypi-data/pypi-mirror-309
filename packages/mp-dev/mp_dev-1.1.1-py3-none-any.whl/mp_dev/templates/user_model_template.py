def get_content():
    return """from sqlalchemy import Column, Integer, String, func, DateTime

from app.DB.Connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    firstname = Column(String)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)
"""