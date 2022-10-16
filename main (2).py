from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy import Column, Integer, String,create_engine
from sqlalchemy.orm import sessionmaker, Session
from databases import *
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import session
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user: password@postgresserver /db"
# creating an engine

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False}
)

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base= declarative_base()

class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, index=True)
    name= Column(String)
    age= Column(Integer,)

Base.metadata.create_all(bind=engine)



SessionLocal= sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()
# create a Person object to add to the database
tom= Person(name="Tom", age=38)
db.add(tom) # add to the database
db.commit() # commit changes

# create a Person object to add to the database
tom= Person(name="Tom", age=38)
db.add(tom) # add to the database
db.commit() # commit changes
db.refresh(tom) # refresh object state
# print(tom.id) # you can get the set id

bob = Person(name="Bob", age=42)
sam= Person(name="Sam", age=25)
db.add(bob)
db.add(sam)
db.commit()

alice = Person(name="Alice", age=33)
kate= Person(name="Kate", age=28)
db.add_all([alice, kate])
db.commit()

db.query(Person)

people=db.query(Person).all()
# for p  in people:
#     print(f"{p.id}.{p.name} ({p.age})")

# getting one object by id
first_person = db.get(Person,1)
# print(f"{first_person.name} - {first_person.age}")
#Tom-38

people = db.query(Person).filter(Person.age >30).all()
# for p in people:
    # print(f"{p.id}.{p.name} ({p.age})")

first = db.query(Person).filter(Person.id==1).first()
# print(f"{first.name} ({first.age})")

tom.name = "Tomas"
tom.age= 22

db.commit()
# check that the changes are applied in the database - we get one object whose name is Tomas
tomas = db.query(Person).filter(Person.id == 1).first()
# print(f"{tom.id}.{tom.name} ({tom.age})")

# bob = db.query(Person).filter(Person.id==2).first()
# db.delete(bob) # delete object
# db.commit() # commit change


app=FastAPI()
def get_db():
    db= SessionLocal()

@app.get("/")
def main():
    return FileResponse("public/index.html")
@app.get("/api/users")
def get_people(db:Session = Depends(get_db)):
    return db.query(Person).all()
@app.get("/api/users/{id}")
def get_person(id,db:Session= Depends(get_db)):
# get user by id
    person = db.query(Person).filter(Person.id == id).first()
# if not found, send status code and error message
    if person==None:
        return JSONResponse(status_code=404, content={ "message": "User not found"})
#if the user is found, send it
    return person
@app.post("/api/users")
def create_person(data = Body(), db:Session= Depends(get_db)):
    person = Person(name=data["name"], age=data["age"])
    db.add(person)
    db.commit()
    db.refresh(person)
    return person
@app.put("/api/users")
def edit_person(data = Body(), db:Session= Depends(get_db)):
# get user by id
    person = db.query(Person).filter(Person.id == data["id"]).first()
# if not found, send status code and error message
    if person == None:
        return JSONResponse(status_code=404, content={ "message": "User not found"})


# if the user is found, change his data and send it back to the client
    person.age = data["age"]
    person.name = data["name"]
    db.commit()  # commit changes
    db.refresh(person)
    return person

@app.delete("/api/users/{id}")
def delete_person(id,db:Session= Depends(get_db)):
# get user by id
    person = db.query(Person).filter(Person.id == id).first()
# if not found, send status code and error message
    if person == None:
        return JSONResponse( status_code=404, content={ "message": "User not found"})
# if the user is found, delete it
    db.delete(person) # delete object
    db.commit() # commit changes
    return person

Base.metadata.create_all(bind=engine)


@app.get("/api/users")
def get_people(db:Session = Depends(get_db)):
    return db.query(Person).all()

@app.get("/api/users/{id}")
def get_person(id,db:Session= Depends(get_db)):
    person = db.query(Person).filter(Person.id == id).first()
    if person==None:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    return person

@app.delete("/api/users/{id}")
def delete_person(id,db:Session= Depends(get_db)):
    person = db.query(Person).filter(Person.id == id).first()
    if person == None:
        return JSONResponse( status_code=404, content={ "message": "User not found"})
    db.delete(person)
    db.commit()
    return person

@app.post("/api/users")
def create_person(data = Body(), db:Session= Depends(get_db)):
    person = Person(name=data["name"], age=data["age"])
    db.add(person)
    db.commit()
    db.refresh(person)
    return person

@app.put("/api/users")
def edit_person(data = Body(), db:Session= Depends(get_db)):
    person = db.query(Person).filter(Person.id == data["id"]).first()
    if person == None:
        return JSONResponse(status_code=404, content={ "message": "User not found"})
    person.age = data["age"]
    person.name = data["name"]
    db.commit() # commit changes
    db.refresh(person)
    return person