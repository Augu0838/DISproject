from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class LoginForm(FlaskForm):
    #id = IntegerField('userid', validators=[DataRequired()])
    user_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    #fav_station = StringField('favoritestation', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
