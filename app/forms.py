from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField
from wtforms.widgets import TextArea, ListWidget, CheckboxInput
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class BotLogSelect(LoginForm):
    botlog = SubmitField('botlog.log')
    vklog = SubmitField('vklog.log')

class MessageShow(LoginForm):
    show = SubmitField('show')

class EditMessage(FlaskForm):
    line = StringField('message', widget=TextArea() ,validators=[DataRequired()])
    edit = SubmitField('edit')

class Post(LoginForm):
    line = StringField('message', widget=TextArea() ,validators=[DataRequired()])
    choice = ['stud', 'teach', 'abitur']
    data = [(a,a) for a in choice]
    checks = MultiCheckboxField('Label', choices=data)
    post = SubmitField('post')

