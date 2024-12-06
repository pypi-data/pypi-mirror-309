from flasgger import Swagger
from flask import Flask

from t1cicd.cicd.db.db import init_flask_db
from t1cicd.cicd.db.service.summary import SummaryService
from t1cicd.cicd.server.api import register_routes
from t1cicd.cicd.server.config import DevelopmentConfig, ProductionConfig, TestingConfig


def create_app(config_name=None):
    app = Flask(__name__)

    # Choose the configuration based on the provided config name
    if config_name == "development":
        app.config.from_object(DevelopmentConfig)
    elif config_name == "testing":
        app.config.from_object(TestingConfig)
    elif config_name == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)  # Default to development config

    # Initialize swagger
    Swagger(app)
    summary_service = None
    # Initialize the database (but skip in tests)
    if config_name != "testing":
        print("hello")
        init_flask_db(app)
        summary_service = SummaryService()

    # Register routes from api.py
    register_routes(app, summary_service)

    return app
