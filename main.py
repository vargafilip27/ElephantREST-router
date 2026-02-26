import asyncpg
from fastapi import FastAPI, HTTPException, Response

from config import Settings

app = FastAPI()


#@app.get("/")
#async def root():
#    return {"message": "Hello World"}


#@app.get("/hello/{name}")
#async def say_hello(name: str):
#    return {"message": f"Hello {name}"}

@app.get("/{table_name}")
async def select_all(table_name: str):
    settings = Settings()
    DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@localhost{settings.DB_PORT}/{settings.DB_NAME}"

    query = "SELECT select_all($1)"

    conn = await asyncpg.connect(DATABASE_URL)
    json_result = conn.fetch(query, table_name)

    if not json_result:
        raise HTTPException(404, "Not Found")

    return Response(content=json_result, media_type="application/json")
