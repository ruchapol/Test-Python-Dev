import sys
from fastapi import HTTPException
from .crud import  BookingCrud, UserCrud


user_crud = UserCrud()
booking_crud = BookingCrud()