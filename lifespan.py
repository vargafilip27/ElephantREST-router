from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
import asyncpg

from config import Settings

settings = Settings()

# Loading from an environment variable (.env)
DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@localhost{settings.DB_PORT}/{settings.DB_NAME}"

# Global variable to hold connection pool
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool

    # Create the connection pool
    db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)

    yield

    # Close the pool
    await db_pool.close()

# Initialize FastAPI with the lifespan
app = FastAPI(lifespan=lifespan)


from fastapi import Depends

async def get_db():
    if db_pool is None:
        raise Exception("Database pool is not initialized.")

    async with db_pool.acquire() as connection:
        yield connection
