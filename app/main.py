from routes import setupRouter
from aiohttp import web
from tortoise import Tortoise, run_async
from models import *
import asyncio
import aio_pika


async def db_setup(app):
    await Tortoise.init(
        db_url='sqlite://../db/db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


async def broker_setup(app):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/"
    )
    print("Connected to: ", connection)
    async with connection:
        queue_name = "test_queue"

        # Creating channel
        channel = await connection.channel()    # type: aio_pika.Channel

        # Declaring queue
        queue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )   # type: aio_pika.Queue

        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                async with message.process():
                    print(message.body)

                    if queue.name in message.body.decode():
                        break


async def start_background_tasks(app):
    app['broker_setup'] = asyncio.create_task(broker_setup(app))


async def cleanup_background_tasks(app):
    app['broker_setup'].cancel()
    await app['broker_setup']

if __name__ == '__main__':
    app = web.Application()
    app.on_startup.append(db_setup)
    setupRouter(app)
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    web.run_app(app)
