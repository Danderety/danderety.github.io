from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()  # если нужно пересоздать
    db.create_all()

    # Создание суперпользователя, если его нет
    if not User.query.filter_by(username='root').first():
        superuser = User(
            username='root',
            password=generate_password_hash('root'),
            is_admin=True,
            is_super=True,
            admin_assigned_at=None
        )
        db.session.add(superuser)
        db.session.commit()
        print("Суперпользователь создан.")
    else:
        print("Суперпользователь уже существует.")
