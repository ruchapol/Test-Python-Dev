
from datetime import datetime
from typing import Any, Dict, List, Optional

import time 
from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException
from .schemas import *
from .model import *


class UserCrud:

    def __init__(self, ): # type: ignore
        self.db = {"001": 
            {
                       "username": "admin",
                       "password": "admin",
                       "is_admin": True,
                       "create_at": "2023-01-01 00:00:00"
            }
        }

    def create(self, createModel: UserCreate):
        id = int(time.time())
        self.db[id] = createModel.dict()       
        return id

    def get_by_id(self, id: int) -> UserModel:
        if id not in self.db:
            raise HTTPException(status_code=404, detail="User not found")
        return self.db[id]
    
    def get_by_username(self, username: str) -> UserModel:
        for id, user in self.db.items():
            if user['username'] == username:
                return user
        raise HTTPException(status_code=404, detail="User not found")

    def get_list(self, searchModel: UserSearch) -> List[UserModel]:
        return self.db
    
    def get_all(self) -> List[UserModel]:

        return []

    async def update(self, id: int, update: UserUpdate):
        
        return {}

    async def delete(self, id: str):
        return True
