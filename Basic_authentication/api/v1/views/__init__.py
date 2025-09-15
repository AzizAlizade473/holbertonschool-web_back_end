from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import endpoints so they get registered
from api.v1.views import index, users
