
from datetime import datetime, timedelta
from fastapi import HTTPException

from passlib.context import CryptContext
from sqladmin.authentication import AuthenticationBackend
from app.db.session import async_session
from sqlalchemy import select
from app.db.models import User, AuthTokens

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
import secrets

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(e)
        return False

def generate_token(length=None)->str:
    return secrets.token_urlsafe(length) if length else secrets.token_urlsafe()

class MyAuth(AuthenticationBackend):
    async def login(self, request):
        data = await request.form()
        try:
            email = data.get('username')
            password = data.get('password')
            print(email,password)
            async with async_session() as db:
                async with db.begin():
                    query= select(User).where(User.email == email).limit(1)
                    res=await db.execute(query)
                    res= res.scalars().first()
                    if res:
                        if not verify_password(password, res.password):
                            return False
                        if not res.status:
                            return False
                        token = generate_token()
                        auth_token= AuthTokens(
                            token=token,
                            expiry=datetime.now()+timedelta(minutes=30),
                            user_id=res.id,
                        )
                        db.add(auth_token)
                        request.session.update({'token': token})
                        return True
                    else:
                        return False

        except Exception as e:
            print(e)  
            return False
        

    async def logout(self, request):
        request.session.clear()
        return True

    async def authenticate(self, request):
        try:
            token = request.session.get('token')
            async with async_session() as db:
                async with db.begin():
                    query= select(AuthTokens).where(AuthTokens.token == token).limit(1)
                    res=await db.execute(query)
                    res= res.scalars().first()
                    if res:
                        return True
                    else:
                        return False

        except Exception as e:
            print(e)
            return False

