# main.py
# This is the entry point of your project.
from db.connection import get_connection
from collector.scheduler import start_scheduler
from collector.db_manager import initialize_db
from utils.logger import setup_logger

logger = setup_logger()
def main():
    logger.info("Application starting…")
    try:
        initialize_db()
        conn = get_connection()
        if not conn:
            logger.error("Unable to establish DB connection.")
            return

        start_scheduler(conn)

    except Exception as e:
        logger.critical(f"Fatal error in main: {e}", exc_info=True)



if __name__ == "__main__":
    main()
