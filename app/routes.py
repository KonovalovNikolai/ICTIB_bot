import pprint

import redis
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import BotLogSelect, MessageShow, EditMessage


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

@app.route('/message/', methods=['GET', 'POST'])
def message():
    msg = MessageShow()
    if msg.validate_on_submit():
        if(msg.password.data == 'cock' and msg.username.data == 'admin'):
            data = {}
            with redis.Redis(db=1) as db:
                keys = db.keys('*')
                keys = [int(key) for key in keys]
                keys.sort()
                data = {key: db.get(key).decode("utf-8") for key in keys}
            return render_template('message.html', title='Messages', msg=msg, messages=data)
        else:
            flash('incorrect username or password')
    return render_template('message.html', title='Messages', msg=msg)

@app.route('/message/<message>/', methods=['GET', 'POST'])
def edit(message):
    msg = MessageShow()
    edt = EditMessage()
    if msg.validate_on_submit():
        if(msg.password.data == 'cock' and msg.username.data == 'admin'):
            mess = ''
            with redis.Redis(db=1) as db:
                mess = db.get(message).decode("utf-8")
            return render_template('edit.html', title='Messages', msg=msg, edt=edt, mess=mess)
        else:
            flash('incorrect username or password')
    elif edt.validate_on_submit():
        with redis.Redis(db=1) as db:
            db.set(message, edt.line.data)
        flash('Message has been edited')
        return render_template('edit.html', title='Messages', msg=msg, edt=edt, mess=edt.line.data)
    return render_template('edit.html', title='Edit messages', msg=msg)