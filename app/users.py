from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from .auth import login_required
from .db import get_db
import json

bp = Blueprint('users', __name__)


@bp.route("/users")
@login_required
def all_users():
    current_user_id = session.get('user_id')
    db_instance = get_db()
    user_table = db_instance.execute("SELECT * FROM User")
    follows_row = db_instance.execute("SELECT FolloweeId FROM Follows WHERE FollowerId = ?", (current_user_id,)).fetchall()
    all_users = {}

    follows = [item[0] for item in follows_row]

    for item in user_table.fetchall():
        temp_dict = {}
        user_id = item[0]
        temp_dict["first_name"] = item[1]
        temp_dict["last_name"] = item[2]

        all_users[user_id]= temp_dict


    return render_template("nav_bar/all_users.html", data = (all_users, follows))


@bp.route("/users/id/<int:user_id>", methods=['GET', 'POST'])
@login_required
def user_page(user_id):
    db_instance = get_db()
    user = db_instance.execute('SELECT * FROM User WHERE id = ?', (user_id,)).fetchone()

    user_dict = {}
    user_dict['id'] = user[0]
    user_dict['name'] = user[1] + " " + user[2]

    liked_songs = db_instance.execute('SELECT S.SongId, S.SongName, S.Genre, S.Song_Url From User U join Likes L on U.Id == L.UserId Join Song S on S.SongId == L.SongId Where U.Id == ?', (user[0],)).fetchall()


    if request.method == "POST":
        if session.get('user_id') == user[0]:
            print("cant follow self")
        else:
            db_instance.execute(
                'INSERT OR REPLACE INTO Follows (FollowerId, FolloweeId) Values (?, ?)',
                (session.get('user_id'), user[0])
            )
            db_instance.commit()

    return render_template("home/public.html", data=user_dict, song_data=liked_songs)
