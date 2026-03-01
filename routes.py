# routes.py
from flask import Blueprint, request, render_template
from database import get_db
from detection import detect

routes = Blueprint("routes", __name__)

@routes.route("/")
def dashboard():
    conn = get_db()

    logs = conn.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50").fetchall()
    alerts = conn.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 20").fetchall()

    total_logs = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
    total_alerts = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]

    event_stats = conn.execute("SELECT status, COUNT(*) as count FROM logs GROUP BY status").fetchall()
    conn.close()

    labels = [row["status"] for row in event_stats]
    values = [row["count"] for row in event_stats]

    return render_template(
        "dashboard.html",
        logs=logs,
        alerts=alerts,
        total_logs=total_logs,
        total_alerts=total_alerts,
        labels=labels,
        values=values
    )

@routes.route("/ingest", methods=["POST"])
def ingest():
    log_line = request.form.get("log")

    if not log_line:
        return "No log provided", 400

    parts = log_line.strip().split()
    if len(parts) < 3:
        return "Invalid log format. Must be: timestamp ip status", 400

    timestamp, ip, status = parts[:3]

    conn = get_db()
    conn.execute(
        "INSERT INTO logs (timestamp, ip, status) VALUES (?, ?, ?)",
        (timestamp, ip, status.upper())
    )
    conn.commit()
    conn.close()

    detect(ip, status.upper())

    return "OK"  