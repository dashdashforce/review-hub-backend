from dotenv import find_dotenv, load_dotenv
import os
load_dotenv(find_dotenv())


DEBUG = os.getenv('DEBUG', default=False) == 'True'
PORT = int(os.getenv('PORT'))
SECRET = os.getenv('SECRET')
