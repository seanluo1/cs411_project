from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    user_id = session.get('user_id')

    friends = db.execute(
        "SELECT FirstName, LastName FROM User, (SELECT f.FollowerId FROM Follows f WHERE f.FolloweeId = ? AND f.FolloweeId IN ( SELECT ff.FollowerID FROM Follows ff WHERE ff.FolloweeID = f.FollowerId )) as temp WHERE User.Id == temp.FollowerId",
        (user_id,)
    ).fetchall()

    # friends = db.execute(
    #     "SELECT u.FirstName FROM User u JOIN Follows f ON f.FollowerId = u.Id JOIN Follows ff ON (ff.FolloweeId, ff.FollowerId) = (f.FollowerId, f.FolloweeId) NATURAL JOIN User uf WHERE u.Id = ? GROUP BY f.FolloweeId",
    #     (user_id,)
    # ).fetchall()

    friend_list = []
    for friend in friends:
        friend_list.append(dict(friend))

    return render_template('home/index.html', data = friend_list)