# analyzer/db_analyzer.py
from utils.logger import setup_logger

logger = setup_logger()

# Thresholds for alerts
THRESHOLDS = {
    "active_connections": 50,
    "idle_in_xact_connections": 20,
    "database_size_bytes": 10 * 1024**3  # 10GB
}

SEVERITY = {
    "low": "INFO",
    "medium": "WARNING",
    "high": "CRITICAL"
}

def get_latest_db_metrics(conn):
    """This function will fetch the latest metrics from metrics_raw table"""
    try:
        with conn.cursor() as cur:
            sql = "SELECT collected_at, active_connections, idle_in_xact_connections, database_size_bytes, bgwriter_stats FROM metrics_raw ORDER BY collected_at DESC LIMIT 1"
            cur.execute(sql)
            row = cur.fetchone()

            if row is None:
                logger.warning("No db metrics found in matrics_raw.")
                return []

            return row
    except Exception as e:
        logger.error(f"Failed to fetch latest DB metrics: {e}")
        return None

def evaluate_db_rules(conn):
    """This function define rules for db matrics """
    insights_to_insert = []
    metrics = get_latest_db_metrics(conn)
    collected_at, active_conn, idle_conn, db_size, bgwriter_json = metrics

    # Rules for db metrics.
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
    logger.debug(f"Checking metric active_connections={active_conn} against threshold={THRESHOLDS['active_connections']}")

    return  insights_to_insert
