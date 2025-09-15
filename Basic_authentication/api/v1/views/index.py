#!/usr/bin/env python3
"""
This module defines the API routes for the index and status endpoints.
It provides endpoints to check the status of the API and to test the
error handling for unauthorized requests.
"""

from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status

    Returns the status of the API.

    This endpoint is used to check if the API is running and
    responsive. It returns a JSON object with a single key
    "status" and a value of "OK".

    Returns:
        A JSON response with the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """
    GET /api/v1/unauthorized

    Raises a 401 Unauthorized error.

    This endpoint is for testing the custom error handler for
    the 401 status code. When accessed, it uses Flask's `abort`
    function to raise an HTTP 401 error, which will trigger the
    corresponding error handler defined in `app.py`.

    Raises:
        HTTPException: A 401 Unauthorized error.
    """
    abort(401)
