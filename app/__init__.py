import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'negri'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(basedir), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=30)  # 👈 срок автологина

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'routes_bp.login'
socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    TEMPLATE_DIR = os.path.join(os.path.dirname(basedir), "templates")
    STATIC_DIR = os.path.join(os.path.dirname(basedir), "static")

    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    # 👇 Регистрируем user_loader после инициализации
    @login_manager.user_loader
    def load_user(user_id):
        #print(f"🔑 Автовход: загружаем пользователя с id={user_id}")
        from app.models import User  # импорт здесь, чтобы избежать циклической зависимости
        return User.query.get(int(user_id))

    with app.app_context():
        from app import models  # 👈 импорт только здесь!
        db.create_all()

    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app, socketio
