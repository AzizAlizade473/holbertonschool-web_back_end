#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

# Import Auth class
from api.v1.auth.auth import Auth
# Assuming the above import path is correct based on the provided file structure

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Create Auth instance based on environment variable
auth = None
AUTH_TYPE = getenv("AUTH_TYPE", None)
if AUTH_TYPE == "auth":
    auth = Auth()

@app.before_request
def handle_before_request() -> str:
    """
    Handler for before_request actions
    """
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if auth.require_auth(request.path, excluded_paths):
        if auth.authorization_header(request) is None:
            abort(401)
        if auth.current_user(request) is None:
            abort(403)

@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler"""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler"""
    return jsonify({"error": "Forbidden"}), 403

@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
