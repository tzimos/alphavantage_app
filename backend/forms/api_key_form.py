import flask
from wtforms import (
    Form,
    StringField,
    validators,
)


class ApiKeyForm(Form):
    api_key = StringField(
        "Alphavantage Api Key",
        validators=[validators.Length(min=1), ]
    )

    def save(self):
        """Save api key to the flask session."""
        session = flask.session
        session["api_key"] = self.api_key.data
