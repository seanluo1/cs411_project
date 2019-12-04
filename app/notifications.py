from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from .auth import login_required
from .db import get_db
import json

bp = Blueprint('notifications', __name__)

@bp.route("/notifications")
def notifications():
    db_instance = get_db()
    user_id = session.get('user_id')

    my_notifs = db_instance.execute("SELECT * FROM PushNotification WHERE UserId=?", (user_id, ))
    all_notifs = {}
    for item in my_notifs.fetchall():
        temp_dict = {}
        notif_id = item[0]
        temp_dict["msg"] = item[2]
        temp_dict["song_url"] = item[3]

        all_notifs[notif_id] = temp_dict

    return render_template("nav_bar/notifications.html", data = all_notifs)
