from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app import db
from app.models import User, Ticket
from app.forms import LoginForm, RegisterForm, SubmitTicketForm

routes_bp = Blueprint('routes_bp', __name__)

@routes_bp.route('/')
def home():
    return redirect(url_for('routes_bp.login'))

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('routes_bp.admin_panel') if user.is_admin else url_for('routes_bp.submit_ticket'))
        return redirect(url_for('routes_bp.login', error=1))

    error = request.args.get('error') == '1'
    return render_template('login.html', form=form, error=error)




@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = request.args.get("error")

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            return redirect(url_for('routes_bp.register', error=1))

        if form.password.data != form.confirm.data:
            return redirect(url_for('routes_bp.register', error=2))

        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('routes_bp.login'))
   
    return render_template('register.html', form=form, error=error)


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
            status='Выполняется',
            user_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('routes_bp.submit_ticket', success=1))
        
    success = request.args.get('success') == '1'
    my_tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.timestamp.desc()).limit(10).all()
    return render_template('submit.html', form=form, my_tickets=my_tickets, success=success)



@routes_bp.route('/admin', methods=['GET'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        
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
    ticket.status = 'Выполнено' if data.get('done') else 'Выполняется'
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
        return redirect(url_for('routes_bp.submit_ticket'))

    users = User.query.all()

    if request.method == 'POST':
        # --- Создание нового пользователя ---
        if 'create_user' in request.form:
            username = request.form.get('new_username', '').strip()
            password = request.form.get('new_password', '').strip()
            role = request.form.get('new_role', 'user')

            if username and password:
                existing_user = User.query.filter_by(username=username).first()
                if not existing_user:
                    hashed = generate_password_hash(password)
                    new_user = User(username=username, password=hashed)
                    if role == 'admin':
                        new_user.is_admin = True
                        new_user.admin_assigned_at = datetime.utcnow()
                    db.session.add(new_user)
                    db.session.commit()

            return redirect(url_for('routes_bp.users'))

        # --- Обновление/удаление существующих пользователей ---
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
        return redirect(url_for('routes_bp.users'))

    return render_template('users.html', users=users)

