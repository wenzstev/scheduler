from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field 
from src.data.models import User, Appointment 
from marshmallow import Schema, ValidationError, fields, validate, pre_load, pre_dump
from werkzeug.security import generate_password_hash
from datetime import datetime

def is_15_minute_chunk(dt):
    if dt.minute %15 != 0 or dt.second != 0 or dt.microsecond != 0:
        raise ValidationError('DateTime must be on a 15 minute increment.')

class UserSchema(SQLAlchemySchema):
    class Meta: 
        model = User 
        load_instance = True 
    
    id = auto_field()
    firstname = auto_field()
    lastname = auto_field()
    email = auto_field()
    is_provider = auto_field()
    

class AppointmentSchema(SQLAlchemySchema):
    class Meta:
        model = Appointment
        load_instance = True 

    id = auto_field()
    starttime = auto_field()
    provider_id = auto_field()
    client_id = auto_field()
    is_confirmed = auto_field()
    confirmation_deadline = auto_field()


class CreateAppointmentsSchema(Schema):
    starttime = fields.DateTime(required=True, validate=is_15_minute_chunk)
    endtime = fields.DateTime(required=True, validate=is_15_minute_chunk)
    provider_email = fields.Email(required=True)
    provider_password = fields.Str(required=True, load_only=True)

class BookAppointmentSchema(Schema):
    client_email = fields.Email(required=True)
    client_password = fields.Str(required=True, load_only=True)

