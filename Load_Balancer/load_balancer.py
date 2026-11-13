from flask import Flask, jsonify, request, Response
import requests
import threading

app = Flask(__name__)
SERVERS = [
    {"name": "Server-1", "url": "http://127.0.0.1:5001"},
    {"name": "Server-2", "url": "http://127.0.0.1:5002"},
    {"name": "Server-3", "url": "http://127.0.0.1:5003"},
]
next_server = 0
lock = threading.Lock()


def server_is_healthy(server):
    try:
        return requests.get(server["url"] + "/health", timeout=0.8).ok
    except requests.RequestException:
        return False


def choose_server():
    global next_server
    with lock:
        for offset in range(len(SERVERS)):
            index = (next_server + offset) % len(SERVERS)
            candidate = SERVERS[index]
            if server_is_healthy(candidate):
                next_server = (index + 1) % len(SERVERS)
                return candidate
    return None


@app.get("/")
def home():
    return jsonify({"project": "Load Balancer for Distributed Systems",
                    "message": "Load balancer is running. Visit /dashboard."})


@app.get("/api/status")
def status():
    result = []
    for server in SERVERS:
        healthy = server_is_healthy(server)
        details = {}
        if healthy:
            try:
                details = requests.get(server["url"] + "/stats", timeout=0.8).json()
            except requests.RequestException:
                healthy = False
        result.append({"name": server["name"], "url": server["url"],
                       "status": "Online" if healthy else "Offline",
                       "requests_handled": details.get("requests_handled", 0),
                       "uptime_seconds": details.get("uptime_seconds", 0)})
    return jsonify({"algorithm": "Round Robin with Health Checks", "servers": result})


@app.get("/dashboard")
def dashboard():
    return DASHBOARD


@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def distribute(path):
    server = choose_server()
    if server is None:
        return jsonify({"error": "No backend servers are currently available"}), 503
    try:
        upstream = requests.request(
            method=request.method,
            url=server["url"] + "/" + path,
            params=request.args,
            data=request.get_data(),
            headers={k: v for k, v in request.headers
                     if k.lower() not in ("host", "content-length")},
            timeout=5)
        excluded = ("content-encoding", "content-length", "transfer-encoding", "connection")
        headers = [(k, v) for k, v in upstream.headers.items() if k.lower() not in excluded]
        return Response(upstream.content, status=upstream.status_code, headers=headers)
    except requests.RequestException:
        return jsonify({"error": f"{server['name']} became unavailable. Please retry."}), 502


DASHBOARD = '''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Load Balancer Dashboard</title><style>
*{box-sizing:border-box}body{margin:0;font-family:Arial;background:#f2f5fa;color:#17243a}
header{background:#172b4d;color:white;padding:25px 5%}main{max-width:1050px;margin:28px auto;padding:0 18px}
.cards,.servers{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:15px}
.card,.server,#result{background:white;padding:20px;border-radius:12px;box-shadow:0 2px 10px #14243b12}
.big{font-size:27px;font-weight:bold;margin-top:8px}.online{color:#14834f}.offline{color:#c32f3b}
button{padding:12px 18px;background:#2463eb;color:white;border:0;border-radius:8px;cursor:pointer;margin:8px 8px 8px 0}
.muted{color:#647187;font-size:14px}#result{white-space:pre-wrap;min-height:55px}
</style></head><body><header><h1>Distributed Systems Load Balancer</h1>
<div>Round Robin scheduling • Backend health monitoring</div></header><main>
<div class="cards"><div class="card">Algorithm<div class="big">Round Robin</div></div>
<div class="card">Servers online<div class="big" id="online">-</div></div>
<div class="card">Requests handled<div class="big" id="total">-</div></div></div>
<h2>Backend server status</h2><div class="servers" id="servers"></div>
<h2>Test the load balancer</h2><p class="muted">Click repeatedly to see requests rotate across available servers.</p>
<button onclick="sendRequest()">Send test request</button><button onclick="refreshStatus()">Refresh status</button>
<div id="result">Test response appears here.</div></main>
<script>
async function refreshStatus(){try{let d=await(await fetch('/api/status')).json();
let n=d.servers.filter(s=>s.status==='Online').length;
document.getElementById('online').textContent=n+' / '+d.servers.length;
document.getElementById('total').textContent=d.servers.reduce((a,s)=>a+s.requests_handled,0);
document.getElementById('servers').innerHTML=d.servers.map(s=>`<div class="server"><h3>${s.name}</h3>
<b class="${s.status==='Online'?'online':'offline'}">${s.status}</b><p class="muted">${s.url}</p>
<p>Requests handled: <b>${s.requests_handled}</b></p><p>Uptime: ${s.uptime_seconds}s</p></div>`).join('');
}catch(e){document.getElementById('servers').textContent='Unable to read status'}}
async function sendRequest(){let b=document.getElementById('result');b.textContent='Sending...';
try{let r=await fetch('/demo');b.textContent=JSON.stringify(await r.json(),null,2);refreshStatus()}
catch(e){b.textContent='Request failed: '+e}}
refreshStatus();setInterval(refreshStatus,3000);
</script></body></html>'''

if __name__ == "__main__":
    print("Load balancer running at http://127.0.0.1:8000")
    print("Dashboard: http://127.0.0.1:8000/dashboard")
    app.run(host="127.0.0.1", port=8000, threaded=True, use_reloader=False)
