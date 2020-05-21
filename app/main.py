from routes import setupRouter
from aiohttp import web
from tortoise import Tortoise, run_async
from models import *
import asyncio


async def db_setup(app):
    await Tortoise.init(
        db_url='sqlite://../db/db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()

if __name__ == '__main__':
    app = web.Application()
    app.on_startup.append(db_setup)
    setupRouter(app)
    web.run_app(app)
