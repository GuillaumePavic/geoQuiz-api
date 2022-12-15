import os
from os.path import join, dirname
import json
import psycopg2
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(url)

with open('data.json', encoding="utf-8") as data_json:
    data = json.load(data_json)

    sql = """
          INSERT INTO "country"
          ("country", "full_name", "capital", "continent_id", "level_id")
          VALUES
          (%s, %s, %s, %s, %s);
        """
    with connection:
        with connection.cursor() as cursor:
          for entry in data:
              cursor.execute(sql, (entry["country"],  entry["full_name"], entry["capital"], entry["continent_id"], entry["level_id"]))


