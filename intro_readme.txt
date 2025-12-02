Intrusion Detection System (IDS) with Real-Time Flask Dashboard

A simple, educational Intrusion Detection System that monitors loopback TCP traffic on port 8080, detects common web attacks using signatures (SQL injection, XSS, directory traversal), and visualizes detections in a real-time web dashboard built with Flask, Flask-SocketIO, and Chart.js.

The project is designed to help you learn:

Network sockets and basic IDS concepts

Flask + Flask-SocketIO for real-time web apps

Frontend integration with Socket.IO and Chart.js

Features

Signature-based IDS:

Detects patterns like:

SELECT * FROM users (SQL injection)

admin'-- (SQL auth bypass)

<script> (XSS)
../ (directory traversal)

Pure Python loopback sniffer (no sudo required)

Real-time web dashboard:

Live counters for SQL/XSS/Dir Traversal and total packets

Recent attacks table (time, type, source IP)

Line chart of attacks over recent events (Chart.js)

Connection status indicator (connected/disconnected from IDS)

Alert sound and animations on new attacks

Requirements

Python 3.10+ (recommended)

pip (Python package manager)

Python dependencies (also listed in requirements.txt):

Flask

flask-socketio

python-socketio

eventlet

(Chart.js and Socket.IO client are loaded via CDN in index.html)

Project Structure

dashboard.py – Flask + Flask-SocketIO backend for the dashboard and push_attack_event function used by IDS

ids_detector.py – Pure Python loopback IDS (TCP on 127.0.0.1:8080) with signature detection and logging

templates/

index.html – Dashboard UI (cards, chart, table)

static/

css/dashboard.css – Custom styling

js/dashboard.js – Socket.IO client, Chart.js integration, and UI updates

requirements.txt – Python dependencies

ids_alerts.log – Log file created at runtime with detected attacks

How to Run Locally

Clone the repository

Using HTTPS:

git clone https://github.com/musavirdar/Intrusion_Detection_System.git

cd <repo>

Create and activate a virtual environment (optional but recommended)

python -m venv venv

Linux/macOS:

source venv/bin/activate

Windows:

venv\Scripts\activate

Install dependencies

pip install --upgrade pip

pip install -r requirements.txt

Start the dashboard (terminal 1)

cd <your-repo> (if not already)

source venv/bin/activate (if not already active)

python dashboard.py

You should see something like:

🚀 Dashboard running at http://0.0.0.0:5000

Start the IDS (terminal 2)

Open a second terminal:

cd <your-repo>

source venv/bin/activate

python ids_detector.py

You should see:

🎉 IDS setup test - all systems ready!

🔍 Monitoring TCP loopback on port 8080... Ctrl+C to stop

Open the dashboard in your browser

Visit:

http://127.0.0.1:5000/

You should see:

Live counters (all zero initially)

A chart area

“Recent Attacks” table (empty at start)

Status bar showing “Connected to IDS”

How to Test the IDS and Dashboard

Send a test attack from a third terminal

With the IDS and dashboard running, open a third terminal:

cd <your-repo>

source venv/bin/activate

Run this Python snippet to send a malicious request to port 8080:

python3 - << 'EOF'

import socket

s = socket.socket()

s.connect(('127.0.0.1', 8080))

s.send(b"SELECT * FROM users<script>../admin'--")

s.close()

print("Attack sent")

EOF

What you should see

Terminal running ids_detector.py:

📦 TCP Packet #1 | From: ('127.0.0.1', ...)

🚨 ATTACK DETECTED: SQL injection detected

🚨 ATTACK DETECTED: XSS attack detected

🚨 ATTACK DETECTED: Directory traversal detected

🚨 ATTACK DETECTED: SQL injection attempt

📝 Logged to ids_alerts.log

Terminal running dashboard.py:

PUSH_ATTACK_EVENT CALLED: sql SQL injection detected 127.0.0.1

(and similar lines for other attack types)

Browser (http://127.0.0.1:5000/):

SQL Injection / XSS / Dir Traversal counters increment

A new row appears in “Recent Attacks”

Line chart adds a new point

Status bar stays “Connected to IDS”

Log File

Detected attacks are also stored in:

ids_alerts.log

Example log line:

[2025-12-02 18:30:12] SQL injection detected from 127.0.0.1 | Signature: SELECT * FROM users

Deploying from GitHub (summary)

High-level steps (for a VPS):

On the server:

sudo apt update && sudo apt install -y python3 python3-venv python3-p

