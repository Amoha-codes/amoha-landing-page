from sqlalchemy.orm import declarative_base,Mapped,mapped_column

from sqlalchemy import String,Integer,DateTime,Float,func
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
    email:Mapped[str] = mapped_column(String,nullable= False)
    message:Mapped[str] = mapped_column(String,nullable= False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(),server_default=func.now(),onupdate=func.now(),server_onupdate=func.now())
    deleted_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
