import os
import crud
import model
import server
from datetime import datetime, time


os.system('dropdb reminders')
os.system('createdb reminders')

model.connect_to_db(server.app)
model.db.create_all()


crud.create_taster('MelonLover')
crud.create_taster('I8Melons')

crud.create_reservation(1, datetime(2022, 1, 10), time(hour=16, minute=30))