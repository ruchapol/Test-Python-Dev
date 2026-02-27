
from datetime import datetime
from typing import Any, Dict, List, Optional

import time 
from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException
from .schemas import *
from .model import *


class UserCrud:

    def __init__(self, ): # type: ignore
        self.db = {}

    def create(self, createModel: UserCreate):
        id = int(time.time())
        self.db[id] = createModel.dict()       
        return id

    def get_by_id(self, id: int) -> UserModel:
        return {}

    def get_list(self, searchModel: UserSearch) -> List[UserModel]:
        return self.db
    
    def get_all(self) -> List[UserModel]:

        return []

    async def update(self, id: int, update: UserUpdate):
        
        return {}

    async def delete(self, id: str):
        return True
