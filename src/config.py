from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY') or 'kdlaksngiojwjb4jqufasujdb2'

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

EMAIL_CHECK_API_KEY = os.environ.get('EMAIL_CHECK_API_KEY') or '65f2c72006c102906655b3759f480eac4dfe32f5'