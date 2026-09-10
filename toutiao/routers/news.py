from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import news

# 创建APIRouter实例
router = APIRouter(prefix="/api/news", tags=["news"])

# 获取新闻分类
@router.get("/categories")
async def get_news_categories(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db,skip, limit)
    return {
        "code": 200,
        "msg": "获取分类成功",
        "data": categories
    }

# 获取新闻列表
@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize",le=100),
        db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    has_more = total > offset + len(news_list)
    return {
        "code": 200,
        "msg": "获取新闻列表成功",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }

# 获取新闻详情
@router.get("/detail")
async def get_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    news_detail = await news.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="News not found")

    await news.update_news_view_count(db, news_detail.id)

    related_news = await news.get_related_news(db, news_detail.id, news_detail.category_id)

    return {
        "code": 200,
        "msg": "获取新闻详情成功",
        "data": news_detail,
        "relatedNews": related_news
    }
