import os
import urllib.parse as up
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv('DB_URI')

up.uses_netloc.append("postgres")
url = up.urlparse(DB_URI)
conn = psycopg2.connect(database=url.path[1:],
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
