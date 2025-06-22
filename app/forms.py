from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()],
                    render_kw={"placeholder": "Введите логин"})
    password = PasswordField("Пароль", validators=[DataRequired()],
                             render_kw={"placeholder": "Введите пароль"})
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=3, max=25)],
    render_kw={"placeholder": "Введите логин"})
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)],
    render_kw={"placeholder": "Введите пароль"})
    confirm = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')],
    render_kw={"placeholder": "Повторите пароль"})
    submit = SubmitField('Зарегистрироваться')

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

