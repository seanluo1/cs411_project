from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .auth import login_required
from .db import get_db
import json

bp = Blueprint('songs', __name__)

@bp.route('/add_song', methods=('GET', 'POST'))
def add_song():
    if request.method == 'POST':
        db = get_db()

        name = request.form['song_name']
        genre = request.form['genre']
        url = request.form['url']



        db.execute(
        'INSERT INTO Song (SongName, Genre, Song_Url) VALUES (?, ?, ?)',
        (name, genre, url))

        db.commit()

    return render_template('nav_bar/add_song.html')

@bp.route("/all_songs")
def all_songs():
    db_instance = get_db()
    user_table = db_instance.execute("SELECT * FROM Song")
    all_songs = {}

    for item in user_table.fetchall():
        temp_dict = {}
        user_id = item[0]
        temp_dict["song_name"] = item[1]
        temp_dict["genre"] = item[2]
        temp_dict["url"] = item[3]
        all_songs[user_id]= temp_dict

    print(all_songs)

    return render_template("nav_bar/my_songs.html", data = all_songs)

@bp.route('/delete_song', methods=('GET', 'POST'))
def delete_song():
    if request.method == 'POST':
        db = get_db()
        song_id = request.form['song_id']

        db.execute(
            'DELETE FROM Song WHERE SongId=(?)',
            (song_id)
        )

        db.commit()

    return render_template('nav_bar/delete_song.html')

@bp.route('/edit_song', methods=('GET', 'POST'))
def edit_song():
    if request.method == 'POST':
        db = get_db()
        song_id = request.form['song_id']
        name = request.form['song_name']
        genre = request.form['genre']
        url = request.form['url']

        db.execute(
            'UPDATE Song SET SongName = ?, Genre = ?, Song_Url = ?'
            ' WHERE SongId = ?',
            (name,genre, url, song_id)
        )
        db.commit()

    return render_template('nav_bar/edit_song.html')