import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pymongo import pymongo




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    Bootstrap(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    dblist = myclient.list_database_names()
    if "mydatabase" in dblist:
        print("The database exists.")
    else:
        print("Doesn't exist.")
    mydb = myclient["mydatabase"]

    from . import db
    db.init_app(app)

    from . import groups
    app.register_blueprint(groups.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import songs
    app.register_blueprint(songs.bp)

    from . import users
    app.register_blueprint(users.bp)

    from . import notifications
    app.register_blueprint(notifications.bp)

    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    return app