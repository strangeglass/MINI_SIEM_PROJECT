from flask import Flask, render_template, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Helper function to get database connection
def get_db_connection():
    conn = sqlite3.connect('siem.db')
    conn.row_factory = sqlite3.Row
    return conn

# Basic route for dashboard (we will build this later)
@app.route('/')
def index():
    return "Mini SIEM Dashboard is Running"

# NEW: Route to receive logs
@app.route('/ingest', methods=['POST'])
def ingest_log():
    try:
        # Receive JSON data from the request
        log_data = request.json
        
        # Extract data (assuming a specific format)
        ip = log_data.get('ip')
        message = log_data.get('message')
        timestamp = log_data.get('timestamp')

        # Connect to database and insert the log
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
    app.run(debug=True, port=5000)