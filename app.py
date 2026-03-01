from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_FILE = 'siem.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            message TEXT
        )
    ''')
    # Create alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            reason TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    """Serves the dashboard page with alerts and log count."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # --- FETCH ALL ALERTS (NO LIMIT) ---
    cursor.execute('SELECT * FROM alerts ORDER BY timestamp DESC')
    alerts = cursor.fetchall()
    
    # --- FETCH TOTAL ALERT COUNT ---
    cursor.execute('SELECT COUNT(*) FROM alerts')
    total_alerts = cursor.fetchone()[0]
    # ---------------------------------------------
    
    # Fetch Log Count
    cursor.execute('SELECT COUNT(*) FROM logs')
    log_count = cursor.fetchone()[0]
    
    conn.close()
    
    # --- PASS total_alerts AND alerts ---
    return render_template('dashboard.html', alerts=alerts, log_count=log_count, total_alerts=total_alerts)

@app.route('/ingest', methods=['POST'])
def ingest_log():
    """Ingests a log entry from the simulator."""
    log = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (timestamp, ip, message) VALUES (?, ?, ?)',
                   (log['timestamp'], log['ip'], log['message']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'log ingested'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)