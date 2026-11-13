COMPUTER NETWORKS PROJECT: LOAD BALANCER FOR DISTRIBUTED SYSTEMS

CONTENTS
- server.py: configurable backend HTTP server
- load_balancer.py: Round Robin load balancer, health checks and dashboard
- requirements.txt: Python dependencies
- Project_Report.docx: report based on the supplied sample report structure
- diagrams/: architecture and request workflow diagrams
- tests/: basic automated project checks

REQUIREMENTS
Windows 10/11, Python 3.9+, VS Code recommended.

INSTALL
1. Extract the ZIP and open the folder in VS Code.
2. Open a terminal and run: py -m pip install -r requirements.txt

START FOUR TERMINALS
Terminal 1: py server.py --name Server-1 --port 5001
Terminal 2: py server.py --name Server-2 --port 5002
Terminal 3: py server.py --name Server-3 --port 5003
Terminal 4: py load_balancer.py

DASHBOARD
Open http://127.0.0.1:8000/dashboard

DEMONSTRATION
- Click Send test request repeatedly; handled_by should rotate across available servers.
- Stop one backend using Ctrl+C. Refresh the dashboard; it should show Offline.
- Send more requests; the load balancer should skip the unhealthy backend.
- Restart the stopped server with its original command.
- Stop all backends and send a request to demonstrate HTTP 503.

BASIC CHECKS
Run: py -m unittest discover -s tests -v

All services run locally on 127.0.0.1. This is an academic prototype, not a
production-grade public-facing load balancer. Capture genuine screenshots and
record actual measurements from your own run before submission.
