from fastapi import FastAPI, Response, Path, Query, status, Body, Form
import mimetypes
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse,PlainTextResponse,FileResponse,RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field
import uuid
app = FastAPI()
@app.get("/")
def read_root():
    # html_content= "<h2> Hello, my name is Arailym!</h2>"
    # content =  {"message":"HEllo"}
    # json_content = jsonable_encoder(content)
    # return  JSONResponse(content=json_content)
    return FileResponse("index.html")

@app.get("/about")
def about():
    return JSONResponse(content={"message":"about"})

@app.get("/text",response_class=PlainTextResponse)
def text():
    data = "Daniyar"
    # PlainTextResponse
    return Response(content=data,media_type="text/plain")

@app.get("/html",response_class=FileResponse)
def root_html():
    # The default browser tries to interpret and display all the files it can, such as text files, image
    # files, some other multimedia files. If the file cannot be interpreted by the browser, then it is
    # downloaded. However, it may be necessary to automatically load without displaying some
    # interpreted files, for example, the same html files. In this case, we can set the
    # parametermedia_typeapplication/octet-stream value. In addition, using the filename parameter for
    # the uploaded file, you can specify a name:
    # return "index.html"
    return FileResponse("for the 1-11 index/index.html", filename="for the 1-11 index/index.html", media_type="application/octet-stream")

@app.get("/users/{name}/{age}")
def users(name:str= Path(min_length=1,max_length=50),age:int= Path(ge=18)):
    return {"user_name" : name,"user_age":age}

@app.get("/users/{name}")
def users(name):
    return {"user_name" : name}

@app.get("/users/admin")
def admin():
    return {"message" : "Hello admin"}

@app.get("/phone")
def phone(phone:str = Path(regex="^\d{8}$")):
    return {"phone": phone}

@app.get("/question")
def question(name:str="Underfined",age:int=0):
    return {"name":name,"age":age}
# http://127.0.0.1:8000/question?name=%22Danik%22&age=18

@app.get("/None")
def users(name:str |None = Query(default=None, min_length=2)):
    if name==None:
        return {"name": "Undefined"}
    else:
        return {"name": name}

@app.get("/list")
def users(people:list[str]= Query()):
    return {"people": people}
# http://127.0.0.1:8000/users?people=AL&people=Dan

# @app.get("/notfound", status_code=404)
# def notfound():
#     return {"message": "Resource Not Found"}

@app.get("/notfound", status_code=status.HTTP_404_NOT_FOUND)
def notfound():
    return {"message": "Resource Not Found"}


@app.get("/response/{id}", status_code=200)
def users(response: Response, id:int):
    if id < 1:
        response.status_code = 400
        return {"message": "Incorrect Data"}
    return {"message": f"Id = {id}"}

@app.get("/old")
def old():
    return RedirectResponse("/new")

@app.get("/new")
def new():
    return PlainTextResponse("New Page")

@app.get("/olds", response_class=RedirectResponse, status_code=302)
def olds():
    return "https://metanit.com/python/fastapi/"

# app.mount("/",StaticFiles(directory = ".",html=True))

# @app.post("/hello")
# def hello(data=Body()):
#     name = data["name"]
#     age = data["age"]
#     return {"message":f" {name}, your age is: {age}"}
class Company(BaseModel):
    name:str
class Person(BaseModel):
    # name: str = Field(default="Undefined", min_length=3, max_length=12)
    # age:int |None = None
    # name:str
    # languages: list = []
    # languages: list = ["Java", "Python", "JavaScript"]
    name: str
    company: Company

# @app.post("/hello")
# def hello(person: Person):
#     if person.age == None:
#         return {"message": f"Hi, {person.name}"}
#     else:
#         return {"message": f"Hi {person.name}, your age is {person.age}"}

# @app.post("/hello")
# def hello(person: Person):
#  return {"message": f"Name: {person.name}. Languages: {person.languages}"}

@app.post("/hello")
def hello(person: Person):
 return {"message": f"{person.name} ({person.company.name})"}


class Person:
 def __init__(self, name, age):
    self.name = name
    self.age = age
    self.id = str(uuid.uuid4())
people = [Person("Tom", 38), Person("Bob", 42), Person("Sam", 28)]
# для поиска пользователя в списке people
def find_person(id):
 for person in people:
    if person.id == id:
         return person
 return None



@app.get("/api/users")
def get_people():
 return people

@app.get("/api/users/{id}")
def get_person(id):
 # получаем пользователя по id
 person = find_person(id)
 print(person)
 # если не найден, отправляем статусный код и сообщение об ошибке
 if person==None:
    return JSONResponse(
 status_code=status.HTTP_404_NOT_FOUND,
 content={ "message": "Пользователь не найден" }
 )
 #если пользователь найден, отправляем его
 return person

@app.post("/api/users")
def create_person(data = Body()):
 person = Person(data["name"], data["age"])
 # добавляем объект в список people
 people.append(person)
 return person

@app.put("/api/users")
def edit_person(data = Body()):
 # получаем пользователя по id
 person = find_person(data["id"])
 # если не найден, отправляем статусный код и сообщение об ошибке
 if person == None:
    return JSONResponse(
 status_code=status.HTTP_404_NOT_FOUND,
 content={ "message": "Пользователь не найден" }
 )
 # если пользователь найден, изменяем его данные и отправляем обратно клиенту
 person.age = data["age"]
 person.name = data["name"]
 return person

@app.delete("/api/users/{id}")
def delete_person(id):
 # получаем пользователя по id
 person = find_person(id)
 # если не найден, отправляем статусный код и сообщение об ошибке
 if person == None:
    return JSONResponse(
 status_code=status.HTTP_404_NOT_FOUND,
 content={ "message": "Пользователь не найден" }
 )
 # если пользователь найден, удаляем его
 people.remove(person)
 return person


# @app.post("/postdata")
# def postdata(username: str = Form(default ="Undefined", min_length=2,max_length=20),
#  userage: int =Form(default=18, ge=18, lt=111)):
#  return {"name": username, "age": userage}

@app.post("/postdata")
def postdata(username: str = Form(),
 languages: list =Form()):
 return {"name": username, "languages": languages}