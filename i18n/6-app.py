#!/usr/bin/env python3
"""
Flask application with Babel configuration and locale priority:
URL > User Settings > Request Header > Default.
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
    login_id = request.args.get('login_as')
    if login_id:
        try:
            user_id = int(login_id)
            return users.get(user_id)
        except ValueError:
            pass
    return None


@app.before_request
def before_request():
    """
    Executed before all other functions.
    Finds the user, if any, and sets it on flask.g.user.
    """
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Determines the best match for supported languages based on the priority:
    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request header
    4. Default locale
    """
    # 1. Locale from URL parameters
    url_locale = request.args.get('locale')
    if url_locale in app.config['LANGUAGES']:
        return url_locale

    # 2. Locale from user settings
    if g.user and g.user.get('locale') and \
       g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')

    # 3. Locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])

    # 4. Default locale (handled automatically by Babel if 1, 2, 3 fail)


@app.route('/')
def index() -> str:
    """
    Route handler for the root URL.
    Renders the 6-index.html template.
    """
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
