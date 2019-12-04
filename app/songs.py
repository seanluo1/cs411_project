from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
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
        song_url = request.form['song_url']

        db.execute(
        'INSERT INTO Song (SongName, Genre, Song_Url) VALUES (?, ?, ?)',
        (name, genre, song_url))

        db.commit()

    return render_template('nav_bar/add_song.html')

@bp.route("/all_songs", methods=('GET', 'POST'))
def all_songs():
    db_instance = get_db()
    user_table = db_instance.execute("SELECT * FROM Song")
    all_songs = {}
    user_id = session.get('user_id')

    g.user = get_db().execute(
    'SELECT * FROM User WHERE Id = ?', (user_id,)
    ).fetchone()

    if request.method == 'POST':
        current_likes = request.form.getlist("liked_box")
        previous_likes = set()
        like_table = get_db().execute(
        'SELECT * FROM Likes WHERE UserId = ?' ,(g.user["Id"], ))

        for like in like_table:
           like = dict(like)
           previous_likes.add(like["SongId"])

        for song in current_likes:
            db_instance.execute(
                'INSERT OR REPLACE INTO Likes (UserId, SongId) VALUES (?, ?)',
                (g.user["Id"], song)
            )
            db_instance.commit()

        for song in previous_likes:
            if str(song) not in current_likes:
                db_instance.execute(
                'DELETE FROM Likes WHERE UserId=(?) AND SongId=(?)',
                (g.user["Id"], song))
                db_instance.commit()

        sotw_id = request.form.get('sotw_button', None)
        if sotw_id:
            #update current user sotw
            sotw = get_db().execute(
                'SELECT SongName FROM Song WHERE SongId = ?',
                (sotw_id,)
            ).fetchone()
            db_instance.execute(
                'UPDATE User SET SongOfWeek = ? WHERE Id = ?',
                (sotw['SongName'], g.user["Id"],)
            )

            #add notification for all of current user's followers
            followers_col = db_instance.execute("SELECT FollowerId FROM Follows WHERE FolloweeId = ?", (user_id,)).fetchall()
            followers = [item[0] for item in followers_col]
            curr_user = g.user["FirstName"] + " " + g.user["LastName"]
            msg = curr_user + " changed their Song of the Week to " + sotw['SongName'] + "."
            
            sotw_ = get_db().execute(
                'SELECT Song_Url FROM Song WHERE SongId = ?',
                (sotw_id,)
            ).fetchone()
            url = sotw_['Song_Url']

            #push personalized notification into table for all followers
            for person in followers:
                db_instance.execute(
                    "INSERT INTO PushNotification (UserId, MessageText, Song_Url) Values (?,?,?)",
                    (person, msg, url)
                )

        db_instance.commit()
        

    for item in user_table.fetchall():
        temp_dict = {}
        song_id = item[0]
        temp_dict["song_name"] = item[1]
        temp_dict["genre"] = item[2]
        temp_dict["song_url"] = item[3]
        like_table = db_instance.execute("SELECT * FROM Likes ")

        found_in_likes = get_db().execute(
        'SELECT * FROM Likes WHERE UserId = ? AND SongId = ?' ,(g.user["Id"], song_id, )
        ).fetchone()

        if found_in_likes:
            temp_dict["liked"] = "T"
        else:
            temp_dict["liked"] = "F"
        
        temp_dict["sotw"] = item[0] #this value doesn't actually matter

        all_songs[song_id]= temp_dict

    like_table = db_instance.execute("SELECT * FROM Likes")
    for like in like_table:
        print(dict(like))



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
        song_url = request.form['song_url']

        db.execute(
            'UPDATE Song SET SongName = ?, Genre = ?, Song_Url = ?'
            ' WHERE SongId = ?',
            (name,genre, song_url, song_id)
        )
        db.commit()

    return render_template('nav_bar/edit_song.html')