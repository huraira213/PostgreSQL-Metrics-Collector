# db/connection.py
import psycopg
from configparser import ConfigParser
from utils.logger import setup_logger
logger = setup_logger()


def load_config():
    """Load database configuration from config.ini"""
    config = ConfigParser()
    config.read('config/config.ini')
    return config['postgresql']

def get_connection():
    try:
        params = load_config()
        conn = psycopg.connect(**params)
        logger.info("Database connection established.")
        return conn
    except Exception as e:
        logger.error(f"DB connection failed: {e}")
        return None






