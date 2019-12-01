from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    #db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    
    # friends = db.execute( # NOTE this doesn't actually do anything yet
    #     'SELECT u.FirstName, u.LastName'
    #     ' FROM User u JOIN Follows f ON u.Id = f.FolloweeId'
    # ).fetchall()
    #return render_template('home/index.html', first_name=first_name)
    return render_template('home/index.html')