import os

from flask import redirect, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

OPENAPI_DIR = os.path.join(os.path.dirname(__file__), "openapi")
SWAGGER_URL = "/docs"
OPENAPI_URL = "/openapi.yaml"


def register_swagger(app):
    swagger_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        OPENAPI_URL,
        config={"app_name": "API de Pedidos", "displayRequestDuration": True},
    )
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    @app.get(OPENAPI_URL)
    def openapi_spec():
        return send_from_directory(OPENAPI_DIR, "openapi.yaml", mimetype="application/yaml")

    @app.get("/")
    def raiz():
        return redirect(SWAGGER_URL)