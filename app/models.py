from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_super = db.Column(db.Boolean, default=False)
    admin_assigned_at = db.Column(db.DateTime, nullable=True)
    tickets = db.relationship('Ticket', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    problem = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Открыт')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Ticket {self.room} - {self.category}>'
