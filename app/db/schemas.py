from pydantic import BaseModel,EmailStr


#data validation schemas here
class ContactForm(BaseModel):
    name:str
    email:EmailStr
    message:str
    subject:str


