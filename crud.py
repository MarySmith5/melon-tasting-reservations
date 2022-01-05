"""Crud operations"""

from model import db, Taster, Reservation, connect_to_db
import datetime

def create_taster(user_name):
    """Create and return a new taster/user."""
    
    taster = Taster(user_name=user_name)

    db.session.add(taster)
    db.session.commit()

    return taster


def create_reservation(taster_id, date, time):
    """Create and return a reservation"""

    reservation = Reservation(taster_id=taster_id, date=date, time=time)

    db.session.add(reservation)
    db.session.commit()

    return reservation


def view_reservations(taster_id):
    """Show all reservations for a taster"""

    return Reservation.query.filter_by(taster_id=taster_id).order_by('date').all()


def check_taken(date, time):
    """Check to see if a reservation already exists for a given date and time"""

    return Reservation.query.filter_by(date=date, time=time).first()


def check_double_reservation(taster_id, date):
    """Checks to see if a taster already has a reservation on the given date"""

    reservation = Reservation.query.filter_by(taster_id=taster_id, date=date).first()
    return reservation



if __name__ == '__main__':
    from server import app
    connect_to_db(app)

