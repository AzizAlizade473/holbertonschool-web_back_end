from flask import abort
from api.v1.views import app_views

@app_views.route('/unauthorized', methods=['GET'])
def unauthorized_route():
    abort(401)
