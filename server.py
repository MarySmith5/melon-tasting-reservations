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


@app.route('/login', methods=['POST'])
def process_login():
    """Check for valid user_name and adds it to the session"""

    user = request.form.get('username')

    if crud.valid_taster(user):
        session['taster'] = user
        flash(f"{session['taster']} you are signed in!")
        taster_id = crud. get_taster_id(user)
        return redirect('/make_reservation', taster_id=taster_id)

    else:
        flash(f"That is not a valid username.")
        return redirect('/')


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
    min = request.form.get('earliest_time')
    max = request.form.get('latest_time')

    taken = crud.check_taken(date, min, max)

    reservation = crud.check_double_reservation(taster_id, date)
    if reservation:
        flash(f"You already have an reservation that day at {reservation.time}. Only one reservation per taster each day.")
        return redirect('/make_reservation')

    else:
        return render_template('select_time.html', min=min, max=max, date=date, taster_id=taster_id, taken=taken)


@app.route('/select_reservation', methods=['POST'])
def process_time_selection():
    """Create a reservation"""

    taster = session['taster']
    date = request.form.get('date')
    time = request.form.get('time')

    taster_id = crud.get_taster_id(taster)

    crud.create_reservation(taster_id=taster_id, date=date, time=time)
    flash(f"{taster} has a reservation on {date} at {time}!")


@app.route('/view_my_reservations')
def show_reservations():
    """Show all the reservations for the user in session"""

    taster = session['taster']
    taster_id = crud.get_taster_id(taster)
    my_reservations = crud.view_reservations(taster_id)

    if my_reservations:
        return render_template('show-reservations.html')

    else:
        flash(f"There are no reservations for {taster}.")
        return redirect('/')







    











if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
