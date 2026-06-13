import os
import psycopg2

from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

def get_connection():
    """
    :return
            Connection to PostgreSQL database.
    """
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
