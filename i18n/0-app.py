#!/usr/bin/env python3
"""
Basic Flask application with Babel configuration.
"""
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """
    Configuration class for the Flask application.
    Sets available languages, default locale, and timezone.
    """
    # Class attribute for available languages
    LANGUAGES = ["en", "fr"]

    # Use Config to set Babel’s default locale
    BABEL_DEFAULT_LOCALE = "en"

    # Use Config to set Babel’s default timezone
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Instantiate the Flask app
app = Flask(__name__)

# Use the Config class for application configuration
app.config.from_object(Config)

# Instantiate the Babel object and store it in a module-level variable
babel = Babel(app)


@app.route('/')
def index() -> str:
    """
    Route handler for the root URL.
    Renders the 1-index.html template.
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
