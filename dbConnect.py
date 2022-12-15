import os
from os.path import join, dirname
from dotenv import load_dotenv
import psycopg2

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(url)