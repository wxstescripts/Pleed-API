from flask import Flask, jsonify
import json


app = Flask(__name__)


@app.route("/")
def home():

    return {
        "status": "online",
        "service": "Pleed API"
    }



@app.route("/commands")
def commands():

    with open(
        "commands.json",
        encoding="utf-8"
    ) as file:

        return jsonify(
            json.load(file)
        )



app.run(
    host="0.0.0.0",
    port=5000
)