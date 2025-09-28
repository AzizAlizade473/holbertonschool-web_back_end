#!/usr/bin/env python3
"""
Flask application with Babel configuration and locale forced by URL parameter.
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
    Determines the best match for supported languages.
    1. Check for 'locale' argument in URL.
    2. Fallback to locale from request header (Accept-Language).
    """
    # 1. Check if locale parameter is present in the URL query string
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
    Renders the 4-index.html template.
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
