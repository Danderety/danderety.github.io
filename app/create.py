import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'routes.login'  # маршрут из blueprint

def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIR = os.path.join(os.path.dirname(BASE_DIR), "templates")
    STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), "static")

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
