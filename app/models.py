from datetime import datetime
from app.create import db
from flask_login import UserMixin
from app.create import login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default='user')  # 'user' или 'admin'
    is_superadmin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    issues = db.Column(db.String(500))  # строка с перечислением чекбоксов
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Ожидает')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
