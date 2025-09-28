#!/usr/bin/env python3
"""
Flask app with user's locale.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration class for the Flask app."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


def get_user():
    """Returns a user dictionary or None if ID not found."""
    login_id = request.args.get('login_as')
    if login_id:
        try:
            return users.get(int(login_id))
        except (ValueError, TypeError):
            return None
    return None


@app.before_request
def before_request():
    """Sets the user as a global on flask.g."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Determines locale based on priority:
    1. URL parameter
    2. User settings
    3. Request header
    4. Default locale
    """
    # 1. Locale from URL parameters
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # 2. Locale from user settings
    if g.user:
        user_locale = g.user.get('locale')
        if user_locale and user_locale in app.config['LANGUAGES']:
            return user_locale

    # 3. Locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])

    # 4. Default locale is handled by Babel if the above return None


@app.route('/')
def index():
    """Renders the index page."""
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
