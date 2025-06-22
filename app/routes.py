from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.create import db
from app.models import User, Ticket
from app.forms import LoginForm, RegisterForm, TicketForm

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
def index():
    return redirect(url_for('routes.login'))


@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.submit_ticket'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('routes.submit_ticket'))
        flash('Неверные данные для входа', 'danger')
    return render_template('login.html', form=form)


@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.submit_ticket'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Пользователь уже существует', 'warning')
        else:
            user = User(
                username=form.username.data,
                password_hash=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрированы. Войдите.', 'success')
            return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)


@routes_bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            room_number=form.room_number.data,
            category=form.category.data,
            issues=form.issues.data,
            comment=form.comment.data,
            created_by_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Заявка успешно отправлена!', 'success')
        return redirect(url_for('routes.submit_ticket'))
    return render_template('submit_ticket.html', form=form)


@routes_bp.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        flash('Доступ только для администраторов', 'danger')
        return redirect(url_for('routes.submit_ticket'))

    tickets = Ticket.query.order_by(Ticket.timestamp.desc()).all()
    return render_template('admin_panel.html', tickets=tickets)


@routes_bp.route('/users')
@login_required
def users():
    if not current_user.is_superadmin:
        abort(403)

    users = User.query.order_by(User.id).all()
    return render_template('users.html', users=users)


@routes_bp.route('/make_admin/<int:user_id>', methods=['POST'])
@login_required
def make_admin(user_id):
    if not current_user.is_superadmin:
        abort(403)

    user = User.query.get_or_404(user_id)
    if not user.is_superadmin and user.role != 'admin':
        user.role = 'admin'
        db.session.commit()
        flash(f"Пользователь {user.username} теперь админ.", 'success')
    else:
        flash("Невозможно изменить этого пользователя", 'warning')

    return redirect(url_for('routes.users'))


@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))
