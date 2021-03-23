from uuid import uuid4

from flask import Flask
from flask_bootstrap import Bootstrap

from backend import endpoints


def create_app() -> Flask:
    """Return a flask app instance ready to run."""
    app = Flask(__name__)
    app.secret_key = "99702d51-59b9-4a06-9560-d6b28be964df"
    app.register_blueprint(endpoints.blueprint)
    Bootstrap(app)
    return app


