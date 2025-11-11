# ui/cli.py
import click
from db.connection import get_connection
from collector.collector import collect_db_metrics, insert_system_metrics
from analyzer.writer import write_insights
from analyzer.db_analyzer import get_latest_db_metrics
from analyzer.sys_analyzer import get_latest_sys_metrics
from tabulate import tabulate  # Optional: nice table formatting


@click.group()
def cli():
    """PostgreSQL Metrics Collector CLI"""
    pass


@cli.command()
def collect():
    """Collect metrics and generate insights immediately."""
    conn = get_connection()
    if not conn:
        click.echo(" Failed to connect to database.")
        return

    db_ok = collect_db_metrics(conn)
    sys_ok = insert_system_metrics(conn)
    write_insights(conn)

    if db_ok and sys_ok:
        click.echo(" Metrics collected and insights generated.")
    else:
        click.echo("Metrics collected but with warnings/errors. Check logs.")


@cli.command()
def analyze():
    """Analyze insights and generate reports."""
    conn = get_connection()
    if not conn:
        click.echo(" Failed to connect to database.")
        return

    write_insights(conn)
    click.echo(" Insights analyzed and reports generated.")


@cli.command()
@click.option("--limit", default=5, help="Number of recent metrics to display")
@click.option("--type", type=click.Choice(["db", "system"], case_sensitive=False), required=True, help="Select which metrics to show")
def show_metrics(type, limit):
    """Show the latest collected metrics."""
    conn = get_connection()
    if not conn:
        click.echo("Failed to connect to database.")
        return

    if type.lower() == "db":
        db_query = """
            SELECT collected_at, active_connections, idle_in_xact_connections, database_size_bytes, bgwriter_stats
            FROM metrics_raw
            ORDER BY collected_at DESC
            LIMIT %s
        """
        with conn.cursor() as cur:
            cur.execute(db_query, (limit,))  # Pass limit as a tuple
            rows = cur.fetchall()

        click.echo("=== Latest DB Metrics ===")
        click.echo(rows if rows else "No DB metrics found.")

    elif type.lower() == "system":
        sys_query = """
            SELECT collected_at, cpu_percent, memory_percent, disk_usage_percent, disk_io_read_delta, disk_io_write_delta
            FROM system_metrics
            ORDER BY collected_at DESC
            LIMIT %s
        """
        with conn.cursor() as cur:
            cur.execute(sys_query, (limit,))
            rows = cur.fetchall()

        click.echo("=== Latest System Metrics ===")
        click.echo(rows if rows else "No System metrics found.")


@cli.command()
@click.option("--limit", default=5, help="Number of recent insights to display")
@click.option("--severity", default=None, help="Filter by severity level (INFO, WARNING, CRITICAL)")
def show_insights(limit, severity):
    """Show the latest insights generated."""
    conn = get_connection()
    if not conn:
        click.echo("Failed to connect to database.")
        return

    try:
        with conn.cursor() as cur:
            query = "SELECT collected_at, metric_name, value, threshold, severity, message FROM insights"
            params = []
            if severity:
                query += " WHERE severity = %s"
                params.append(severity.upper())
            query += " ORDER BY collected_at DESC LIMIT %s"
            params.append(limit)

            cur.execute(query, params)
            rows = cur.fetchall()

            if not rows:
                click.echo("No insights found!")
                return

            headers = ["Time", "Metric", "Value", "Threshold", "Severity", "Message"]
            click.echo(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
    except Exception as e:
        click.echo(f"Failed to fetch insights: {e}")


if __name__ == "__main__":
    cli()
