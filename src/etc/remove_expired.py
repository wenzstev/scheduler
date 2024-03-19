from datetime import datetime
from flask_apscheduler import APScheduler

from src.data.models import Appointment
from . import db

def check_unconfirmed_appointments(app):
    with app.app_context():
        now = datetime.now()
        unconfirmed_appts = Appointment.query.filter(Appointment.is_confirmed==False, Appointment.confirmation_deadline < now).all()
        for appointment in unconfirmed_appts:
            appointment.client_id = None
            appointment.confirmation_deadline = None 
        db.session.add_all(unconfirmed_appts)
        db.session.commit()


def init_scheduler(app):
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    func = lambda : check_unconfirmed_appointments(app) # lambda to capture the app context
    scheduler.add_job(id="Clear unconfirmed appointments", func=func, trigger='interval', minutes=5)


