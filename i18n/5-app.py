#!/usr/bin/env python3
"""
Flask application with Babel configuration and mock user login functionality.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel


# Mock database user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


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


def get_user():
    """
    Returns a user dictionary based on the 'login_as' URL parameter,
    or None if the ID is not found or not passed.
    """
    # Get the value of the 'login_as' URL parameter
    login_id = request.args.get('login_as')
    if login_id:
        try:
            # Cast the ID to integer and look it up in the users dictionary
            user_id = int(login_id)
            return users.get(user_id)
        except ValueError:
            # Handle case where login_as is not a valid integer
            pass
    return None


@app.before_request
def before_request():
    """
    Executed before all other functions.
    Finds the user, if any, and sets it on flask.g.user.
    """
    g.user = get_user()


def get_locale():
    """
    Determines the best match for supported languages.
    1. Check for 'locale' argument in URL.
    2. Fallback to locale from request header (Accept-Language).
    """
    # 1. Check for 'locale' argument in URL
    url_locale = request.args.get('locale')
    if url_locale in app.config['LANGUAGES']:
        return url_locale

    # 2. Fallback to locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# Initialize Babel with the app and set the custom locale selector
babel.init_app(app, locale_selector=get_locale)


@app.route('/')
def index() -> str:
    """
    Route handler for the root URL.
    Renders the 5-index.html template.
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
