from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field, ValidationError, root_validator, validator, RootModel
from pydantic.types import conlist

def get_gmt7_time_str():
    return (datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%S")


######## user schemas ########

class UserSearch(BaseModel):

    is_admin: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
               "is_admin": None
            }
        }

class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool
    create_at: str = Field(default_factory=get_gmt7_time_str)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "password": "password",    
                "is_admin": False            
            }            
        }

class UserLogin(BaseModel):
    username: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "password",                
            }            
        }

class UserUpdate(BaseModel):

    class Config:
        json_schema_extra = {
            "example": {
                
            }            
        }


########### booking ##############

class BookingSearch(BaseModel):

    user_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
               "user_id": None
            }
        }

class BookingCreate(BaseModel):
    user_id: Optional[str] = None
    time_slot_start: datetime
    time_slot_end: datetime
    create_at: datetime = Field(default_factory=get_gmt7_time_str)

    class Config:
        json_schema_extra = {
            "example": {
                "time_slot_start": "2023-01-01 09:00:00",
                "time_slot_end": "2023-01-01 17:00:00",           
            }            
        }

class BookingUpdate(BaseModel):

    class Config:
        json_schema_extra = {
            "example": {
                "time_slot_start": "2023-01-01 09:00:00",
                "time_slot_end": "2023-01-01 17:00:00",  
            }            
        }
