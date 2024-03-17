from flask import (
    Blueprint, g, jsonify, request
)
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from . import db 

from src.models import User
from src.schemas import UserSchema

from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/<int:user_id>', methods=(['GET', 'PUT', 'DELETE']))
def users(user_id):
    user = User.query.get(user_id)
    if user is None:
        return {"message": f"No user with id {user_id} found."}, 404
    
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user))

@bp.route('/', methods=['POST'])
def create_user():
    
    user_data = request.json 

    if 'password' in user_data:
        hashed_password = generate_password_hash(user_data['password'])
        user_data['password'] = hashed_password

    user_schema = UserSchema(session=db.session)
    try: 
        user = user_schema.load(user_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as err:
        return jsonify(err.detail), 400 #FIXME bad error

    response_data = user_schema.dump(user)
    response_data.pop('password', None)
    
    return jsonify(response_data), 201

