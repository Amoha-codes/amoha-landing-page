from fastapi import FastAPI,HTTPException,Form,Depends
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db.schemas import ContactForm
from app.db.models import Contact
from app.db.session import get_session,init_db,engine
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqladmin import Admin,ModelView
from app.db.models import Contact,Internships

try:
    templates = Jinja2Templates('./app/templates/')
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
admin = Admin(app,engine)

class ContactView(ModelView,model=Contact):
    column_list=['id','name','subject','message','created_at']
    column_labels={'created_at':'date'}
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

class InternshipView(ModelView,model=Internships):
    column_list=['id','name','description','pay']
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    

admin.add_view(ContactView)
admin.add_view(InternshipView)


app.mount('/static',StaticFiles(directory="app\\static"),name="static")

@app.get("/")
async def get_home(request:Request):
    try:
        return templates.TemplateResponse(
            request,"index.html"
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
                name=name,email=email,subject=subject,message=message
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
    uvicorn.run("main:app",port=8080)


