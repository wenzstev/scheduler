from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field 
from src.models import User, Appointment 

class UserSchema(SQLAlchemySchema):
    class Meta: 
        model = User 
        load_instance = True 
    
    id = auto_field()
    firstname = auto_field()
    lastname = auto_field()
    email = auto_field()
    password = auto_field()
    isProvider = auto_field()

class AppointmentSchema(SQLAlchemySchema):
    class Meta:
        model = Appointment
        load_instance = True 

    id = auto_field()
    starttime = auto_field()
    provider_id = auto_field()
    client_id = auto_field()
    isConfirmed = auto_field()