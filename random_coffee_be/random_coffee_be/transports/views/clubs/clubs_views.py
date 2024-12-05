from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from ..models.user import User
from ..depends import get_db

router = APIRouter()

clubs = [
    "Dota 2",
    "CS2",
    "Genshin Impact",
    "HonkaiStarRail",
    "Tet-a-tet",
    "ZZZ",
    "Valorant",
    "Mobile Legends",
    "ToF",
    "WutheringWaves"
]

@router.get("/clubs", response_model=List[str])
async def get_clubs():
    return clubs

@router.post("/clubs/join", response_model=dict)
async def join_club(user_id: int, club: str, db: AsyncSession = Depends(get_db)):
    if club not in clubs:
        raise HTTPException(status_code=404, detail="Club not found")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if club in user.clubs:
        raise HTTPException(status_code=400, detail="User already in club")

    user.clubs.append(club)
    await db.commit()
    return {"detail": f"User joined {club}"}

@router.post("/clubs/leave", response_model=dict)
async def leave_club(user_id: int, club: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if club not in user.clubs:
        raise HTTPException(status_code=400, detail="User not in club")

    user.clubs.remove(club)
    await db.commit()
    return {"detail": f"User left {club}"}