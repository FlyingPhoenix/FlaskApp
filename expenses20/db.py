import sqlite3

import click
from flask import Flask
from flask import current_app, g
from flask.cli import with_appcontext

app = Flask(__name__)

DATABASE = 'db_expenses.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def insert_db(query, args=()):
    con = get_db()
    cur = con.execute(query, args)
    con.commit()
    cur.close()
    return {'Result': 'Success!', 'Id': cur.lastrowid}


def select_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
