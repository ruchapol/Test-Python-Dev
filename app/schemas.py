from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field, ValidationError, root_validator, validator, RootModel
from pydantic.types import conlist

def get_gmt7_time_str():
    # Get the current time in UTC, add 7 hours for GMT+7, and format as a string
    return (datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")


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
                "password": "testpassword",    
                "is_admin": False            
            }            
        }

class UserLogin(BaseModel):
    username: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "password": "testpassword",                
            }            
        }

class UserUpdate(BaseModel):
    user_id: str


    class Config:
        json_schema_extra = {
            "example": {
                
            }            
        }
