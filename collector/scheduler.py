# collector/scheduler.py
# This file is responsible for scheduling the timed execution of your metrics collection.
import schedule
import time
from collector.collector import collect_db_metrics, insert_system_metrics
from analyzer.writer import write_insights
from utils.logger import setup_logger

logger = setup_logger()

def job(conn):
    logger.info("Running scheduled ")
    db_metrics = collect_db_metrics(conn)
    sys_metrics = insert_system_metrics(conn)
    write_insights(conn)
    if not db_metrics or not sys_metrics:
        logger.warning(f"Run had errors: db_metrics={db_metrics}, sys_metrics={sys_metrics}")


def start_scheduler(conn):
    schedule.every(1).minute.do(job, conn=conn)

    while True:
        schedule.run_pending()
        time.sleep(1)

