from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    name = StringField('имя', validators=[DataRequired()])
    surname = StringField('фамилия', validators=[DataRequired()])
    age = IntegerField('возраст')
    position = StringField('позиция')
    speciality = StringField('специальность')
    address = TextAreaField("адрес")
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')