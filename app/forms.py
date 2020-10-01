from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class BotLogSelect(LoginForm):
    botlog = SubmitField('botlog.log')
    vklog = SubmitField('vklog.log')