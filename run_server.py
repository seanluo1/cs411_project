from flask import Flask
from views.routes import index_blueprint
from flask_sqlalchemy import SQLAlchemy


# TODO: connect db to sql sb

#db = SQLAlchemy()
app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = ""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db.init_app(app)
app.register_blueprint(index_blueprint)
app.run(debug=True)