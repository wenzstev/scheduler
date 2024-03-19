from datetime import datetime, timedelta

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from . import db

from src.models import User, Appointment
from src.schemas import UserSchema, AppointmentSchema, CreateAppointmentsSchema, BookAppointmentSchema
from src.helpers import validate_schema


bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@bp.route('/<int:appointment_id>', methods=(['GET', 'DELETE']))
def appointments(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment is None:
        return {"message": f"No appointment with id {appointment_id} found."}, 404
    

    appointment_schema = AppointmentSchema()
    return jsonify(appointment_schema.dump(appointment))


@bp.route('/', methods=["GET", "POST"])
def create_appointments():
    if request.method == "POST":
        create_appointments, error_response, status_code = validate_schema(CreateAppointmentsSchema(), request.json)
        if error_response:
            return error_response, status_code
        
        provider_email = create_appointments["provider_email"]
        user = User.query.filter_by(email=provider_email).first_or_404() # email is unique, only one result will come

        if not user.is_provider:
            return {"message": f"User {provider_email} is not a provider in the system. Only providers can create appointment slots."}, 403
        
        password = create_appointments["provider_password"]
        if not check_password_hash(user.password, password):
            return {"message": f"Unauthorized. Password incorrect."}, 403
        
        new_appointments = []
        cur = create_appointments["starttime"]
        while cur < create_appointments["endtime"]:
            new_appt = Appointment(starttime=cur, provider_id=user.id)
            new_appointments.append(new_appt)
            cur += timedelta(minutes=15)
        
        db.session.add_all(new_appointments)
        db.session.commit()

        appointment_schema = AppointmentSchema(many=True)
        return jsonify(appointment_schema.dump(new_appointments)), 201



    if request.method == "GET":
        appointments = Appointment.query.all() 
        appointment_schema = AppointmentSchema(many=True)
        return jsonify(appointment_schema.dump(appointments))

 
@bp.route('/<int:appointment_id>/book', methods=(['PUT']))
def book_appt(appointment_id):
    book_appointment, error_response, status_code = validate_schema(BookAppointmentSchema(), request.json)
    if error_response:
        return error_response, status_code

    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.client_id is not None:
        return {"message": f"This appointment has already been booked."}, 400 
    
    client = User.query.filter_by(email=book_appointment["client_email"]).first_or_404()
    
    if not check_password_hash(client.password, book_appointment["client_password"]):
        return {"message": "Unauthorized. Password incorrect."}, 403
    
    appointment.client_id = client.id
    appointment.confirmation_deadline = datetime.now() + timedelta(minutes=30)
    db.session.add(appointment)
    db.session.commit()

    return jsonify(AppointmentSchema().dump(appointment)), 200



@bp.route('/<int:appointment_id>/confirm', methods=(['PUT']))
def confirm_appt(appointment_id):

    confirm_appt, error_response, status_code = validate_schema(BookAppointmentSchema(), request.json)
    if error_response:
        return error_response, status_code
    
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.client_id is None:
        return {"message": "You must book an appointment before confirming it."}
    
    client = User.query.filter_by(email=confirm_appt["client_email"]).first_or_404()

    if(client.id != appointment.client_id):
        return {"message": "You cannot confirm an appointment you didn't book!"}, 400
    
    appointment.is_confirmed = True
    appointment.confirmation_deadline = None 

    db.session.add(appointment)
    db.session.commit()

    return jsonify(AppointmentSchema().dump(appointment)), 200
