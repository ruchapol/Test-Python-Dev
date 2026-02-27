import sys
from fastapi import HTTPException
from .crud import  UserCrud

# Instantiate CRUD classes with the MongoDB connection
user_crud = UserCrud()
