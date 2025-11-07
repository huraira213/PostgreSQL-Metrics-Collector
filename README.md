## PostgreSQL Metrics Collector
A lightweight Python-based monitoring tool that collects and stores key PostgreSQL internal metrics (from pg_stat_activity, pg_stat_bgwriter, and pg_database_size()) into a structured database table for analysis and performance tracking.

This project is designed to help developers and database engineers understand how PostgreSQL exposes internal system statistics, how to query them programmatically using psycopg, and how to build a foundation for real-time database monitoring systems.

**Core Features:**

Connects to PostgreSQL using psycopg with context managers.

Extracts live system metrics (connections, checkpoints, I/O stats, DB size).

Stores snapshots with timestamps in a local table (metrics_raw).

Demonstrates clean, modular Python design for database introspection.

**Learning Focus:**

PostgreSQL system catalogs and introspection views

Python–PostgreSQL integration (via psycopg)

Designing a metrics schema and periodic collectors

Goal:
Build foundational understanding of PostgreSQL internals, preparing for advanced topics like query optimization, performance diagnostics, and data infrastructure monitoring.

---
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
├── scripts/
│   └── init_db.sql            # SQL script to create metrics_raw table (for setup)
│
├── README.md                  # Project overview, setup steps, and example output
├── requirements.txt           # Dependencies (psycopg, schedule, etc.)
└── main.py                    # Entry point – starts the collector and scheduler

```
| Folder/File               | Purpose                                                                  |
| ------------------------- | ------------------------------------------------------------------------ |
| `collector/collector.py`  | Core engine: fetches metrics and stores them in DB                       |
| `collector/db_manager.py` | Creates table, manages inserts, handles DB context                       |
| `collector/queries.py`    | Keeps SQL logic separate and reusable                                    |
| `collector/scheduler.py`  | Runs the collector every X minutes using `schedule` or `threading.Timer` |
| `config/db_config.json`   | Stores DB credentials securely (avoid hardcoding)                        |
| `logs/collector.log`      | Records run status, errors, and timestamps                               |
| `scripts/init_db.sql`     | Simple schema creation script for the metrics table                      |
| `tests/test_collector.py` | Verifies that queries return valid results                               |
| `main.py`                 | Starts the program (imports collector and runs it periodically)          |

---