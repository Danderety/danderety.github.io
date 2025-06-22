from app.create import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    if not User.query.filter_by(username='Danderety').first():
        admin = User(
            username='Danderety',
            password_hash=generate_password_hash('88005553535!Kirillka12!'),
            role='admin',
            is_superadmin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Супер-админ Danderety создан')
    else:
        print('Супер-админ уже существует')
