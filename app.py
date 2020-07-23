import os
from flask import Flask, render_template
from flask_restful_swagger_2 import Api
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

from models import db, ma

from resource.add_config import AddConfig
from resource.get_configs import GetConfigs
from resource.get_config import GetConfig


def app_factory():
    """Application factory function, instantiate configure
    and return an application instance"""
    app = Flask(__name__)

    # set swagger ui configuration
    SWAGGER_URL = "/v1/doc"
    API_URL = "/v1/doc.json"

    # Call factory function to create swaggerui blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={  # Swagger UI config overrides
                'app_name': "Complaint MicroAPI",
                'validatorUrl': None
            }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    def page_not_found(e):
        return render_template("error.html", page=API_URL[:-5]), 404
    app.register_error_handler(404, page_not_found)

    # load config for development server
    # if FLASK_ENV is set to development
    # else setup app from environment variables
    if os.environ.get("FLASK_ENV") == "development":
        app.config.from_pyfile("config.py")
    else:
        app.config.from_pyfile("config_pro.py")


    # register extensions
    api = Api(
        app,
        api_version="1.0",
        api_spec_url="/v1/doc",
        title="Settings MicroAPI",
        description="A micro-service for managing settings.",
        consumes=["application/json"],
        produces=["application/json"]
    )

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)

    # register endpoints
    api.add_resource(AddConfig, "/v1/setting/new")
    api.add_resource(GetConfigs, "/v1/setting/<string:user_id>/all")
    api.add_resource(GetConfig, "/v1/setting/<string:user_id>/<string:api_name>")

    return app


myapp = app_factory()
