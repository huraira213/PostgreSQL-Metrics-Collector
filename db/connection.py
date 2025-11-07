# db/connection.py
import psycopg
from configparser import ConfigParser

def load_config():
    """Load database configuration from config.ini"""
    config = ConfigParser()
    config.read('config/config.ini')
    return config['postgresql']

def get_connection():
    """ Get a database connection """
    try:
        params = load_config()
        return psycopg.connect(**params)
    except Exception as e:
        print(f"Error as {e}")

def initialize_db():
    """Initialize the metrics_raw table with our hybrid schema"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS metrics_raw(
        id BIGSERIAL PRIMARY KEY,
        collected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        active_connections INTEGER,
        idle_in_xact_connections INTEGER,
        database_size_bytes BIGINT,
        bgwriter_stats JSONB
    );
    
    CREATE INDEX IF NOT EXISTS idx_metrics_collected_at ON metrics_raw (collected_at);
    """

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_sql)
                conn.commit()
            print("Database is initialized successfully")
    except Exception as e:
        print(f" Database initialization failed: {e}")
        raise

