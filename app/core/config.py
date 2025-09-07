import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT")
    MYSQL_DB: str = os.getenv("MYSQL_DB")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

settings = Settings()