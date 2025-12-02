Requirements:

Python 3.10 or newer

pip

Packages (in requirements.txt):

Flask

flask-socketio

python-socketio

eventlet

How to run (local):

Clone the repo:

git clone https://github.com/<your-username>/<your-repo>.git

cd <your-repo>

Create and activate virtualenv (optional but recommended):

python -m venv venv

Linux/macOS: source venv/bin/activate

Windows: venv\Scripts\activate

Install dependencies:

pip install --upgrade pip

pip install -r requirements.txt

Start the dashboard (terminal 1):

python dashboard.py

Open http://127.0.0.1:5000/ in your browser

Start the IDS (terminal 2):

python ids_detector.py

IDS listens on 127.0.0.1:8080

How to test detection:

With dashboard and IDS running, open a third terminal.

Run:

python3 - << 'EOF'

import socket

s = socket.socket()

s.connect(('127.0.0.1', 8080))

s.send(b"SELECT * FROM users<script>../admin'--")

s.close()

print("Attack sent")

EOF

Expected:

IDS terminal prints “ATTACK DETECTED” lines and logs to ids_alerts.log.

Dashboard updates counters, adds a row in “Recent Attacks”, and updates the line chart.

Main files:

dashboard.py – Flask + Socket.IO backend and push_attack_event API.

ids_detector.py – Pure Python loopback IDS with signature detection and logging.

templates/index.html – Dashboard UI.

static/css/dashboard.css – Styles for the dashboard.

static/js/dashboard.js – Socket.IO client, Chart.js logic, and UI updates.

requirements.txt – Python dependencies.
