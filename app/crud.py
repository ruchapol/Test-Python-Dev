
from datetime import datetime
from typing import Any, Dict, List, Optional

import time 
from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException
from .schemas import *
from .model import *

# from app.dependencies import get_db


class UserCrud:

    def __init__(self, ): # type: ignore
        self.db = {"001": 
            {
                "id": "001",
                "username": "admin",
                "password": "password",
                "is_admin": True,
                "create_at": "2023-01-01T00:00:00"
            },
            "002": 
            {
                "id": "002",
                "username": "usertest001",
                "password": "password",
                "is_admin": False,
                "create_at": "2023-01-01T00:01:00"
            }
        }

    def create(self, createModel: UserCreate):
        id = int(time.time())
        createModel_dict = createModel.model_dump()
        createModel_dict["id"] = str(id)
        self.db[str(id)] = createModel_dict       
        return str(id)

    def get_by_id(self, id: str) -> UserModel:
        if id not in self.db:
            raise HTTPException(status_code=404, detail="User not found")
        return self.db[id]
    
    def get_by_username(self, username: str) -> UserModel:
        for id, user in self.db.items():
            if user['username'] == username:
                return user
        raise HTTPException(status_code=404, detail="User not found")

    def get_list(self, searchModel: UserSearch) -> List[UserModel]:
        
        result = self.db
        if searchModel.is_admin is not None:
            result = {id: user for id, user in result.items() if user['is_admin'] == searchModel.is_admin} 
        return list(result.values())
    
    def get_all(self) -> List[UserModel]:
         
        return list(self.db.values())

    def update(self, id: str, update: UserUpdate) -> UserModel:
        
        if id not in self.db:
            raise HTTPException(status_code=404, detail="User not found")
        
        old_data = self.db[id]
    
        self.db[id] = UserModel(
            id = old_data["id"],
            username = old_data["username"],
            password = old_data["password"],
            is_admin = old_data["is_admin"],
            create_at = old_data["create_at"],
        ).model_dump()      
    
        self.db[id] = UserModel(**self.db[id], **update.dict()).model_dump()   

        return UserModel(**self.db[id])

    def delete(self, id: str):
        if id not in self.db:
            raise HTTPException(status_code=404, detail="User not found")
        del self.db[id]
        return True


class BookingCrud:

    def __init__(self, ): # type: ignore
        self.db = self.db = {"0001": 
            {
                "id": "0001",
                "user_id": "001",
                "time_slot_start": "2023-01-01T09:00:00",
                "time_slot_end": "2023-01-01T17:00:00",
                "create_at": "2023-01-01T00:00:00"
            },
            "0002": 
            {
                "id": "0002",
                "user_id": "001",
                "time_slot_start": "2023-01-02T09:00:00",
                "time_slot_end": "2023-01-02T17:00:00",
                "create_at": "2023-01-02T00:00:00"
            },
            "0003": 
            {
                "id": "0003",
                "user_id": "002",
                "time_slot_start": "2023-01-01T09:00:00",
                "time_slot_end": "2023-01-01T17:00:00",
                "create_at": "2023-01-01T00:00:00"
            },
            "0004": 
            {
                "id": "0004",
                "user_id": "002",
                "time_slot_start": "2023-01-02T09:00:00",
                "time_slot_end": "2023-01-02T17:00:00",
                "create_at": "2023-01-02T00:00:00"
            }
        }

    def create(self, createModel: BookingCreate):
        id = int(time.time())
        createModel_dict = createModel.model_dump()
        createModel_dict["id"] = str(id)
        self.db[str(id)] = createModel_dict       
        return str(id)

    def get_by_id(self, id: str) -> BookingModel:
        if id not in self.db:
            raise HTTPException(status_code=404, detail="Booking not found")
        return BookingModel(**self.db[id])
    

    def get_list(self, searchModel: BookingSearch) -> List[BookingModel]:
        result = self.db

        print("get_list: searchModel", searchModel)

        print("get_list: result", result)

        if searchModel.user_id is not None:
            result = {id: booking for id, booking in result.items() if booking['user_id'] == searchModel.user_id} 
            print("get_list: result", result)
        
        return list(result.values())
    
    def get_all(self) -> List[BookingModel]:
         
        return (self.db.values())

    def update(self, id: str, update: BookingUpdate) -> BookingModel:
        
        if id not in self.db:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        old_data = self.db[id]
    
        self.db[id] = BookingModel(
            id = old_data["id"],
            user_id = old_data["user_id"],
            time_slot_start = update.time_slot_start if update.time_slot_start is not None else old_data["time_slot_start"],
            time_slot_end = update.time_slot_end if update.time_slot_end is not None else old_data["time_slot_end"],
            create_at = old_data["create_at"],
        ).model_dump()      

        return self.db[id]

    def delete(self, id: str):
        if id not in self.db:
            raise HTTPException(status_code=404, detail="Booking not found")
        del self.db[id]
        return True