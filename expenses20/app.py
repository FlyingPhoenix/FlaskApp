from flask import Blueprint, Flask
from flask import request
from flask import jsonify
from flask import session

from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from flask_prometheus_metrics import register_metrics

from datetime import datetime
from const import STUB_RESULT
from controllers.user import User
from controllers.expenses_types import ExpensesTypes
from controllers.expenses import Expenses
from controllers.statistics import Statistics

#
# Constants
#

CONFIG = {"version": "v0.1.2", "config": "staging"}
MAIN = Blueprint("main", __name__)

#
# Main app
#

@MAIN.route("/")
def index():
    return "This is the main page."


@MAIN.route('/users', methods=['GET', 'POST'])
def user():
    """
    API аккаунтов пользователей
    """
    if request.method == 'POST':
        name = request.form['name']
        return User().create_user(name)
    if request.method == 'GET':
        return jsonify(User().get_all_users())
    return STUB_RESULT


@MAIN.route('/sign-in', methods=['POST', 'LOCK'])
def login():
    """
    API авторизации
    """
    if request.method == 'POST':
        if 'user_id' in session:
            return {'Result': 'You are already logged in'}
        user_id = User().get_user_id(request.form['name'])
        if user_id:
            session['user_id'] = User().get_user_id(request.form['name'])
            return {'Result': 'Authorization was successful', 'id': session['user_id']}
        return {'Result': 'Login have not been found'}

    if request.method == 'LOCK':
        session.pop('user_id', None)
        return {'Result': 'You successfully logged out'}


@MAIN.route('/expenses-types', methods=['POST', 'GET'])
def expenses_types():
    """
    API типов расходов
    """
    if request.method == 'POST':
        name = request.form['name']
        return ExpensesTypes().create_type(name)
    if request.method == 'GET':
        return jsonify(ExpensesTypes().get_all_types())
    return STUB_RESULT


@MAIN.route('/expenses', methods=['POST', 'GET'])
def expenses():
    """
    API записи расходов
    """
    if 'user_id' not in session:
        return {'Result': 'You should sign in'}

    if request.method == 'POST':
        params = {
            'user': session['user_id'],
            'type': request.form['type'],
            'sum': request.form['sum'],
            'description': request.form['description'],
            'r_date': datetime.strptime(request.form['r_date'], '%Y-%m-%d')
        }
        return Expenses().create_record(params)


@MAIN.route('/statistics/month', methods=['GET'])
def month_sum():
    """
    Получить суммы расходов по пользователяем за месяц
    """
    if request.method == 'GET':
        return jsonify(Statistics().month_sum(request.args['year'], request.args['month']))
    return STUB_RESULT


# @MAIN.route("/banana")
# def banana():
#     return "A banana is an elongated, edible fruit – botanically a berry – produced by several kinds of large herbaceous flowering plants in the genus Musa."
#
#
# @MAIN.route("/apple")
# def apple():
#     return "An apple is an edible fruit produced by an apple tree (Malus domestica). Apple trees are cultivated worldwide and are the most widely grown species in the genus Malus."
#
#
# @MAIN.route("/dragonfruit")
# def dragonfruit():
#     return "A pitaya (/pɪˈtaɪ.ə/) or pitahaya (/ˌpɪtəˈhaɪ.ə/) is the fruit of several different cactus species indigenous to the Americas. Pitaya usually refers to fruit of the genus Stenocereus, while pitahaya or dragon fruit refers to fruit of the genus Hylocereus, both in the family Cactaceae."


def register_blueprints(app):
    """
    Register blueprints to the app
    """
    app.register_blueprint(MAIN)


def create_app(config):
    """
    Application factory
    """
    app = Flask(__name__)

    # Set the secret key to some random bytes. Keep this really secret!
    app.secret_key = b'_34jgkd8!u40u2'

    register_blueprints(app)
    register_metrics(app, app_version=config["version"], app_config=config["config"])
    return app

#
# Dispatcher
#

def create_dispatcher() -> DispatcherMiddleware:
    """
    App factory for dispatcher middleware managing multiple WSGI apps
    """
    main_app = create_app(config=CONFIG)
    return DispatcherMiddleware(main_app.wsgi_app, {"/metrics": make_wsgi_app()})

#
# Run
#

if __name__ == "__main__":
    run_simple(
         "0.0.0.0",
         5000,
         create_dispatcher(),
         use_reloader=True,
         use_debugger=True,
         use_evalex=True,
    )
