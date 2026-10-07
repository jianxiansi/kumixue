from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.users import get_user_by_username, create_user, create_token
from schemas.users import UserRequest

router = APIRouter(prefix="/api/users", tags=["users"])

# 注册用户
@router.post("/register")
async def register_user(user_date: UserRequest, db:AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_username(db, user_date.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = await create_user(db, user_date)
    token = await create_token(db, user.id)
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token":token,
            "userinfo":{
                "id": user.id,
                "username": user.username,
                "bio":user.bio,
                "avatar":user.avatar
            }
        }
    }
