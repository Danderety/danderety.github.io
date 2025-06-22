from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Повторите пароль', validators=[
        DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')


class SubmitTicketForm(FlaskForm):
    room = StringField('Номер кабинета', validators=[DataRequired()])
    category = SelectField('Категория', choices=[
        ('Принтер', 'Принтер'),
        ('Компьютер', 'Компьютер'),
        ('Смартфон', 'Смартфон'),
        ('Сеть', 'Сеть')
    ], validators=[DataRequired()])
    problem = StringField('Проблема', validators=[DataRequired()])
    attachment = FileField('Прикрепить фото', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Только изображения!')
    ])
    submit = SubmitField('Отправить')
