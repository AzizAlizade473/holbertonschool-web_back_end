#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views



@app_views.route("/status", methods=["GET"])
def status():
    return "OK", 200



@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """ GET /api/v1/unauthorized
    Return:
      - raises a 401 error
    """
    abort(401)
