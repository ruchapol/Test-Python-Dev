from datetime import datetime
from typing import List, Tuple
from pydantic import BaseModel, ValidationError, validator, Field


class UserModel(BaseModel):
    id: str
    username: str
    password: str
    create_at: datetime
    is_admin: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": "001",
                "username": "testuser",
                "password": "testpassword",
                "is_admin": True,
                "create_at": "2023-01-01 00:00:00"
            }            
        }

class BookingModel(BaseModel):
    id: str
    user_id: str
    time_slot_start: datetime
    time_slot_end: datetime
    create_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "001",
                "user_id": "001",
                "time_slot_start": "2023-01-01 09:00:00",
                "time_slot_end": "2023-01-01 17:00:00",
                "create_at": "2023-01-01 00:00:00"
            }            
        }

class TokenData(BaseModel):
    username: str | None = None
    is_admin: bool | None = None

