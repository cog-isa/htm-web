import sys
sys.path.insert(0, "htm-core/")

from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from flask import session
from models import User, RunSettings
from utils import get_hash
from peewee import DoesNotExist
from flask import Response
from sockets import SocketClient

app = Flask(__name__)


@app.route('/')
def htm_main():
    return render_template("basic.html")


@app.route('/htmSettings/')
def htm_settings():
    settings = []

    if 'user_mail' in session:
        user = User.get(User.mail == session['user_mail'])
        print(user.get_id())
        try:
            res = RunSettings.select().where(RunSettings.user == user.get_id())
            for i in res:
                settings.append(i)
        except RunSettings.DoesNotExist:
            print("RunSettings empty")

    return render_template("htmSettings.html", settings=settings)


@app.route('/htmRun/')
def htm_run():
    return render_template("htmRun.html")


@app.route('/turn_on_java_server/', methods=['POST'])
def turn_on_java_server():
    print("go")
    res = '{"test": "test"}'
    if 'user_mail' in session:
        user = User.get(User.mail == session['user_mail'])
        port = user.port
        client = SocketClient(10100)
        client.request(port)
        client.close()
        client = SocketClient(port)
        res = client.request("")
        client.close()

    return Response(response=res, status=200, mimetype="application/json")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['email']
        password = request.form['password']
        q = None
        try:
            q = User.get(User.mail == mail)
        except DoesNotExist:
            pass

        if q and get_hash(password) == q.password:
            session['user_mail'] = mail
            return redirect(url_for('htm_settings'))

    return redirect(url_for('htm_main'))


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('htm_settings'))


@app.route('/add_new_conf/')
def add_new_conf():
    RunSettings.create(json_string='', name='Новая конфигурация', user=User.get(User.mail == session['user_mail']))


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'AAJFjp3141`15123`;ewr[][/fw;jq'

    app.run()
