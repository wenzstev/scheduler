import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

from src.models import User, Appointment
from src.schemas import UserSchema, AppointmentSchema


bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@bp.route('/<int:appointment_id>', methods=(['GET', 'PUT', 'DELETE']))
def appointments(appointment_id):
    # if get, check for the provider, the start time, and the end time in the url 
    #   return those values

    appointment = Appointment.query.get(appointment_id)
    if appointment is None:
        return {"message": f"No appointment with id {appointment_id} found."}, 404
    

    appointment_schema = AppointmentSchema()
    return jsonify(appointment_schema.dump(appointment))

@bp.route('/', methods=["GET", "POST"])
def create_appointments():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.get(email=email)
        if user is None:
            return {"message": f"No user with email {email} found."}, 400 
        
        if not user.isProvider:
            return {"message": f"User {email} is not a provider in the system. Only providers can create appointment slots."}, 400

        if not check_password_hash(user.password, password):
            return {"message": f"Unauthorized. Password incorrect."}, 403
        


        return {}


    if request.method == "GET":
        appointments = Appointment.query.all() 
        appointment_schema = AppointmentSchema(many=True)
        return jsonify(appointment_schema.dump(appointments))

 


@bp.route('/<int:appointment_id>/confirm', methods=(['PUT']))
def confirm_appt():

    # confirm an appointment, using a provdied appt id
    # requires a user and password of the user who created the appointment

    pass

