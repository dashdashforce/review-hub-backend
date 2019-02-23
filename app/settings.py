from dotenv import find_dotenv, load_dotenv
import os
load_dotenv(find_dotenv())


DEBUG = os.getenv('DEBUG', default=False) == 'True'
PORT = int(os.getenv('PORT'))
SECRET = os.getenv('SECRET')

AUTH_EXPIRE = 5000

GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GUTHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
