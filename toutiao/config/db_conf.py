from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

# 数据库url
ASYNC_DATABASE_URL="mysql+aiomysql://root:123456@localhost:3306/news_db?charset=utf8mb4"

# 创建异步引擎
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, pool_size=10, max_overflow=20)

# 创建异步会话
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# 创建依赖项
async def get_db():
    async with async_session() as session:
        yield session
