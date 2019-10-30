import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from . import db
index_blueprint = Blueprint("index", __name__ ,template_folder='templates')

@index_blueprint.route("/add_user", methods=['POST'])
def test1():
    data = request.get_json()
    first_name = data["first_name"] 
    last_name = data["last_name"]
    email = data["email"]
    password = data["password"]

    db_instance = db.get_db()
    db_instance.execute(
        'INSERT INTO User(FirstName, LastName, Email, Password) VALUES (?, ?, ?, ?)',
        (first_name, last_name, email, password)
    )
    db_instance.commit()

    return render_template("hello.html")


@index_blueprint.route("/check_users_db")
def test2():
    db_instance = db.get_db()
    user_table = db_instance.execute("SELECT * FROM User")
    all_users = {}

    for item in user_table.fetchall():
        all_users["user_id"] = item[0]
        all_users["first_name"] = item[1]
        all_users["last_name"] = item[2]
        all_users["email"] = item[3]
        all_users["password"] = item[4]

    print(all_users)

    return render_template("hello.html")


