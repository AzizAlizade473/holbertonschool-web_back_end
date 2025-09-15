#!/usr/bin/python3
from flask import Flask
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 5000))
    app.run(host=host, port=port)
