from sqlalchemy import Column, String, Integer, Boolean
from database import Base


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    

