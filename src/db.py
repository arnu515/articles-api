from os import getenv

from prisma import Client

db = Client(log_queries=bool(getenv("DEBUG")))
