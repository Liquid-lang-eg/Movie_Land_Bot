import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALGORITHM = os.getenv("ALGORITHM")
DATABASE_URL = os.getenv("DATABASE_URL")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BACKEND_URL = os.getenv("BACKEND_URL")
REDIS_URL = os.getenv("REDIS_URL")
MAX_ERROR_LENGTH = 500