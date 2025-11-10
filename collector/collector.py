#collector/collector.py
from collector.queries import (ACTIVE_CONNECTION, IDLE_IN_TRANSACTION_CONNECTIONS, DATABASE_SIZE, BGWITER_STATS)
from utils.logger import setup_logger
from collector.utils import collect_system_metrics
import json


logger = setup_logger()
def collect_db_metrics(conn):
    """ Collects metrics from PostgreSQL database and store them in a table"""
    try:
        with conn.cursor() as cur:
            #  FIX: parameters must be tuples ("dbname",)
            cur.execute(ACTIVE_CONNECTION, ("metrics_collector",))
            active_connections = cur.fetchone()[0]

            cur.execute(IDLE_IN_TRANSACTION_CONNECTIONS)
            idle_in_xact = cur.fetchone()[0]

            cur.execute(DATABASE_SIZE, ("metrics_collector",))
            database_size = cur.fetchone()[0]

            cur.execute(BGWITER_STATS)
            bgwriter_stats = cur.fetchall()

            #  FIX: convert list → JSON string
            bgwriter_json = json.dumps([
                {
                    "checkpoints_timed": row[0],
                    "checkpoints_req": row[1],
                    "buffers_checkpoint": row[2],
                    "buffers_clean": row[3],
                    "buffers_backend": row[4],
                    "buffers_backend_fsync": row[5],
                    "buffers_alloc": row[6],
                    "checkpoint_write_time": row[7],
                    "checkpoint_sync_time": row[8]
                } for row in bgwriter_stats
            ])

            insert_sql = """
                         INSERT INTO metrics_raw (active_connections,
                                                  idle_in_xact_connections,
                                                  database_size_bytes,
                                                  bgwriter_stats)
                         VALUES (%s, %s, %s, %s); 
                         """

            cur.execute(
                insert_sql,
                (active_connections, idle_in_xact, database_size, bgwriter_json)
            )
            conn.commit()
            logger.info(f"DB Metrics inserted successfully.")
            return True

    except Exception as e:
        logger.error(f"Error collecting metrics: {e}")
        return False

def insert_system_metrics(conn):
    """ Collects system metrics from System and store them in a table"""
    try:
        with conn.cursor() as cur:
            system_metrics = collect_system_metrics()
            if not system_metrics:
                logger.warning('No system metrics collected.')
                return False

            insert_sys_sql = """
                         INSERT INTO system_metrics (
                             cpu_percent, 
                             memory_percent, 
                             disk_usage_percent, 
                             disk_io_read_delta, 
                             disk_io_write_delta)
                         VALUES (%s, %s, %s, %s, %s); 
                         """
            cur.execute(
                insert_sys_sql,
                (
                    system_metrics["cpu_percent"],
                    system_metrics["memory_percent"],
                    system_metrics["disk_usage_percent"],
                    system_metrics["disk_io_read_delta"],
                    system_metrics["disk_io_write_delta"],
                )
            )
            conn.commit()
            logger.info(f"System metrics inserted successfully.")
            return True
    except Exception as e:
        logger.error(f"Error collecting system metrics: {e}")
        return False
