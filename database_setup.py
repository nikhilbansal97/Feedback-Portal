from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Form(Base):
    __tablename__ = "formTable"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(1000), nullable=False)
    last_name = Column(String(1000), nullable=False)
    roll = Column(Integer, nullable=False)
    email_id = Column(String(1000),nullable=False)
    accomodation = Column(String(1000), nullable=False)
    food = Column(String(1000), nullable=False)
    clean = Column(String(1000), nullable=False)
    complain = Column(String(1000), nullable=False)
    behaviour = Column(String(1000), nullable=False)
    medical = Column(String(1000), nullable=False)

class User(Base):
    __tablename__ = "userTable"

    id = Column(Integer, primary_key=True)
    name = Column(String(1000), nullable=False)
    email = Column(String(1000), nullable=False)


engine = create_engine('sqlite:///formdatabase.db')
Base.metadata.create_all(engine)
