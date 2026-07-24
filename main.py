import json
import os
from flask import Flask, abort, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

COMMAND_FILE = "commands.json"
SHOWCASE_FILE = "showcase.json"


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


@app.route("/stats")
def stats():
    try:
        with open(SHOWCASE_FILE, encoding="utf-8") as file:
            data = json.load(file)

        return jsonify({
            "servers": data.get("totalServers", 0),
            "users": data.get("totalMembers", 0),
            "commands": data.get("totalCommands", 0),
            "uptime": data.get("uptime", "99.9%"),
        })

    except Exception as e:
        return (
            jsonify({
                "servers": 0,
                "users": 0,
                "commands": 0,
                "uptime": "unknown",
                "error": str(e),
            }),
            500,
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
