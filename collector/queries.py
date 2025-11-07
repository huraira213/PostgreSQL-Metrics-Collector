# collector/queries.py

ACTIVE_CONNECTION = """
SELECT state, count(*) 
FROM pg_stat_activity
WHERE datname = %s
GROUP BY state;
"""

IDLE_IN_TRANSACTION_CONNECTIONS = """
SELECT count(*) 
FROM pg_stat_activity 
WHERE state = 'idle in transaction';
"""

DATABASE_SIZE = """ 
                SELECT datname, pg_database_size(datname) 
                    FROM pg_database; 
                """

# Complex metrics (will become JSON)
BGWITER_STATS = """
SELECT 
    checkpoints_timed,
    checkpoints_req, 
    buffers_checkpoint,
    buffers_clean,
    buffers_backend,
    buffers_backend_fsync,
    buffers_alloc,
    checkpoint_write_time,
    checkpoint_sync_time
FROM pg_stat_bgwriter;
"""