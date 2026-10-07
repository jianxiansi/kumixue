from typing import Optional

from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
import datetime
from sqlalchemy import DateTime, func, Integer, String, Index, Text, ForeignKey


# 创建基类
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),comment="创建时间")

# 创建分类模型类
class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True,comment="分类ID")
    name: Mapped[str] = mapped_column(String(50),unique=True,nullable=False,comment="分类名称")
    sort: Mapped[int] = mapped_column(Integer,nullable=False,comment="分类排序")

    def __repr__(self):
        return f"<Category(id={self.id},name={self.name},sort={self.sort})>"

# 创建新闻模型类
class News(Base):
    __tablename__ = "news"

    # 创建索引：提升查询速度
    __table_args__ = (
        Index('fk_news_category_idx', 'category_id'),
        Index('idx_publish_time', 'publish_time')
    )
    create_time = None
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("news_category.id"), comment="分类ID")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="新闻标题")
    author: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="作者")
    source: Mapped[Optional[str]] = mapped_column(String(64), default="", comment="新闻来源")
    summary: Mapped[Optional[str]] = mapped_column(String(500), default="", comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    publish_time: Mapped[datetime] = mapped_column(DateTime, comment="发布时间")
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="状态：1正常")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"
