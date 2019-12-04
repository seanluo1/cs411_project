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


    return render_template("groups/my_groups.html", data =my_groups )


@bp.route('/new_group', methods=('GET', 'POST'))
@login_required
def new_group():
    current_user_id = session.get('user_id')

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["groups"]
    error = None

    new_group = {}
    if request.method == 'POST':
        db = get_db()

        group_name = request.form['groupName']
        
        my_groups = list(mycol.find({ "admin_id": current_user_id }, {"name": 1, "_id": 0}))
        for group in my_groups:
            if group['name'] == group_name:
                error = "Group Name exists"
                break

        if error:
            flash(error, 'danger')
            return render_template('groups/add_group.html')


        new_group = {"id": mycol.count() + 1, "name": group_name, "admin_id": current_user_id, "members": [current_user_id]}
        mycol.insert_one(new_group)

        return redirect(url_for('groups.all_groups'))

    return render_template('groups/add_group.html')


@bp.route("/groups/id/<int:group_id>", methods=['GET', 'POST'])
@login_required
def group_page(group_id):
    current_user_id = session.get('user_id')
    db_instance = get_db()
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["groups"]
    error = None


    if request.method == 'POST':
        user_id_to_add = request.form['id']
        

    
    group = list(mycol.find({ "id": group_id }))[0]
    group_member_ids = group['members']

    if current_user_id not in group_member_ids:
        flash(error, 'danger')
        return redirect(url_for('home.index'))
    
    #print(group_member_ids)
    group_members_table = db_instance.execute("SELECT * FROM User WHERE id IN (%s)" % ','.join('?'*len(group_member_ids)), group_member_ids).fetchall()
    #print(group_members_table)
    
    #print(group)
    group_members = []

    

    for member in group_members_table:
        member_dict = {}
        member_dict["id"] = member[0]
        member_dict["name"] = member[1] + " " + member[2]
        member_dict["sotw"] = member[5]
        group_members.append(member_dict)

    #print(group_members)

    return render_template("groups/group_page.html", data=(group, group_members)  )




@bp.route("/groups/id/<int:group_id>/add_member", methods=['GET', 'POST'])
@login_required
def add_member(group_id):
    db_instance = get_db()
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["groups"]
    error = None

    group = list(mycol.find({ "id": group_id }))[0]
    print(group)

    all_results = {}

    if request.method == 'POST':

        query = request.form['searchName']
        formatted_query = "\"%" + query + "%\""
        sql_query = "SELECT * FROM User WHERE FirstName || ' ' || LastName LIKE " + formatted_query
        print(sql_query)
        query_results = db_instance.execute(sql_query)
        all_results = []
        for item in query_results.fetchall():
            user_dict = {}
            user_dict["id"] = item[0]
            user_dict["name"] = item[1] + ' ' + item[2]
            all_results.append(user_dict)
        return render_template("groups/add_member.html", data=(group, all_results)  )



    return render_template("groups/add_member.html", data=(group, [])  )