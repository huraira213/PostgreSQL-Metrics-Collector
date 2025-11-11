# analyzer/sys_analyzer.py
from utils.logger import setup_logger

logger = setup_logger()

# Thresholds for alerts
THRESHOLDS = {
    "cpu_percent": 85,
    "memory_percent": 85,
    "disk_usage_percent": 90
}

SEVERITY = {
    "low": "INFO",
    "medium": "WARNING",
    "high": "CRITICAL"
}


def get_latest_sys_metrics(conn):
    """Thus function will fetch the latest metrics from sys_metrics table"""
    try:
        with conn.cursor() as cur:
            sql = "SELECT collected_at, cpu_percent, memory_percent, disk_usage_percent, disk_io_read_delta, disk_io_write_delta  FROM system_metrics ORDER BY collected_at DESC LIMIT 1"
            cur.execute(sql)
            row = cur.fetchone()

            if row is None:
                logger.warning("No sys metrics found in matrics_raw.")
                return []

            return row
    except Exception as e:
        logger.error(f"Failed to fetch latest SYS metrics: {e}")
        return None


def evaluate_sys_rules(conn):
    """Analyze the latest metrics and insert insights."""
    insights_to_insert = []
    matrics = get_latest_sys_metrics(conn)
    collected_at, cpu, mem, disk, io_read, io_write = matrics

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
    logger.debug(f"Checking metric active_connections={cpu} against threshold={THRESHOLDS['cpu_percent']}")

    return insights_to_insert
