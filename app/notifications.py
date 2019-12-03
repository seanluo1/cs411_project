from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from .auth import login_required
from .db import get_db

from flask_pymongo import pymongo
import json



bp = Blueprint('notifications', __name__)

@bp.route("/all_notifications")
@login_required
def all_notifications():

    return render_template("nav_bar/notifications.html")



