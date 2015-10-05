import sys
from utils import get_hash
from settingsform import SettingsForm

sys.path.insert(0, "htm-web/")
sys.path.insert(0, "htm-core/")
sys.path.insert(0, "htm-core/spatialPooler")
sys.path.insert(0, "htm-core/temporalPooler")
sys.path.insert(0, "htm-core/gens")
sys.path.insert(0, "htm-core/apps")

from sockets import SystemMessages

import json
import utils
from flask import Flask, request, redirect, url_for, flash
from flask.templating import render_template
from flask import session
from models import User, RunSettings

from peewee import DoesNotExist
from flask import jsonify
from flask import Response
from sockets import SocketClient

from htm_core_class import HTMCore
import wtforms_json

#  In order to start using WTForms-JSON, you need to first initialize the extension.
#  This monkey patches some classes and methods within WTForms and adds JSON handling support
wtforms_json.init()

app = Flask(__name__)


@app.route('/')
def htm_main():
    return render_template("basic.html")


@app.route('/htmSettings/', methods=['GET', 'POST'])
def htm_settings():
    settings = []

    if 'user_mail' in session:
        user = User.get(User.mail == session['user_mail'])

        if request.method == 'POST':  # and form.validate():
            form = SettingsForm(request.form)
            set = RunSettings.select().where(RunSettings.id == int(request.form['name'].split('form-')[1])).get()
            set.json_string = json.dumps(form.data)
            set.save()
            flash('Конфигурация сохранена')

        try:
            res = RunSettings.select().where(RunSettings.user == user.get_id())
            for set in res:
                # print(json.loads(set.json_string))
                f = SettingsForm()
                if set.json_string != "":
                    f = SettingsForm.from_json(json.loads(set.json_string), skip_unknown_keys=True)

                settings.append({"id": set.id, "data": f})

        except RunSettings.DoesNotExist:
            print("RunSettings empty")
        return render_template("htmSettings.html", settings=settings)

    else:
        return render_template("basic.html")


@app.route('/htmRun/')
def htm_run():
    return render_template("htmRun.html")


######################################################################################################################
@app.route('/turn_on_htm_server/', methods=['POST'])
def turn_on_htm_server():
    print("turn_on_htm_server")
    res = '{"test": "test"}'
    if 'user_mail' in session:
        print("OKOKOK")
        user = User.get(User.mail == session['user_mail'])
        port = user.port
        settings_id = int(request.form['settings_id'])
        client = SocketClient(10100)
        client.request((port, settings_id), SystemMessages.TURN_ON_HTM_WITH_SETTINGS)
        client.close()
        print("OUT_OK")

    return Response(response=res, status=200, mimetype="application/json")


@app.route('/stop_htm_server/', methods=['POST'])
def stop_htm_server():
    print("stop_htm_server")
    res = '{"test": "test"}'
    if 'user_mail' in session:
        user = User.get(User.mail == session['user_mail'])
        port = user.port
        client = SocketClient(port)
        res = client.request(data="", message=SystemMessages.STOP)
        client.close()
        print(res)

    return Response(response=res, status=200, mimetype="application/json")


@app.route('/get_htm_data/', methods=['POST'])
def get_htm_data():
    print("get_htm_data")
    res = '{"test": "test"}'
    if 'user_mail' in session:
        user = User.get(User.mail == session['user_mail'])
        port = user.port

        client = SocketClient(port)
        res = client.request(data="", message=SystemMessages.GET_DATA)
        client.close()


        """
        вывод сериализованных данных в файл
        f = open("out.txt", "w")
        f.write(res)
        f.close()
        """

    return Response(response=res, status=200, mimetype="application/json")


@app.route('/move_and_get_htm_data/', methods=['POST'])
def move_and_get_htm_data():
    print("go")
    res = '{"test": "test"}'
    if 'user_mail' in session:
        user = User.get(User.mail == session['user_mail'])
        port = user.port
        client = SocketClient(port)

        mes=SystemMessages.MOVE
        if request.form['cnt'] == '1':
            mes=SystemMessages.MOVE
        elif request.form['cnt'] == '100':
            mes=SystemMessages.MOVE100
        elif request.form['cnt'] == '1000':
            mes=SystemMessages.MOVE1000

        res = client.request(data="", message=mes)
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


@app.route('/add_new_conf/', methods=['POST'])
def add_new_conf():
    RunSettings.create(json_string='', name='Новая конфигурация', user=User.get(User.mail == session['user_mail']))
    return 'OK'


@app.route('/remove_conf/', methods=['POST'])
def remove_conf():
    q = RunSettings.delete().where(RunSettings.id == int(request.form['ident']))
    q.execute()
    return 'OK'


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'AAJFjp3141`15123`;ewr[][/fw;jq'
    # turn_off_all_java_machines()

    app.run()
