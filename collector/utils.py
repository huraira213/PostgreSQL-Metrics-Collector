
# collector/utils.py
import psutil
from utils.logger import setup_logger

logger = setup_logger()
_prev_io_counters = None

def collect_system_metrics():
    """
    CPU usage: cpu_percent(interval=1) — measures CPU load over 1 second.
Memory usage: .virtual_memory().percent — % of RAM in use.
Disk usage: .disk_usage('/').percent — % used on root partition.
Disk I/O: .disk_io_counters() — total bytes read/written since boot. function gives disk usage statistics as a tuple for a given path. Total, used and free space are expressed in bytes, along with the percentage usage.
"""
    global _prev_io_counters
    try:
        cpu = psutil.cpu_percent(interval=0)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        io = psutil.disk_io_counters()

        if _prev_io_counters:
            read_delta = io.read_bytes - _prev_io_counters.read_bytes
            write_delta = io.write_bytes - _prev_io_counters.write_bytes
        else:
            read_delta = 0
            write_delta = 0

        _prev_io_counters = io

        metrics = {
            "cpu_percent": cpu,
            "memory_percent": mem,
            "disk_usage_percent": disk,
            "disk_io_read_delta": read_delta,
            "disk_io_write_delta": write_delta
        }

        if cpu > 90 or mem > 90 or disk > 90:
            logger.warning(f"High system resource usage: {metrics}")


        return metrics

    except Exception as e:
        logger.error(f"Failed to collect system metrics: {e}")
        return None
