from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.db import get_db
from app.utils.utils import MyAuth

# from app.MyAuth import get_current_admin


from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import schemas, crud_async   # assume you wrote async CRUD helpers
from app.db.session import get_session   # yields AsyncSession
from app.utils.utils import get_current_admin

router = APIRouter(prefix="/internships", tags=["internships"])

@router.post("/", response_model=schemas.InternshipOut)
async def create_internship(
    internship_in: schemas.InternshipCreate,
    db: AsyncSession = Depends(get_session),
    admin = Depends(get_current_admin)
):
    return await crud_async.create_internship(db, internship_in)

@router.get("/", response_model=List[schemas.InternshipOut])
async def list_internships(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_session)):
    return await crud_async.list_internships(db, skip=skip, limit=limit)

@router.get("/{internship_id}", response_model=schemas.InternshipOut)
async def get_internship(internship_id: int, db: AsyncSession = Depends(get_session)):
    obj = await crud_async.get_internship(db, internship_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.put("/{internship_id}", response_model=schemas.InternshipOut)
async def update_internship(
    internship_id: int,
    internship_in: schemas.InternshipUpdate,
    db: AsyncSession = Depends(get_session),
    admin = Depends(get_current_admin)
):
    updated = await crud_async.update_internship(db, internship_id, internship_in.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Not found")
    return updated

@router.delete("/{internship_id}")
async def delete_internship(
    internship_id: int,
    db: AsyncSession = Depends(get_session),
    admin = Depends(get_current_admin)
):
    ok = await crud_async.delete_internship(db, internship_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {"ok": True}
