from fastapi import FastAPI
import psycopg
import redis
import os
from fastapi.responses import JSONResponse

USE_CACHE = os.getenv("USE_CACHE", "false").lower() == "true"

app = FastAPI()
try:
    db = psycopg.connect(os.getenv("POSTGRES_URI"))
except Exception as e:
    raise Exception("Could not connect to postgres!", e)

if USE_CACHE:
    cache = redis.Redis.from_url(os.getenv("REDIS_URI"))
    try:
        cache.ping()
    except Exception as e:
        raise Exception("Could not connect to redis!", e)


@app.get("/")
def home():
    return {"Hello": "World"}


@app.get("/db/{q}")
def sql_injection(q: str):
    result = src = None
    if USE_CACHE:
        result = cache.get(q)
        src = "redis"

    if not result:
        result = db.execute("SELECT (value) FROM important_data WHERE name=%s;", (q,)).fetchone()
        src = "database"

        if not result:
            return JSONResponse({"error": f"Could not find requested key", "key": q}, 404)

        result = result[0]
        if USE_CACHE:
            cache.set(q, result)

    return {"result": result, "source": src}
