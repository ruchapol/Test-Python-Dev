import os
import io
from fastapi import APIRouter, Body, Depends,BackgroundTasks
from fastapi.responses import StreamingResponse
from numpy import ndarray
from .crud import *
from fastapi import HTTPException
from fastapi.responses import FileResponse
from datetime import datetime
from typing import List, Optional
from .database import user_crud
from .schemas import *
from jose import JWTError, jwt
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

  
router = APIRouter()


@router.post("/user/list")
async def user_list(searchModel: UserSearch):
    data = user_crud.get_list(searchModel=searchModel)
    return {
        "data": data,
    }

@router.post("/user/")
async def user_create(createModel: UserCreate):
    data = user_crud.create(createModel=createModel)
    return {
        "data": data,
    }

@router.put("/user/{id}")
async def user_edit(updateModel: UserUpdate, id: int):
    data = user_crud.update(id=id, update=updateModel)
    return {
        "success": True,
        "data": data
    }

@router.delete("/user/{id}")
async def user_delete(id: int):
    await user_crud.delete(id=id)
    return {
        "success": True
    }

@router.post("/user/login")
async def user_login(userLoginModel: UserLogin):
    data = user_crud.get_by_username(userLoginModel.username)
    if data['password'] != userLoginModel.password:
        raise HTTPException(status_code=400, detail="Invalid password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    access_token = create_access_token(
            data={"username": userLoginModel.username}, expires_delta=access_token_expires
        )

    return {
        "data": data,
        "accessToken": access_token
    }


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt