from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import threading

app = Flask(__name__)

db_lock = threading.Lock()

# Helper function to get database connection
def get_db_connection():
    conn = sqlite3.connect('siem.db')
    conn.row_factory = sqlite3.Row
    return conn

# Updated route to display the dashboard with data
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch recent logs
    logs = cursor.execute('SELECT * FROM logs ORDER BY id DESC LIMIT 10').fetchall()
    
    # Fetch recent alerts
    alerts = cursor.execute('SELECT * FROM alerts ORDER BY id DESC LIMIT 10').fetchall()
    
    conn.close()
    return render_template('dashboard.html', logs=logs, alerts=alerts)

# Route to receive logs
@app.route('/ingest', methods=['POST'])
def ingest_log():
    try:
        log_data = request.json
        ip = log_data.get('ip')
        message = log_data.get('message')
        timestamp = log_data.get('timestamp')

        with db_lock:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO logs (timestamp, ip, message) VALUES (?, ?, ?)',
                (timestamp, ip, message)
            )
            conn.commit()
            conn.close()

        print(f"Log received and saved: {ip} - {message}")
        return jsonify({"status": "success", "message": "Log ingested"}), 200
        
    except Exception as e:
        print(f"Error ingesting log: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    import database
    database.init_db()
    app.run(debug=True, port=5000)