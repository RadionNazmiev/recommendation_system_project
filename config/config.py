import os

from dotenv import load_dotenv

from config.utils import load_config


load_dotenv()

PG_USER = os.getenv('PG_USER')
PG_PASS = os.getenv('PG_PASS')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')


if __name__ == "__main__":
    from yaml import safe_load

    d = load_config(os.path.join("config", "config.yaml"))
    print(d)
    print(PG_USER)
    
