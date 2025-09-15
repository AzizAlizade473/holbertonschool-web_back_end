from api.v1.views import app_views

@app_views.route("/status", methods=["GET"])
def status():
    # Must return plain text "OK" for the checker
    return "OK"
