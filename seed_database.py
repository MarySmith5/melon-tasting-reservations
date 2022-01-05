import os
import crud
import model
import server


os.system('dropdb reminders')
os.system('createdb reminders')

model.connect_to_db(server.app)
model.db.create_all()


crud.create_taster('MelonLover')
crud.create_taster('I8Melons')