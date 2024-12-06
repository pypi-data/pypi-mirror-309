from setuptools import setup
from pg_common import VERSION

DIST_NAME = "pg_common"
__author__ = "baozilaji@gmail.com"

setup(
    name=DIST_NAME,
    version=VERSION,
    description="python game: common lib",
    packages=['pg_common'],
    author=__author__,
    python_requires='>=3.9',
    install_requires=[
        'sshtunnel==0.4.0',
        'redis==4.6.0',
        'prettytable==3.9.0',
        'aiohttp==3.8.6',
        'aiodns==3.1.1',
        'pycryptodome==3.19.0',
        'pymysql==1.1.0',
        'pymongo==4.7.2',
        'requests==2.28.2',
        'pydantic==1.10.11',
    ]
)
