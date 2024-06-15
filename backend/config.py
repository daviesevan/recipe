from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

class ApplicationConfiguration:
    SECRET_KEY = os.getenv("APP_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///recipe.sqlite3"
    JWT_SECRET_KEY = os.getenv('APP_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 900 #15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = 86400 #1 day
    EDAMAM_API_URL = "https://api.edamam.com/search"
    EDAMAM_APP_ID = os.getenv("RECIPE_APP_ID")
    EDAMAM_API_KEY = os.getenv("RECIPE_API")
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
