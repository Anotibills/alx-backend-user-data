#!/usr/bin/env python3
"""
App code with error handling
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv('AUTH_TYPE')

if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    '''
    This returns not found
    '''
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    '''
    This returns unauthorized error
    '''
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    '''
    This returns forbidden error
    '''
    return jsonify({"error": "Forbidden"}), 403

@app.before_request
def before_request() -> None:
    '''
    This handles before request
    '''
    paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if auth and auth.require_auth(request.path, paths):
        if not auth.authorization_header(request):
            abort(401)
        if not auth.current_user(request):
            abort(403)

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", "5000"))
    app.run(host=host, port=port)
