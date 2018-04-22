from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Form, User, Base

engine = create_engine('sqlite:///formdatabase.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

formsList = session.query(Form).all()

if len(formsList) > 0:
    for form in formsList:
        session.delete(form)
    session.commit()

form1 = Form(first_name="John",last_name="Abrahim", roll='1010102',email_id='john@gmail.com',accomodation="good",food="good", clean="good", complain="bad", behaviour="okok", medical="bad")
session.add(form1)
form2 = Form(first_name="Jonny",last_name="Bravo", roll='1010102',email_id='jonny@gmail.com',accomodation="good",food="bad", clean="good", complain="bad", behaviour="very good", medical="bad")
session.add(form2)
form3 = Form(first_name="Shinchan",last_name="Cartoon", roll='1010102',email_id='john@gmail.com',accomodation="good",food="good", clean="good", complain="bad", behaviour="awesome", medical="not good")
session.add(form3)
user1 = User(name="Admin", email="admin@google.com")
session.add(user1)
user2 = User(name="President",email="president@gmail.com")
session.add(user2)

session.commit()
