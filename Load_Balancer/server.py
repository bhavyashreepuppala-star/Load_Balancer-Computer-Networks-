from flask import Flask, jsonify
import argparse
import time

app = Flask(__name__)
request_count = 0
started_at = time.time()
SERVER_NAME = "Backend"
PORT = 5001

@app.get("/health")
def health():
    return jsonify({"status": "healthy", "server": SERVER_NAME, "port": PORT})

@app.get("/stats")
def stats():
    return jsonify({"server": SERVER_NAME, "port": PORT,
                    "requests_handled": request_count,
                    "uptime_seconds": round(time.time() - started_at, 2)})

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def handle_request(path):
    global request_count
    request_count += 1
    return jsonify({"message": "Request successfully processed",
                    "handled_by": SERVER_NAME, "server_port": PORT,
                    "request_number_on_this_server": request_count,
                    "requested_path": "/" + path})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--port", required=True, type=int)
    args = parser.parse_args()
    SERVER_NAME, PORT = args.name, args.port
    print(f"Starting {SERVER_NAME} at http://127.0.0.1:{PORT}")
    app.run(host="127.0.0.1", port=PORT, threaded=True, use_reloader=False)
