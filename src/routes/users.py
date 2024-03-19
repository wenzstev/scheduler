from flask import (
    Blueprint, jsonify, request
)
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from . import db 

from src.data.models import User
from src.data.schemas import UserSchema

from werkzeug.security import generate_password_hash


bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/<int:user_id>', methods=(['GET']))
def users(user_id):
    user = User.query.get(user_id)
    if user is None:
        return {"message": f"No user with id {user_id} found."}, 404
    
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user))

@bp.route('/', methods=['POST'])
def create_user():
    password = request.json.get('password')
    user_data = request.json.copy()
    user_data.pop('password', None)
    
    try: 
        user_schema = UserSchema(session=db.session)
        user = user_schema.load(user_data)
        user.password = generate_password_hash(password)

        db.session.add(user)
        db.session.commit()
        
        response_data = user_schema.dump(user)
        return jsonify(response_data), 201

    except ValidationError as err:
        return jsonify(err.messages), 400
    except IntegrityError as err:
        return jsonify(err.detail), 400 #FIXME bad error



