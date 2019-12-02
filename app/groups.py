from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from .auth import login_required
from .db import get_db

from flask_pymongo import pymongo
import json



bp = Blueprint('groups', __name__)

@bp.route("/groups")
@login_required
def all_groups():
    current_user_id = session.get('user_id')
    db_instance = get_db()
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["groups"]

    my_groups = list(mycol.find({ "admin_id": current_user_id }))


    return render_template("nav_bar/my_groups.html", data =my_groups )


@bp.route('/new_group', methods=('GET', 'POST'))
def new_group():
    current_user_id = session.get('user_id')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["groups"]

    new_group = {}
    if request.method == 'POST':
        db = get_db()

        group_name = request.form['groupName']

        new_group = {"id": 1, "name": group_name, "admin_id": current_user_id}
        mycol.insert_one(new_group)

        return redirect(url_for('groups.all_groups'))

    return render_template('nav_bar/add_group.html')
