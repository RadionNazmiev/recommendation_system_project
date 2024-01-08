import os

from dotenv import load_dotenv

from config.utils import load_config


load_dotenv()

PG_USER = os.getenv('PG_USER')
PG_PASS = os.getenv('PG_PASS')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')
