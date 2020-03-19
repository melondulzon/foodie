from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class SignForm(FlaskForm):
    """
        Flask WTF_Forms was only used for user sign in and sign up.
        Required fields are validated with DataRequired() and
        additional validation is limited to providing a username and
        password no shorter than 4 characters.
    """

    # Fields - require some validation
    username = StringField('Usuari', validators=[DataRequired()])
    password = PasswordField('Contrasenya', validators=[DataRequired()])
    remember = BooleanField("Recorda'm")
    submit = SubmitField('Registrar-me')

    # username
    def validate_username(self, username):
        if len(username.data) < 4:
            raise ValidationError('username must be longer than 4 characters')

    # password
    def validate_password(self, password):
        if len(password.data) < 4:
            raise ValidationError('password must be longer than 4 characters')



