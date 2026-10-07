from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from modelds.news import News
from modelds.news import Category

# 获取新闻分类
async def get_categories(db:AsyncSession,skip:int=0,limit:int=10):
    stet = select(Category).offset(skip).limit(limit)
    result = await db.execute(stet)
    return result.scalars().all()

# 获取指定分类的新闻列表
async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# 查询指定分类下的新闻数量
async def get_news_count(db:AsyncSession,category_id:int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalars().all()

# 获取新闻详情
async def get_news_detail(db:AsyncSession,news_id:int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalars().one_or_none()

# 浏览量+1
async def update_news_view_count(db:AsyncSession,news_id:int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

# 获取同类新闻
async def get_related_news(db:AsyncSession, news_id:int, category_id:int, limit:int=5):
    stmt = select(News).where(News.id != news_id).where(News.category_id == category_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
