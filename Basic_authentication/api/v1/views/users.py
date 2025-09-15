from api.v1.views import app_views

@app_views.route("/users", methods=["GET"])
def get_users():
    return {"users": []}

