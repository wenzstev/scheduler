import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass 

db = SQLAlchemy(model_class=Base)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'src.sqlite'),
        SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
    )

    db.init_app(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try: 
        os.makedirs(app.instance_path)
    except OSError:
        pass 


    from . import appointments, users
    app.register_blueprint(appointments.bp)
    app.register_blueprint(users.bp)

    with app.app_context():
        db.create_all()

    return app