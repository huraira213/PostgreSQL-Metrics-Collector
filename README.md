## PostgreSQL Metrics Collector
A lightweight Python-based monitoring tool that collects and stores key PostgreSQL internal metrics (from pg_stat_activity, pg_stat_bgwriter, and pg_database_size()) into a structured database table for analysis and performance tracking.

### Project Structure
```
postgresql-metrics-collector/
│
├── collector/
│   ├── __init__.py
│   ├── collector.py           # Core logic: connects to DB, runs queries, inserts metrics
│   ├── db_manager.py          # Handles connections and schema setup (metrics_raw table)
│   ├── queries.py             # SQL queries for pg_stat_activity, pg_stat_bgwriter, etc.
│   ├── scheduler.py           # Handles timed collection (every minute)
│   └── utils.py               # Helper functions (timestamp, logging, config loading)
│
├── utils/
│   └── logger.py 
│
│
├── config/
│   └── db_config.json         # PostgreSQL connection settings (host, user, dbname, etc.)
│   └──config.ini
│
├── data/
│   └── metrics_raw.db         # (Optional) SQLite for local storage if PostgreSQL not used
│
├── db/
│   └── connection.py  
│ 
├── logs/
│   └── collector.log          # Logs connection, errors, and metric insertions
│
├── tests/
│   ├── test_connection.py
│   ├── debug_connection.py
│   └──config.ini
│ 
├── ui/
│   └── cli.py  
│
├── scripts/
│   └── init_db.sql            # SQL script to create metrics_raw table (for setup)
│
├── README.md                  # Project overview, setup steps, and example output
├── requirements.txt           # Dependencies (psycopg, schedule, etc.)
└── main.py                    # Entry point – starts the collector and scheduler

```
