from passlib.context import CryptContext
from sqladmin.authentication import AuthenticationBackend
from app.db.session import get_session
from sqlalchemy import select
from app.db.models import User
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(e)
        return False



class MyAuth(AuthenticationBackend):
    async def login(self, request):
        data = await request.form()
        try:
            print(data)
            async with get_session() as db:
                async with db.begin():
                    query= select(User)
                    res=await db.execute(query)
                    res= res.scalars().all()
                    for ress in res:
                        print(ress)
                    
                    

            return True
        except Exception as e:
            print(e)  
            return False
        

    async def logout(self, request):
        return True

    async def authenticate(self, request):
        return False

