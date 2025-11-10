from db.connection import get_connection
from utils.logger import setup_logger

logger = setup_logger()

# Thresholds for alerts
THRESHOLDS = {
    "cpu_percent": 85,
    "memory_percent": 85,
    "disk_usage_percent": 90,
    "active_connections": 50,
    "idle_in_xact_connections": 20,
    "database_size_bytes": 10 * 1024**3  # 10GB
}

SEVERITY = {
    "low": "INFO",
    "medium": "WARNING",
    "high": "CRITICAL"
}


def evaluate_rules(conn):
    """Analyze the latest metrics and insert insights."""
    try:
        with conn.cursor() as cur:
            # Example: fetch the latest raw metrics
            cur.execute("""
                SELECT *
                FROM metrics_raw
                ORDER BY collected_at DESC
                LIMIT 1;
            """)
            row = cur.fetchone()
            if not row:
                logger.warning("No metrics available to analyze.")
                return False

            collected_at, active_conn, idle_conn, db_size, bgwriter_json = row[1:]

            insights_to_insert = []

            # DB Rules
            if active_conn > THRESHOLDS["active_connections"]:
                insights_to_insert.append((
                    "active_connections",
                    active_conn,
                    THRESHOLDS["active_connections"],
                    SEVERITY["high"],
                    f"High number of active connections: {active_conn}"
                ))

            if idle_conn > THRESHOLDS["idle_in_xact_connections"]:
                insights_to_insert.append((
                    "idle_in_xact_connections",
                    idle_conn,
                    THRESHOLDS["idle_in_xact_connections"],
                    SEVERITY["medium"],
                    f"Too many idle-in-transaction connections: {idle_conn}"
                ))

            if db_size > THRESHOLDS["database_size_bytes"]:
                insights_to_insert.append((
                    "database_size_bytes",
                    db_size,
                    THRESHOLDS["database_size_bytes"],
                    SEVERITY["medium"],
                    f"Database size exceeds threshold: {db_size} bytes"
                ))

            # System Metrics
            cur.execute("""
                SELECT *
                FROM system_metrics
                ORDER BY collected_at DESC
                LIMIT 1;
            """)
            sys_row = cur.fetchone()
            if sys_row:
                cpu, mem, disk, io_read, io_write = sys_row[1:]
                if cpu > THRESHOLDS["cpu_percent"]:
                    insights_to_insert.append((
                        "cpu_percent",
                        cpu,
                        THRESHOLDS["cpu_percent"],
                        SEVERITY["high"],
                        f"CPU usage high: {cpu}%"
                    ))
                if mem > THRESHOLDS["memory_percent"]:
                    insights_to_insert.append((
                        "memory_percent",
                        mem,
                        THRESHOLDS["memory_percent"],
                        SEVERITY["medium"],
                        f"Memory usage high: {mem}%"
                    ))
                if disk > THRESHOLDS["disk_usage_percent"]:
                    insights_to_insert.append((
                        "disk_usage_percent",
                        disk,
                        THRESHOLDS["disk_usage_percent"],
                        SEVERITY["medium"],
                        f"Disk usage high: {disk}%"
                    ))

            # Insert insights
            if insights_to_insert:
                insert_sql = """
                    INSERT INTO insights (metric_name, value, threshold, severity, message)
                    VALUES (%s, %s, %s, %s, %s);
                """
                cur.executemany(insert_sql, insights_to_insert)
                conn.commit()
                logger.info(f"{len(insights_to_insert)} insights inserted.")
            else:
                logger.info("No insights generated this cycle.")

            return True

    except Exception as e:
        logger.error(f"Error evaluating rules: {e}")
        return False
