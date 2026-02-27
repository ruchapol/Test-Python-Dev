from fastapi import APIRouter, Body, Depends,BackgroundTasks
from fastapi.responses import StreamingResponse
from .crud import *
from fastapi import HTTPException, status
from fastapi.security import APIKeyHeader

from datetime import datetime
from typing import List, Optional
from .database import user_crud, booking_crud
from .schemas import *
from jose import JWTError, jwt
from pwdlib import PasswordHash
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

password_hash = PasswordHash.recommended()

api_key_header = APIKeyHeader(name="Authorization") 
router = APIRouter()

print("password hash example", password_hash.hash("password"))


############## User API ##############

@router.post("/user/list", tags=["user"])
async def user_list(searchModel: UserSearch):
    data = user_crud.get_list(searchModel=searchModel)
    return {
        "data": data,
    }

@router.get("/user/me", tags=["user"])
async def user_get_me(token: str = Depends(api_key_header)):
    current_user = get_current_user(token=token)
    return {
        "data": current_user
    }

@router.get("/user/{id}", tags=["user"])
async def user_get_by_id(id: str):
    data = user_crud.get_by_id(id=id)
    return {
        "data": data,
    }

@router.post("/user/", tags=["user"])
async def user_create(createModel: UserCreate):
    createModel.password = get_password_hash(createModel.password)
    data = user_crud.create(createModel=createModel)
    return {
        "data": data,
    }

@router.put("/user/{id}", tags=["user"])
async def user_edit(updateModel: UserUpdate, id: str):
    data = user_crud.update(id=id, update=updateModel)
    return {
        "success": True,
        "data": data.model_dump()
    }

@router.delete("/user/{id}", tags=["user"])
async def user_delete(id: str):
    await user_crud.delete(id=id)
    return {
        "success": True
    }

@router.post("/user/login", tags=["user"])
async def user_login(userLoginModel: UserLogin):
    """
    user 1:
    username: admin password: password 

    user 2:
    username: usertest001 password: password
    """

    data = user_crud.get_by_username(userLoginModel.username)
    if not verify_password(userLoginModel.password, data['password']):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    access_token = create_access_token(
            data={"username": userLoginModel.username}, expires_delta=access_token_expires
        )

    return {
        "data": data,
        "accessToken": access_token
    }


############## Booking API ##############

@router.post("/booking/list", tags=["booking"])
async def booking_list(searchModel: BookingSearch, token: str = Depends(api_key_header)):
    current_user = get_current_user(token=token)

    data = []
    if current_user.is_admin:
        data = booking_crud.get_list(searchModel=searchModel)
    else:
        searchModel.user_id = current_user.id
        data = booking_crud.get_list(searchModel=searchModel)

    return {
        "data": data
    }


@router.get("/booking/{id}", tags=["booking"])
async def booking_get_by_id(id: str, token: str = Depends(api_key_header)):
    current_user = get_current_user(token=token)
    data = booking_crud.get_by_id(id=id)
    if data.user_id != current_user.id and current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Not authorized to access this booking")

    return {
        "data": data.model_dump(),
    }

@router.post("/booking/", tags=["booking"])
async def booking_create(createModel: BookingCreate, token: str = Depends(api_key_header)):
    current_user = get_current_user(token=token)
    
    createModel.user_id = current_user.id
    data = booking_crud.create(createModel=createModel)
    return {
        "data": data,
    }

@router.put("/booking/{id}", tags=["booking"])
async def booking_edit(updateModel: BookingUpdate, id: str, token: str = Depends(api_key_header)):
    current_user = get_current_user(token=token)
    
    data = booking_crud.get_by_id(id=id)
    if current_user.is_admin == False and data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this booking")
    
    data = booking_crud.update(id=id, update=updateModel)
    
    return {
        "success": True,
        "data": data
    }

@router.delete("/booking/{id}", tags=["booking"])
async def booking_delete(id: str, token: str = Depends(api_key_header)):
    current_user = get_current_user(token=token)

    booking_crud.delete(id=id)
    return {
        "success": True
    }


##############################################

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str) -> UserModel:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = user_crud.get_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return UserModel(**user)