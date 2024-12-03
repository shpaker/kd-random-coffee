from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory data stores
users = {}
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

# Data models
class User(BaseModel):
    tg_id: int
    name: str
    ready_status: bool = False
    clubs: List[str] = []

@app.post("/user")
async def create_user(user: User):
    users[user.tg_id] = user
    return {"detail": "User created successfully"}

@app.get("/user")
async def get_user(tg_id: int):
    if tg_id in users:
        return users[tg_id]
    else:
        raise HTTPException(status_code=404, detail="Гнида не найдена")

@app.get("/clubs")
async def get_club():
    return clubs

@app.post("/club/join")
async def join_club(tg_id: int, club: str):
    if tg_id in users:
        if club in clubs:
            if club in users[tg_id].clubs:
                raise HTTPException(status_code=400, detail="Пользователь уже находится в клубе")
            users[tg_id].clubs.append(club)
            return{"detail": f"The user appeared in the {club}"}
        raise HTTPException(status_code=404, detail="Клуб не найден")
    raise HTTPException(status_code=404, detail="Гнида не найдена")

@app.post("/club/leave")
async def leave_club(tg_id: int, club: str):
    if tg_id in users:
        if club in users[tg_id].clubs:
            users[tg_id].clubs.remove(club)
            return{"detail": f"The user removed in the {club}"}
        else:
            raise HTTPException(status_code=404, detail="Пользователь не находится в клубе")
    raise HTTPException(status_code=404, detail="Гнида не найдена")
