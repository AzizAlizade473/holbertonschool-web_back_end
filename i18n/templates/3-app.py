#!/usr/bin/env python3
"""
Basic Flask application with Babel configuration and parametrized templates.
"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """
    Configuration class for the Flask application.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel()


def get_locale():
    """
    Determines the best match for supported languages based on
    the user's request header (Accept-Language).
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# Initialize Babel with the app and set the custom locale selector
babel.init_app(app, locale_selector=get_locale)


@app.route('/')
def index() -> str:
    """
    Route handler for the root URL.
    Renders the 3-index.html template.
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
