
# **PostgreSQL Metrics Collector**

A lightweight, Python-based monitoring tool that collects PostgreSQL internal metrics, system resource usage, and automatically generates insights using rule-based analysis.
Provides a CLI for triggering metric collection, viewing data, and inspecting insights.

---

## **Features**

* Collects PostgreSQL metrics:

  * Active connections
  * Idle-in-transaction connections
  * Database size (`pg_database_size`)
  * Background writer stats (`pg_stat_bgwriter`)
* Collects system metrics using `psutil`:

  * CPU usage
  * Memory usage
  * Disk usage
  * Disk I/O deltas
* Rule-based Analyzer:

  * Generates insights with severity levels (`INFO`, `WARNING`, `CRITICAL`)
  * Stores all insights in a dedicated table
* Command-Line Interface (CLI):

  * Trigger manual metric collection
  * View metrics and insights
  * Filter results by severity or limit

---

## **Project Structure**

```postgresql-metrics-collector/
│
├── collector/
│   ├── collector.py           # Core logic: connects to DB, runs queries, inserts metrics
│   ├── db_manager.py          # Handles connections and schema setup (metrics_raw table)
│   ├── queries.py             # SQL queries for pg_stat_activity, pg_stat_bgwriter, etc.
│   ├── scheduler.py           # Handles timed collection (every minute)
│   └── utils.py               # Helper functions (timestamp, logging, config loading)
│
├── analyzer/
│   ├── db_analyzer.py       # returns list of db insights
│   ├── sys_analyzer.py      # returns list of system insights
│   └──  writer.py            # insert insights into DB

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
├── __init__.py
├── README.md                  # Project overview, setup steps, and example output
├── requirements.txt           # Dependencies (psycopg, schedule, etc.)
└── main.py                    # Entry point – starts the collector and scheduler

```

---

## **Installation**

### 1. Clone the repository

```bash
git clone https://github.com/huraira213/PostgreSQL-Metrics-Collector.git
cd PostgreSQL-Metrics-Collector
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL connection


```
config/config.ini
```

Example:

```

   [postgresql]
host = localhost
dbname = metrics_collector
user = huraira
password = ali33
port = 5432


```

---

#  **CLI Usage**

Run any command from the project root:

```bash
python ui/cli.py [COMMAND] [OPTIONS]
```

---

## **1. Collect metrics**

Collects DB metrics + system metrics → saves them → generates insights.

```bash
python ui/cli.py collect
```

Output example:

```
Metrics collected and insights generated.
```

---

## **2. Analyze insights manually**

Runs the analyzer again on existing metrics.

```bash
python ui/cli.py analyze
```

---

## **3. Show metrics**

### Show latest DB metrics:

```bash
python ui/cli.py show-metrics --type db
```

### Show latest system metrics:

```bash
python ui/cli.py show-metrics --type system
```

### With limit:

```bash
python ui/cli.py show-metrics --type db --limit 10
```

---

## **4. Show insights**

```bash
python ui/cli.py show-insights
```

### Filter by severity:

```bash
python ui/cli.py show-insights --severity CRITICAL
```

### Show more rows:

```bash
python ui/cli.py show-insights --limit 20
```

Example output:

```
╒══════════════════════╤══════════════════════╤═════════╤══════════╤══════════╤══════════════════════════════╕
│ Time                 │ Metric               │ Value   │ Threshold│ Severity │ Message                      │
╞══════════════════════╪══════════════════════╪═════════╪══════════╪══════════╪══════════════════════════════╡
│ 2025-11-11 15:00:00  │ active_connections   │ 55      │ 50       │ CRITICAL │ High number of connections    │
│ 2025-11-11 15:00:00  │ cpu_percent          │ 92      │ 85       │ CRITICAL │ CPU usage high: 92%           │
╘══════════════════════╧══════════════════════╧═════════╧══════════╧══════════╧══════════════════════════════╛
```

---

#  **Quick Start Workflow**

Most common workflow:

```bash
# Step 1: Collect metrics
python ui/cli.py collect

# Step 2: Show metrics
python ui/cli.py show-metrics --type db

# Step 3: Show insights
python ui/cli.py show-insights --limit 10
```

---

#  **Notes**

* The scheduler (`collector/scheduler.py`) can run continuous monitoring every minute.
* The CLI is ideal for **manual** monitoring.
* All logs are stored in:

  ```
  logs/collector.log
  ```

---

#  **Future Enhancements**

* FastAPI dashboard
* Notifications (email/Slack)
* Rules loaded from config instead of code
* Visualization charts

---


