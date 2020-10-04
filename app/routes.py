import pprint
import sqlite3

import redis
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import BotLogSelect, MessageShow, EditMessage, Post
from config import bot


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
                edt.line.data = mess
            return render_template('edit.html', title='Messages', msg=msg, edt=edt, mess=mess.split('\n'))
        else:
            flash('incorrect username or password')
    elif edt.validate_on_submit():
        with redis.Redis(db=1) as db:
            db.set(message, edt.line.data)
        flash('Message has been edited')
    return render_template('edit.html', title='Edit messages', msg=msg)

@app.route('/post/', methods=['GET', 'POST'])
def post():
    post = Post()
    if post.validate_on_submit():
        if(post.password.data == 'cock' and post.username.data == 'admin'):
            if(post.checks.data == []):
                flash('No selected form')
                return render_template('post.html', title='Post', forms=post)
            else:
                users = ''
                for user in post.checks.data:
                    users += "'" + user + "'" + ' or '
                users = users[:len(users)-4]
                text = post.line.data
                sql = 'SELECT id FROM user WHERE type={}'.format(users)
                connection = sqlite3.connect(database = "Database.db", timeout= 5)
                cursor = connection.cursor()
                cursor.execute(sql)
                res = cursor.fetchall()
                for user_id in res:
                    print(user_id, text)
                    bot.send_message(chat_id=user_id[0],text=text)

        else:
            flash('incorrect username or password')
    return render_template('post.html', title='Post', forms=post)