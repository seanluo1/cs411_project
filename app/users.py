from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .auth import login_required
from .db import get_db
import json

bp = Blueprint('users', __name__)

@bp.route("/users")
@login_required
def all_users():
    db_instance = get_db()
    user_table = db_instance.execute("SELECT * FROM User")
    all_users = {}

    for item in user_table.fetchall():
        temp_dict = {}
        user_id = item[0]
        temp_dict["first_name"] = item[1]
        temp_dict["last_name"] = item[2]
        all_users[user_id]= temp_dict

    print(all_users)

    return render_template("nav_bar/all_users.html", data = all_users)


@bp.route("/users/id/<int:user_id>")
@login_required
def user_page(user_id):
    db_instance = get_db()
    user = db_instance.execute('SELECT * FROM User WHERE id = ?', (user_id,)).fetchone()

    user_dict = {}
    user_dict['id'] = user[0]
    user_dict['name'] = user[1] + " " + user[2]

    liked_songs = db_instance.execute('SELECT S.SongId, S.SongName, S.Genre, S.Song_Url From Likes L Join Song S on S.SongId == L.SongId Where L.UserId == ?', (user_id,)).fetchall()
    print(liked_songs)

    return render_template("home/public.html", data=user_dict, song_data=liked_songs)
