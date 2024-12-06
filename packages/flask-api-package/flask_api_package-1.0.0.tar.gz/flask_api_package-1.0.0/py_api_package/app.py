from flask import Flask
from flask_api_package.routes import register_routes

def create_app():
    app = Flask(__name__)

    # Register routes from the routes module
    register_routes(app)

    return app