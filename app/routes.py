import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import db
index_blueprint = Blueprint("index", __name__ ,template_folder='templates')

@index_blueprint.route("/")
def test1():
    db_instance = db.get_db()
    db_instance.execute(
        'INSERT INTO User(Id, FirstName, LastName, Email, Password) VALUES (?, ?, ?, ?, ?)',
        (1, "Bob", "Smith", "bob@smith.com", "password")
    )
    db_instance.commit()

    return render_template("hello.html")


@index_blueprint.route("/woo")
def test2():
    db_instance = db.get_db()
    db_instance.execute(
        'SELECT * FROM User'
    )
    

    return render_template("hello.html")


