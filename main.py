import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

COMMAND_FILE = "commands.json"


@app.route("/")
def home():
    return {
        "status": "online",
        "service": "Pleed API"
    }


@app.route("/commands")
def commands():
    with open(COMMAND_FILE, encoding="utf-8") as file:
        return jsonify(json.load(file))


@app.route("/update-commands", methods=["POST"])
def update_commands():
    data = request.get_json()

    if not data:
        return {"error": "No data provided"}, 400

    with open(COMMAND_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    return {
        "success": True,
        "commands": len(data)
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
