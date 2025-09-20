from app.db.enums import Status
from fastapi import FastAPI,HTTPException,Form,Depends
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db.schemas import ContactForm
from app.db.models import Contact
from app.db.session import get_session,init_db,engine,async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqladmin import Admin,ModelView
from app.db.models import Contact,Internships,User,Courses
from app.utils.utils import MyAuth, hash_password
from datetime import datetime
from sqlalchemy import select
from pathlib import Path
import os
# 

from fastapi import FastAPI, HTTPException

app = FastAPI()

# Dummy course database
courses = {
    1: {"id": 1, "title": "Python Basics", "description": "Learn Python from scratch"},
    2: {"id": 2, "title": "FastAPI Mastery", "description": "Build APIs with FastAPI"},
    3: {"id": 3, "title": "Data Science 101", "description": "Intro to Data Science"}
}

@app.get("/")
def read_root():
    return {"message": "Welcome to Amoha Landing Page API"}

@app.get("/courses")
def get_courses():
    return {"courses": list(courses.values())}

@app.get("/courses/{course_id}")
def get_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]


# 

Base_path = Path(__file__).resolve().parent
print(Base_path)

try:
    templates = Jinja2Templates((Base_path/"app"/"templates").__str__())
except Exception as e:
    raise e

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        yield

    except Exception as e:
        print(str(e))

app = FastAPI(lifespan=lifespan)
admin = Admin(app,engine,authentication_backend=MyAuth(secret_key="test"))
# admin = Admin(app,engine)

class ContactView(ModelView,model=Contact):
    column_list=['id','name','subject','message','created_at']
    column_labels={'created_at':'date'}
    form_edit_rules=['status']
    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True

class InternshipView(ModelView,model=Internships):
    column_list=['id','name','description','pay']
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

class UserView(ModelView,model=User):
    column_list=[User.id,User.name,User.email,User.is_admin,User.status,User.created_at,User.updated_at]
    form_edit_rules = ['name','email','status','is_admin']
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    async def on_model_change(self, data, model, is_created, request):
        try:
            print(data)
            if is_created:
                data['password'] = hash_password(data['password'])
        except Exception as e:
            print(e)
    
class CourseView(ModelView,model=Courses):
    column_list=[Courses.id,Courses.name,Courses.description,Courses.image,Courses.created_at,Courses.updated_at]
    form_edit_rules = ['name','description','image']
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True





    

admin.add_view(ContactView)
admin.add_view(InternshipView)
admin.add_view(UserView)
admin.add_view(CourseView)

# 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

print(BASE_DIR)
print(STATIC_DIR)

# 
app.mount('/static',StaticFiles(directory="app//static"),name="static")

@app.get("/")
async def get_home(request:Request,db:AsyncSession=Depends(get_session)):
    try:
        async with db:
            query = select(Courses)
            courses= await db.execute(query)
            courses = courses.scalars().all()
            
        return templates.TemplateResponse(
            request,"index.html",
            context={
                'courses':courses
            }
            
        )
    except Exception as e:
        print(e)
        raise HTTPException(500,"Internal server error")

@app.post("/contact")
async def post_contact(name:str= Form(),email:str=Form(),subject:str=Form(),message:str=Form(),db:AsyncSession=Depends(get_session)):
    async with db.begin():
        try:
            #validating the data using pydantic
            data_model = ContactForm(
                name=name,email=email,subject=subject,message=message,status=Status.NEW.name
            )
            #inserting data into contact orm model
            data_in_db = Contact(
                **data_model.model_dump()
            )
            #adding the instance to session 
            db.add(data_in_db)
            await db.flush()
            print(name,email,subject,message)
            return "OK"
        except Exception as e:
            print(e)
            raise HTTPException(400,"Bad request")
if __name__ == "__main__":
    import uvicorn
    from app.utils.config import get_settings
    settings=get_settings()
    uvicorn.run("main:app",port=settings.PORT,host=settings.HOST)


