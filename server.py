"""Server for appointment reminder app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, Reservation
import crud
from jinja2 import StrictUndefined
from datetime import datetime, date, timedelta, time
import os
import pytz


app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.jinja_env.undefined = StrictUndefined

USER_SESSION = session

tz = pytz.timezone("America/Denver")

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
       
        return redirect('/make_reservation')

    else:
        flash(f"That is not a valid username.")
        return redirect('/')


@app.route('/make_reservation')
def select_reservation():
    """Renders the page to find a reservation"""

    min_date = crud.find_min_date()

    if not session.get("taster"):
        return redirect('/')

    else:
        return render_template('make_reservation.html', min_date=min_date)


@app.route('/make_reservation', methods=['POST'])
def process_reservation():
    """Checks if a reservation is valid and creates it."""
    
    taster_id = crud.get_taster_id(session['taster'])
    date_data = request.form.get('date')
    date = datetime.strptime(date_data, '%Y-%m-%d')
    
    min_hour = request.form.get('earliest_hour')
    min_minutes = request.form.get('earliest_minutes')
    min_AP =request.form.get('earliest_AP')
    min_time = f" {min_hour}:{min_minutes} {min_AP}"
    join_min= date_data + min_time
    min1 = datetime.strptime(join_min, '%Y-%m-%d %I:%M %p')
    min = tz.localize(min1)
    
    

    max_hour = request.form.get('latest_hour')
    max_minutes = request.form.get('latest_minutes')
    max_AP = request.form.get('latest_AP')
    max_time = f" {max_hour}:{max_minutes} {max_AP}"
    join_max = date_data + max_time 
    max1 = datetime.strptime(join_max, '%Y-%m-%d %I:%M %p')
    max = tz.localize(max1)
    
    print(f"*****MAX {max} ******")

    times = []
    available_times = []
    taken_times = []

    taken = crud.check_taken(date, min, max)
    if taken:
        for took in taken:
            taken_time = datetime.strftime(took.time, '%I:%M %p')
            taken_times.append(taken_time)

    for time in times:
        if time not in taken_times:
            available_times.append(time)
            

    reservation = crud.check_double_reservation(taster_id, date)
    if reservation:
        flash(f"You already have an reservation that day at {reservation.time}. Only one reservation per taster each day.")
        return redirect('/make_reservation')

    else:
        return render_template('select_time.html', min=min, max=max, date=date, available_times=available_times)


@app.route('/select_reservation', methods=['POST'])
def process_time_selection():
    """Create a reservation"""

    taster = session['taster']
    date = request.form.get('date')
    time = request.form.get('time')

    taster_id = crud.get_taster_id(taster)

    crud.create_reservation(taster_id=taster_id, date=date, time=time, date_time=date_time)
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
