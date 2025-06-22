from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from app import db
from app.models import User, Ticket
from app.forms import LoginForm, RegisterForm, SubmitTicketForm
import os

routes_bp = Blueprint('routes_bp', __name__)


@routes_bp.route('/')
@login_required
def index():
    return render_template('index.html')


@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('routes_bp.index'))
        flash('Неверный логин или пароль')
    return render_template('login.html', form=form)


@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь зарегистрирован')
        return redirect(url_for('routes_bp.login'))
    return render_template('register.html', form=form)


@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes_bp.login'))


@routes_bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_ticket():
    form = SubmitTicketForm()
    if form.validate_on_submit():
        attachment_path = None
        if form.attachment.data:
            filename = secure_filename(form.attachment.data.filename)
            save_path = os.path.join('static', 'attachments', filename)
            form.attachment.data.save(save_path)
            attachment_path = filename
        ticket = Ticket(
            room=form.room.data,
            category=form.category.data,
            problem=form.problem.data,
            attachment=attachment_path,
            timestamp=datetime.utcnow(),
            status='Открыт',
            user_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Проблема отправлена.')
        return redirect(url_for('routes_bp.submit_ticket'))
    return render_template('submit.html', form=form)


@routes_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Доступ только для админов.')
        return redirect(url_for('routes_bp.index'))

    tickets = Ticket.query.order_by(Ticket.timestamp.desc()).all()

    if request.method == 'POST':
        for ticket in tickets:
            if request.form.get(f'done_{ticket.id}'):
                ticket.status = 'Выполнено'
            if request.form.get(f'delete_{ticket.id}'):
                db.session.delete(ticket)
        db.session.commit()
        return redirect(url_for('routes_bp.admin_panel'))

    return render_template('admin_panel.html', tickets=tickets)


@routes_bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if not current_user.is_super:
        flash('Доступ запрещён.')
        return redirect(url_for('routes_bp.index'))

    users = User.query.all()

    if request.method == 'POST':
        for user in users:
            if user.is_super:
                continue  # нельзя снять права с суперпользователя

            if f'delete_{user.id}' in request.form:
                db.session.delete(user)
                continue

            new_pw = request.form.get(f'password_{user.id}')
            if new_pw:
                user.password = generate_password_hash(new_pw)

            if f'admin_{user.id}' in request.form:
                if not user.is_admin:
                    user.is_admin = True
                    user.admin_assigned_at = datetime.utcnow()
            else:
                user.is_admin = False
                user.admin_assigned_at = None

        db.session.commit()
        flash('Изменения сохранены.')
        return redirect(url_for('routes_bp.users'))

    return render_template('users.html', users=users)


@routes_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join('static', 'attachments'), filename)
