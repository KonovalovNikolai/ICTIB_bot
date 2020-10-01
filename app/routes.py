from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import BotLogSelect

@app.route('/', methods=['GET', 'POST'])
@app.route('/logs/', methods=['GET', 'POST'])
def logs():
    log = BotLogSelect()
    if log.validate_on_submit():
        if(log.password.data == 'cock' and log.username.data == 'admin'):
            lable = 'botlog.log' if log.botlog.data else 'vklog.log'
            return render_template('logs.html', title='Logs', log=log, file=open('Logs/' + lable))
        else:
            flash('incorrect username or password')
    return render_template('logs.html', title='Logs', log=log, file=None)