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
