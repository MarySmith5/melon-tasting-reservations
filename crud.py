"""Crud operations"""

from model import db, Taster, Reservation, connect_to_db
import datetime

def create_taster(user_name):
    """Create and return a new taster/user."""
    
    taster = Taster(user_name=user_name)

    db.session.add(taster)
    db.session.commit()

    return taster


def valid_taster(user_name):
    """check to see if user_name has an account"""

    return Taster.query.filter_by(user_name=user_name).first()


def get_taster_id(user_name):

    taster = Taster.query.filter_by(user_name=user_name).one()
    return taster.taster_id


def create_reservation(taster_id, date, time, date_time):
    """Create and return a reservation"""

    reservation = Reservation(taster_id=taster_id, date=date, time=time, date_time=date_time)

    db.session.add(reservation)
    db.session.commit()

    return reservation


def view_reservations(taster_id):
    """Show all reservations for a taster"""

    return Reservation.query.filter_by(taster_id=taster_id).order_by('date').all()
    


def check_taken(min, max):
    """Check to see if a reservation already exists for a given date and time"""

    taken = Reservation.query.filter(Reservation.fix_timezone()>=min, Reservation.fix_timezone()<=max).all()
    return taken


def check_double_reservation(taster_id, date):
    """Checks to see if a taster already has a reservation on the given date"""

    reservation = Reservation.query.filter_by(taster_id=taster_id, date=date).first()
    return reservation


def find_min_date():
    """Checks current date"""
    min_date = datetime.date.today()
    return min_date


def find_time_range(times, min, max):
    
    
    for i, time in enumerate(times): 
        if time == min:
            a = i
        if time == max:
            z = i 
    if a > z:
        return "invalid"

    elif max == "11:30 PM":
        time_range = times[a:]
    else:
        time_range = times[a:z+1]

        return time_range


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

