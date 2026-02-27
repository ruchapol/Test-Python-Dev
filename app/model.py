"""
request/response body files

"""
from datetime import datetime
from typing import List, Tuple
from pydantic import BaseModel, ValidationError, validator, Field


class UserModel(BaseModel):
    _id: int
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "password": "testpassword"
            }            
        }
