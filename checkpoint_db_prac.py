p1 = ModelPerson(name="Ryan", person_type="f")
p2 = ModelPerson(name="Mark", person_type="s")
p3 = ModelPerson(name="Paul", person_type="f", wants_accomodation=True)
p4 = ModelPerson(name="Barney", person_type="s")
room = ModelRoom(name="Hogwarts", room_type="o", people_in_room=[p1, p2, p3])
room.people_in_room.append(p4)
session.add_all([p1, p2, p3, room])
session.commit()

print(room.people_in_room)
# print(session.query(Room).filter(room.name == 'Hogwarts').first())
#print(session.query(ModelPerson.id).all())
#print(session.query(ModelPerson).filter(ModelPerson.name == 'Pau').first())

import os

db = 'tests/test.db'
if os.path.exists(db):
    with open(db, 'wb'):
        pass
engine2 = create_engine('sqlite:///'+db)
tables = Base.metadata.tables
Base.metadata.create_all(engine2)

for table in tables:
    print ('##################################')
    print (table)
    print ( tables[table].select())
    data = engine.execute(tables[table].select()).fetchall()
    for a in data: print(a)
    if data:
        print (tables[table].insert(), data)
        engine2.execute( tables[table].insert(), data)
