from pathlib import Path

import redis.asyncio as redis
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from middlewares import (BlackListMiddleware, CustomCORSMiddleware,
                         CustomHeaderMiddleware, UserAgentBanMiddleware,
                         WhiteListMiddleware)
from src.conf.config import config
from src.database.db import get_db
from src.routes import auth, contacts, users

app = FastAPI()

app.add_middleware(CustomHeaderMiddleware)  # noqa
app.add_middleware(CustomCORSMiddleware,  # noqa
                   origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )
# app.add_middleware(BlackListMiddleware)  # noqa
# app.add_middleware(WhiteListMiddleware) # noqa
# app.add_middleware(UserAgentBanMiddleware)  # noqa


BASE_DIR = Path(".")

app.mount("/static", StaticFiles(directory=BASE_DIR / "src" / "static"), name="static")

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=config.REDIS_DOMAIN, port=config.REDIS_PORT, db=0, password=config.REDIS_PASSWORD)
    await FastAPILimiter.init(r)


templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")  # noqa


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "target": "Go IT Students"})


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Database is configured correctly"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
