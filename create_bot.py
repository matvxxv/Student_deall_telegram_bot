from dataclasses import dataclass
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@dataclass
class Bot:
    token: str

@dataclass
class DB:
    host: str
    db_name: str
    user: str
    password: str

@dataclass
class Config:
    bot: Bot
    db: DB

def load_config():
    return Config(
        bot = Bot(token=os.environ.get("TOKEN")),
        db = DB(
            host=os.environ.get("DB_HOST"),
            db_name=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS")
        )
    )

print(load_config().db.host)