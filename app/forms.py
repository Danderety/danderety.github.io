from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(), EqualTo('password', message='Пароли не совпадают')
    ])
    submit = SubmitField('Зарегистрироваться')

class TicketForm(FlaskForm):
    room_number = StringField('Номер кабинета', validators=[DataRequired()])
    category = SelectField('Категория', choices=[('Принтер', 'Принтер'), ('Компьютер', 'Компьютер'),
                                                 ('Смартфон', 'Смартфон'), ('Сеть', 'Сеть')])
    issues = TextAreaField('Описание проблемы (или список выбранных чекбоксов)')
    comment = TextAreaField('Комментарий (необязательно)')
    submit = SubmitField('Отправить заявку')
