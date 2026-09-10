import uuid
from datetime import timedelta, datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modelds.users import User_token, User
from schemas.users import UserRequest
from utils.security import get_password_hash


# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_date:UserRequest):
    # 加密处理
    hashed_password = get_password_hash(user_date.password)
    user = User(username=user_date.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # 从数据库中获取最新数据
    return user

# 生成Token
async def create_token(db: AsyncSession, user_id: int):
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(User_token).where(User_token.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
        await db.commit()
    else:
        user_token = User_token(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()

    return token