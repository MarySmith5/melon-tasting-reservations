"""Server for appointment reminder app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, Reservation
import crud
from jinja2 import StrictUndefined
from datetime import datetime, date, timedelta, time
import os


app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

USER_SESSION = session

@app.route('/')
def show_login():
    """Renders the signup page"""

    if not session.get("taster"):
        return render_template('login.html')

    else:
        return redirect('/make_reservation')


@app.route('/make_reservation')
def select_reservation():
    """Renders the page to find a reservation"""

    if not session.get("taster"):
        return redirect('/')

    else:
        return render_template('make_reservation.html')


@app.route('/make_reservation', methods=['POST'])
def process_reservation():
    """Checks if a reservation is valid and creates it."""

    taster_id = request.form.get('taster_id')
    date = request.form.get('date')
    time = request.form.get('time')

    reservation = crud.check_double_reservation(taster_id, date)
    if reservation:
        flash(f"You already have an reservation that day at {reservation.time}.")
        return redirect('/make_reservation')

    if crud.check_taken(date, time):
        flash(f"That reservation is taken")











if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
