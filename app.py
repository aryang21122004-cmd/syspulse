import os
import sqlite3
import threading
import time
from functools import wraps
from flask import Flask, render_template, jsonify, request
import psutil
from dotenv import load_dotenv

# Load secret environment keys
load_dotenv()

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "dev-key-change-me")


# ── Restored Step 8 Database Background Worker ─────────────────────
def init_db():
    conn = sqlite3.connect('metrics.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS system_logs
                 (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                  cpu REAL, ram REAL, temp REAL)''')
    conn.commit()
    conn.close()

def log_metrics_periodically():
    while True:
        # Pull system data matching production resolution
        cpu_usage = psutil.cpu_percent(interval=0.5)
        ram_usage = psutil.virtual_memory().percent

        temp = 0
        sensors_temp = psutil.sensors_temperatures()
        if sensors_temp:
            if "coretemp" in sensors_temp:
                temp = sensors_temp["coretemp"][0].current
            elif list(sensors_temp.values()):
                temp = list(sensors_temp.values())[0][0].current

        # Insert record into database
        conn = sqlite3.connect('metrics.db')
        c = conn.cursor()
        c.execute("INSERT INTO system_logs (cpu, ram, temp) VALUES (?, ?, ?)", (cpu_usage, ram_usage, temp))
        conn.commit()
        conn.close()
        
        time.sleep(30) # Capture logging state every 30 seconds

# Automatically spin up database connection & tracking thread on load
init_db()
threading.Thread(target=log_metrics_periodically, daemon=True).start()


# ── Auth decorator ─────────────────────────────────────────────────
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get("X-API-Key") != API_KEY:
            return jsonify({"error": "Invalid or missing API key."}), 401
        return f(*args, **kwargs)
    return decorated


# ── Routes ─────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html", api_key=API_KEY)


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200


@app.route("/api/metrics")
@require_api_key
def get_metrics():
    cpu_usage = psutil.cpu_percent(interval=0.5)
    ram_usage = psutil.virtual_memory().percent

    temp = 0
    sensors_temp = psutil.sensors_temperatures()
    if sensors_temp:
        if "coretemp" in sensors_temp:
            temp = sensors_temp["coretemp"][0].current
        elif list(sensors_temp.values()):
            temp = list(sensors_temp.values())[0][0].current

    fan_speed = 0
    sensors_fans = psutil.sensors_fans()
    if sensors_fans and list(sensors_fans.values()):
        fan_speed = list(sensors_fans.values())[0][0].current

    return jsonify({
        "cpu":  cpu_usage,
        "ram":  ram_usage,
        "temp": temp,
        "fan":  fan_speed,
    }), 200


# ── Restored Step 8 Secure History Route ───────────────────────────
@app.route("/api/history")
@require_api_key  # Leverages the production security gate automatically
def get_history():
    conn = sqlite3.connect('metrics.db')
    c = conn.cursor()
    c.execute("SELECT timestamp, cpu, ram FROM system_logs ORDER BY timestamp DESC LIMIT 10")
    logs = c.fetchall()
    conn.close()
    return jsonify(logs), 200


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)