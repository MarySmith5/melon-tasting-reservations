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

db_uri = os.environ["DATABASE_URL"].replace("postgres", "postgresql")
connect_to_db(app, db_uri)

USER_SESSION = session

TIMES = [" 12:00 AM", " 12:30 AM", " 1:00 AM", " 1:30 AM", " 2:00 AM", " 2:30 AM", 
        " 3:00 AM", " 3:30 AM", " 4:00 AM", " 4:30 AM", " 5:00 AM", " 5:30 AM", " 6:00 AM", 
        " 6:30 AM", " 7:00 AM", " 7:30 AM"," 8:00 AM", " 8:30 AM", " 9:00 AM", " 9:30 AM", 
        " 10:00 AM", " 10:30 AM", " 11:00 AM", " 11:30 AM", " 12:00 PM", " 12:30 PM", " 1:00 PM", 
        " 1:30 PM", " 2:00 PM", " 2:30 PM", " 3:00 PM", " 3:30 PM", " 4:00 PM", " 4:30 PM", 
        " 5:00 PM", " 5:30 PM", " 6:00 PM", " 6:30 PM", " 7:00 PM", " 7:30 PM", " 8:00 PM", 
        " 8:30 PM", " 9:00 PM", " 9:30 PM", " 10:00 PM", " 10:30 PM", " 11:00 PM", " 11:30 PM"]

tz = pytz.timezone("UTC")

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
    

    time_range = crud.find_time_range(TIMES, min_time, max_time)

    if time_range == "invalid":
        flash(f"Latest time must be later than earliest time")
        return redirect('/make_reservation')

    available_times = []
    taken_times = []

    taken = crud.check_taken(min, max)

    if taken:
        
        for took in taken:
            fix_tz = tz.localize(took.date_time)
            taken_t = datetime.strftime(fix_tz, '%-I:%M %p')
            taken_time = f" {taken_t}"
            taken_times.append(taken_time)
    print(f"*****processed times {taken_times} ******")
    for time in TIMES:
        if time not in taken_times and time in time_range:
            available_times.append(time)
            

    reservation = crud.check_double_reservation(taster_id, date)
    if reservation:
        f_tz = tz.localize(reservation.date_time)
        t = datetime.strftime(reservation.date_time, "%I:%M %p")
        flash(f"You already have an reservation on {date_data} at {t}. Only one reservation per taster each day.")
        return redirect('/make_reservation')

    else:
        return render_template('select_time.html', date=date_data, available_times=available_times)


@app.route('/select_reservation', methods=['POST'])
def process_time_selection():
    """Create a reservation"""

    taster = session['taster']
    date = request.form.get('date')
    time = request.form.get('res_time')
    
    join_date = f"{date} {time}"
   
    res_date = datetime.strptime(join_date, '%Y-%m-%d %I:%M %p')
    date_time = tz.localize(res_date)

    taster_id = crud.get_taster_id(taster)

    crud.create_reservation(taster_id=taster_id, date=date, time=time, date_time=date_time)
    flash(f"{taster} has a reservation on {date} at {time}!")

    return redirect('/')


@app.route('/view_my_reservations')
def show_reservations():
    """Show all the reservations for the user in session"""

    taster = session['taster']
    taster_id = crud.get_taster_id(taster)
    my_reservations = crud.view_reservations(taster_id)

    if my_reservations:
        return render_template('show-reservations.html', taster=taster, my_reservations=my_reservations)

    else:
        flash(f"There are no reservations for {taster}.")
        return redirect('/')






if __name__ == "__main__":
    
    
    app.run()