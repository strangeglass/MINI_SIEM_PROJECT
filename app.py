from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import threading # NEW: Import threading for locks

app = Flask(__name__)

# NEW: Create a lock object to handle database concurrency
db_lock = threading.Lock()

# Helper function to get database connection
def get_db_connection():
    conn = sqlite3.connect('siem.db')
    conn.row_factory = sqlite3.Row
    return conn

# Basic route for dashboard
@app.route('/')
def index():
    return "Mini SIEM Dashboard is Running"

# Route to receive logs
@app.route('/ingest', methods=['POST'])
def ingest_log():
    try:
        # Receive JSON data from the request
        log_data = request.json
        
        # Extract data
        ip = log_data.get('ip')
        message = log_data.get('message')
        timestamp = log_data.get('timestamp')

        # Use the lock to make database operations safe
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
    # We need to make sure the database exists before starting
    import database
    database.init_db()
    app.run(debug=True, port=5000)