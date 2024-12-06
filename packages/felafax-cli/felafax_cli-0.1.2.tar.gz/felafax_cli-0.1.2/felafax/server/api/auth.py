from fastapi import APIRouter, HTTPException, Request
from typing import Dict
from datetime import datetime

from ..handlers.user import UserHandler
from ..common import get_storage_provider, handle_error
from pydantic import BaseModel, EmailStr
from typing import Optional
import logging

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

# Models for request/response
class UserAuth(BaseModel):
    email: str
    name: Optional[str] = None

class TokenAuth(BaseModel):
    token: str

class UserResponse(BaseModel):
    user_id: str

class TokenResponse(BaseModel):
    token: str

class LoginResponse(BaseModel):
    user_id: str
    token: str

@router.post("/create_user", response_model=UserResponse)
async def create_user(auth: UserAuth):
    try:
        user_id = await UserHandler.create_user_id(auth.email)

        # Create user in storage
        storage_client = await get_storage_provider()
        user_handler = UserHandler(storage_client, user_id)
        await user_handler.create_new_user(auth.email, auth.name)
        
        logger.info(f"Successfully created user with ID: {user_id}")
        return {"user_id": user_id}
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise handle_error(e)

@router.post("/create_token", response_model=TokenResponse)
async def create_token(user_id: str):
    try:
        storage_client = await get_storage_provider()
        user_handler = UserHandler(storage_client, user_id)
        
        # Verify user exists
        user_info = await user_handler.get_user_info()
        if not user_info:
            raise HTTPException(status_code=404, detail="User not found")
            
        token = await user_handler.create_token()
        return {"token": token}
    except Exception as e:
        raise handle_error(e)
    
@router.post("/login", response_model=LoginResponse)
async def login(auth: TokenAuth):
    try:
        storage_client = await get_storage_provider()
        user_id = await UserHandler.find_user_id(auth.token, storage_client)
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {"user_id": user_id, "token": auth.token}
    except HTTPException:
        raise
    except Exception as e:
        raise handle_error(e)
