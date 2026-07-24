import json
import os
from flask import Flask, abort, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

COMMAND_FILE = "commands.json"
SHOWCASE_FILE = "showcase.json"
STATS_FILE = "stats.json"


def verify_key():
    key = request.headers.get("Authorization")
    if key != os.getenv("API_KEY"):
        abort(401)


@app.route("/")
def home():
    return {"status": "online", "service": "Pleed API"}


@app.route("/commands")
def commands():
    with open(COMMAND_FILE, encoding="utf-8") as file:
        return jsonify(json.load(file))


@app.route("/commands/<name>")
def command_details(name):
    with open(COMMAND_FILE, encoding="utf-8") as file:
        commands = json.load(file)

    for command in commands:
        if command["name"].lower() == name.lower():
            return jsonify(command)

    return {"error": "Command not found"}, 404


@app.route("/update-commands", methods=["POST"])
def update_commands():
    verify_key()

    data = request.get_json()

    if not data:
        return {"error": "No data provided"}, 400

    with open(COMMAND_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return {"success": True, "commands": len(data)}


@app.route("/update-stats", methods=["POST"])
def update_stats():
    # If using API key protection, uncomment the next line:
    # verify_key()

    data = request.get_json()

    if not data:
        return {"error": "No stats provided"}, 400

    with open(STATS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return {"success": True}


@app.route("/stats")
def stats():
    if not os.path.exists(STATS_FILE):
        return {
            "servers": 0,
            "users": 0,
            "commands": 0,
            "uptime": "unknown",
        }

    with open(STATS_FILE, encoding="utf-8") as file:
        return jsonify(json.load(file))


@app.route("/update-servers", methods=["POST"])
def update_servers():
    data = request.get_json()

    if not data:
        return {"error": "No data provided"}, 400

    with open(SERVER_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    servers_list = data.get("servers", []) if isinstance(data, dict) else []

    return {
        "success": True,
        "servers": len(servers_list)
    }


@app.route("/servers")
def servers():
    if not os.path.exists(SERVER_FILE):
        return jsonify({"servers": []})

    try:
        with open(SERVER_FILE, encoding="utf-8") as file:
            return jsonify(json.load(file))
    except Exception as e:
        return jsonify({"error": str(e), "servers": []}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
