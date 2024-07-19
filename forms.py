
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class PurchaseForm(FlaskForm):
    product_id = IntegerField('ID del Producto', validators=[DataRequired()])
    quantity = IntegerField('Cantidad', validators=[DataRequired()])
    submit = SubmitField('Comprar')

class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    message = TextAreaField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Nombre del Equipo', validators=[DataRequired()])
    captain = StringField('Nombre del Capitán', validators=[DataRequired()])
    submit = SubmitField('Registrar')

