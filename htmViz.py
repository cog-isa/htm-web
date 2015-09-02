import json
from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from flask import session
from models import User
from utils import get_hash
from peewee import DoesNotExist
from flask import jsonify
import jsonpickle
from flask import Response
from sockets import SocketClient

from htm_core_class import HTMCore

app = Flask(__name__)


@app.route('/')
def htm_main():
    return render_template("basic.html")


@app.route('/htmSettings/')
def htm_settings():
    return render_template("htmSettings.html")


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
        # res=connection.turn_on_htm_server(port)
        # временная заглушка
        # core = HTMCore()
        # res=jsonpickle.encode(core)
        # print(res)
        client = SocketClient(10100)
        client.request(port)
        client.close()
        client = SocketClient(port)
        res = client.request("")
        client.close()

    return Response(response=res, status=200, mimetype="application/json")


@app.route('/get_data_from_htm/')
def get_data_from_htm():
    if 'user_mail' in session:
        user = User.get(User.mail == session['user_mail'])
        port = user.port
        res=connection.receive(port)
        print(res)
        return res


@app.route('/stop_java_server/', methods=['POST'])
def stop_java_server():
    if 'user_mail' in session:
        user = User.get(User.mail == session['user_mail'])
        port = user.port
        if connection.test_connect(port):
            connection.stop_htm_server(port)
            print('stopped')

    return jsonify({'data': str('ok')})


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


def turn_off_all_java_machines():
    q = User.select()
    for i in q:
        connection.stop_htm_server(i.port)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'AAJFjp3141`15123`;ewr[][/fw;jq'
    # turn_off_all_java_machines()

    app.run()
