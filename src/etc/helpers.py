from flask import jsonify
from marshmallow import ValidationError


def validate_schema(schema, data):
    try:
        return schema.load(data), None, None
    except ValidationError as err:
        return None, jsonify(err.messages), 400 # could probably use abort() here
    
