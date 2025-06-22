from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.validators import DataRequired, Length

from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()],
                    render_kw={"placeholder": "Введите логин"})
    password = PasswordField("Пароль", validators=[DataRequired()],
                             render_kw={"placeholder": "Введите пароль"})
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()],
                           render_kw={"placeholder": "Придумайте логин"})

    password = PasswordField("Пароль", validators=[
        DataRequired(),
        Length(min=6, message="Пароль должен содержать минимум 6 символов")
    ], render_kw={"placeholder": "Придумайте пароль", "id": "password"})

    confirm = PasswordField("Повторите пароль", validators=[
        DataRequired()
    ], render_kw={"placeholder": "Повторите пароль"})

    submit = SubmitField("Зарегистрироваться")
    
class SubmitTicketForm(FlaskForm):
    room = StringField("Номер кабинета", validators=[DataRequired()])
    category = SelectField("Категория", choices=[
        ('Принтер', 'Принтер'),
        ('Компьютер', 'Компьютер'),
        ('Смартфон', 'Смартфон'),
        ('Интернет', 'Интернет'),
        ('Доска', 'Доска'),
        ('Проектор', 'Проектор'),
        ('Иное', 'Иное'),
    ], validators=[DataRequired()])
    problem = StringField("Проблема", validators=[DataRequired()])
    submit = SubmitField("Отправить")

