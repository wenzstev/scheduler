import os

from flask import Flask, jsonify
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


    from routes import appointments, users
    app.register_blueprint(appointments.bp)
    app.register_blueprint(users.bp)

    with app.app_context():
        db.create_all()

    @app.errorhandler(404)
    def json_404(e):
        return jsonify(error="Resource not found."), 404 # TODO: improve 404 error message
    
    from src.etc.remove_expired import init_scheduler
    init_scheduler(app)

    return app