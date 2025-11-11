#analyzer/writer.py
from analyzer.db_analyzer import evaluate_db_rules
from analyzer.sys_analyzer import evaluate_sys_rules
from utils.logger import setup_logger


logger = setup_logger()
def write_insights(conn):
    db_insights = evaluate_db_rules(conn) or []
    sys_insights = evaluate_sys_rules(conn) or []

    all_insights = db_insights + sys_insights

    if not all_insights:
        logger.info("No insights generated this cycle.")
        return

    try:
        with conn.cursor() as cur:
            insert_sql = """INSERT INTO insights (metric_name, value, threshold, severity, message) VALUES (%s, %s, %s, %s, %s);  """
            cur.executemany(insert_sql, all_insights)
            conn.commit()
            logger.info(f"{len(all_insights)} insights inserted.")
    except Exception as e:
        logger.error(f"Failed to insert insights: {e}")
