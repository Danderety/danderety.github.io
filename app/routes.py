from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app import db
from app.models import User, Ticket
from app.forms import LoginForm, RegisterForm, SubmitTicketForm

routes_bp = Blueprint('routes_bp', __name__)


@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('routes_bp.admin_panel'))
            return redirect(url_for('routes_bp.submit_ticket'))
       
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
        ticket = Ticket(
            room=form.room.data,
            category=form.category.data,
            problem=form.problem.data,
            timestamp=datetime.utcnow(),
            status='Открыт',
            user_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Тикет отправлен')
        return redirect(url_for('routes_bp.submit_ticket'))

    my_tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.timestamp.desc()).limit(10).all()
    return render_template('submit.html', form=form, my_tickets=my_tickets)



@routes_bp.route('/admin', methods=['GET'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Доступ запрещен')
        return redirect(url_for('routes_bp.submit_ticket'))

    tickets = Ticket.query.order_by(Ticket.timestamp.desc()).all()
    return render_template('admin_panel.html', tickets=tickets)


@routes_bp.route('/admin/toggle_done/<int:ticket_id>', methods=['POST'])
@login_required
def toggle_done(ticket_id):
    if not current_user.is_admin:
        return '', 403

    data = request.get_json()
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = 'Выполнено' if data.get('done') else 'Открыт'
    db.session.commit()
    return '', 204


@routes_bp.route('/admin/delete_tickets', methods=['POST'])
@login_required
def delete_tickets():
    if not current_user.is_admin:
        return '', 403

    data = request.get_json()
    ids = data.get('ids', [])
    action = data.get('action')

    for ticket_id in ids:
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            continue

        if action == 'now':
            db.session.delete(ticket)
    db.session.commit()
    return '', 204


@routes_bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if not current_user.is_super:
        flash('Доступ запрещён')
        return redirect(url_for('routes_bp.submit_ticket'))

    users = User.query.all()

    if request.method == 'POST':
        for user in users:
            if user.is_super:
                continue

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
