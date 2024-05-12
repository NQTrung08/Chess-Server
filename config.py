import os

from dotenv import load_dotenv

load_dotenv()


db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("USER_HOST"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DB_NAME"),
}
