from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from app.db.enums import Status

#data validation schemas here
class ContactForm(BaseModel):
    name:str
    email:EmailStr
    message:str
    subject:str
    status:Status


class InternshipBase(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    apply_link: Optional[str] = None
    is_remote: Optional[bool] = False

class InternshipCreate(InternshipBase):
    pass

class InternshipUpdate(InternshipBase):
    pass

class InternshipOut(InternshipBase):
    id: int
    model_config=ConfigDict(from_attributes=True)

