import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'negri'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(basedir), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('static', 'attachments')

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'routes_bp.login'

def create_app():
    TEMPLATE_DIR = os.path.join(os.path.dirname(basedir), "templates")
    STATIC_DIR = os.path.join(os.path.dirname(basedir), "static")

    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()

    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
