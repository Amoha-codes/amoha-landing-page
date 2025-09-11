from sqlalchemy.orm import declarative_base,Mapped,mapped_column

from sqlalchemy import String,Integer,DateTime,Float,func,Boolean
from datetime import datetime

Base = declarative_base()

#orm models defined here these model will talk with db 
class Contact(Base):
    __tablename__ = "contacts"
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,index=True)
    name:Mapped[str] = mapped_column(String,nullable= False)
    subject:Mapped[str] = mapped_column(String,nullable= False)
    email:Mapped[str] = mapped_column(String,nullable= False)
    message:Mapped[str] = mapped_column(String,nullable= False)
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

