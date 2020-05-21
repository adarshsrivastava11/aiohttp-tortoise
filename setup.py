from setuptools import setup


install_requires = [
    'aiohttp',
    'tortoise-orm',
    'asyncpg',
    'aiosqlite'
]

setup(
    name='aiohttp-tortoise',
    version='0.1',
    install_requires=install_requires,
)
