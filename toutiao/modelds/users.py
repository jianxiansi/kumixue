from datetime import datetime
from sqlalchemy import Index, Integer, String, SmallInteger, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    __table_args__ = (
        Index("phone_UNIQUE", "phone"),
        Index("username_UNIQUE", "username"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False, default='')
    avatar: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    email: Mapped[str] = mapped_column(String(100), nullable=False, default='')
    phone: Mapped[str] = mapped_column(String(20), nullable=False, default='')
    gender: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    bio: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    status: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

class User_token(Base):
    __tablename__ = "user_token"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("user.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(255), nullable=False, comment="令牌")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
