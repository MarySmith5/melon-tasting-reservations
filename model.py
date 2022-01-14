"""Models for tastin appointment app"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
import arrow

db = SQLAlchemy()

class Taster(db.Model):
    """An account holder"""

    __tablename__ = 'tasters'

    taster_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50))

    my_reservations = db.relationship('Reservation', back_populates='my_taster')

    def __repr__(self):
        """Show info about a taster"""
        return f"{self.user_name}"


class Reservation(db.Model):
    """A reservation for a tasting"""

    __tablename__ = 'reservations'

    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    taster_id = db.Column(db.Integer, db.ForeignKey('tasters.taster_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    
    my_taster = db.relationship('Taster', back_populates='my_reservations')

    def readable_time(self):
        t = datetime.strftime(self.date_time, '%I:%M %p')
        return t


    def __repr__(self):
        """Show info about a reservation"""
        return f"Tasting on {self.date} at {self.readable_time()}"

    

def connect_to_db(flask_app, db_uri, echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    
    connect_to_db(app, echo=False)













