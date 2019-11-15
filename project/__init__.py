from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)

    login_manager.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']
    
#    if app.config['SSL_REDIRECT']:
#        from flask_sslify import SSLify
#        sslify = SSLify(app)
#
#        from werkzeug.contrib.fixers import ProxyFix 
#        app.wsgi_app = ProxyFix(app.wsgi_app)

    
    from auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
