from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
import asyncpg

# Loading from an environment variable (.env)
DATABASE_URL = # TODO

# Global variable to hold our connection pool
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_pool

    # Create the connection pool
    print("Connecting to PostgreSQL...")
    db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)

    yield  # The FastAPI app runs while paused here

    # Close the pool
    print("Closing PostgreSQL connection...")
    await db_pool.close()

# Initialize FastAPI with the lifespan
app = FastAPI(lifespan=lifespan)
