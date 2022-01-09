import os
import crud
import model
import server
from datetime import datetime, time


os.system('dropdb reservations')
os.system('createdb reservations')

model.connect_to_db(server.app)
model.db.create_all()


crud.create_taster('MelonLover')
crud.create_taster('I8Melons')

crud.create_reservation(1, datetime(2022, 1, 8), time(hour=8, minute=30), datetime(2022, 1, 11, hour=6, minute=00, second=00, microsecond=0, tzinfo=None))

