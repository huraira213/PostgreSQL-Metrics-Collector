# collector/db_manager,py
from db.connection import get_connection
from utils.logger import setup_logger

logger = setup_logger()

def initialize_db():
    """Initialize the metrics_raw table with our hybrid schema"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # For Database matrics
                cur.execute("""
                            CREATE TABLE IF NOT EXISTS metrics_raw(
                                id BIGSERIAL PRIMARY KEY,
                                collected_at
                                TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                                active_connections INTEGER,
                                idle_in_xact_connections INTEGER,
                                database_size_bytes BIGINT,
                                bgwriter_stats JSONB
                                );
                            """)
                cur.execute("""
                            CREATE INDEX IF NOT EXISTS idx_metrics_collected_at
                                ON metrics_raw (collected_at);
                            """)

                # For system metrics
                cur.execute("""
                            CREATE TABLE IF NOT EXISTS system_metrics(
                                id BIGSERIAL PRIMARY KEY,
                                collected_at TIMESTAMPTZ NOT NULL DEFAULT NOW (),
                                cpu_percent REAL,
                                memory_percent REAL,
                                disk_usage_percent REAL,
                                disk_io_read_delta BIGINT,
                                disk_io_write_delta BIGINT
                                );
                            """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_system_metrics
                    on system_metrics(id);
                            """)

                # For inSight
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS insights(
                    id BIGSERIAL PRIMARY KEY,
                    collected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    metric_name TEXT NOT NULL,
                    value NUMERIC,
                    threshold NUMERIC,
                    severity TEXT,
                    message TEXT
                        )
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_insights_collected_at
                    ON insights (collected_at);""")
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_insights_metric_name
                    ON insights (metric_name);
                            """)

                conn.commit()
                logger.info("DB initialized successfully")

    except Exception as e:
        logger.critical(f"Error initializing database: {e}")
        raise