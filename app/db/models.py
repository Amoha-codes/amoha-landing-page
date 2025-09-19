
from sqlalchemy.orm import declarative_base,Mapped,mapped_column
from app.db.enums import Status
from sqlalchemy import String,Integer,DateTime,Float,func,Boolean,ForeignKey,Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from pathlib import Path
Base = declarative_base()
base_path = Path(__file__).resolve().parent
storage = FileSystemStorage("./static/assests/img")

#orm models defined here these model will talk with db 
class Contact(Base):
    __tablename__ = "contacts"
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    name:Mapped[str] = mapped_column(String,nullable= False)
    subject:Mapped[str] = mapped_column(String,nullable= False)
    email:Mapped[str] = mapped_column(String,nullable= False)
    message:Mapped[str] = mapped_column(String,nullable= False)
    status:Mapped[Status] =mapped_column(Enum(Status),default=Status.NEW.name)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now(),onupdate=func.now(),server_onupdate=func.now())
    deleted_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class Internships(Base):
    __tablename__ = "internships"
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    name:Mapped[str] = mapped_column(String,nullable= False)
    description:Mapped[str] = mapped_column(String,nullable= False)
    pay:Mapped[float] = mapped_column(Float,nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now(),onupdate=func.now(),server_onupdate=func.now())
    deleted_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    name:Mapped[str] = mapped_column(String,nullable= False)
    email:Mapped[str] = mapped_column(String,nullable=False,unique=True)
    password:Mapped[str] = mapped_column(String,nullable=False)
    status:Mapped[bool] = mapped_column(Boolean,nullable=False,default=True)
    is_admin:Mapped[bool] = mapped_column(Boolean,nullable=False,default=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now(),onupdate=func.now(),server_onupdate=func.now())
    deleted_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class AuthTokens(Base):
    __tablename__ = 'auth_tokens'
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    token:Mapped[str] = mapped_column(String,nullable= False)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'),nullable=False)
    users:Mapped[User] = relationship(User,lazy='selectin',cascade="delete")
    expiry:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now(),onupdate=func.now(),server_onupdate=func.now())
    deleted_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)


class Courses(Base):
    __tablename__="courses"
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    name:Mapped[str] = mapped_column(String,nullable= False)
    description:Mapped[str] = mapped_column(String,nullable = False)
    image:Mapped[str] = mapped_column(FileType(storage=storage),nullable=False)
    icon:Mapped[str] = mapped_column(String,nullable=False,server_default="/static/assest/images/c.png")
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now(),onupdate=func.now(),server_onupdate=func.now())
    deleted_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)