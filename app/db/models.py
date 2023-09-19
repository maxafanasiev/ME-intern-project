from sqlalchemy import Column, Integer, String, Boolean, ARRAY, DateTime, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_email = Column(String(255), unique=True, nullable=False)
    user_firstname = Column(String(100), nullable=True)
    user_lastname = Column(String(100), nullable=True)
    user_status = Column(String(100), nullable=True)
    user_city = Column(String(50), nullable=True)
    user_phone = Column(String(20), nullable=True)
    user_links = Column(ARRAY(String), nullable=True)
    user_avatar = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now())

