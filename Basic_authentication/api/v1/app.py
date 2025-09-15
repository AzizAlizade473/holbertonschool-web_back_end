from flask import Flask, jsonify, abort

app = Flask(__name__)

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized"}), 401
