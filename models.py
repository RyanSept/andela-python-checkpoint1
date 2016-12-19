from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref


engine = create_engine('sqlite:///:memory:')
Base = declarative_base()


class ModelRoom(Base):

    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    room_type = Column(String(1))
    people_in_room = relationship(
        "ModelPerson", back_populates="room", uselist=True)

    def __repr__(self):
        return "<Room (name='%s')>" % (self.name)


class ModelPerson(Base):

    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    person_type = Column(String(1))
    wants_accomodation = Column(Boolean, default=False)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    room = relationship("ModelRoom", back_populates="people_in_room")

    def __repr__(self):
        return "<Person (name='%s')>" % (self.name)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

p1 = ModelPerson(name="Ryan", person_type="f")
p2 = ModelPerson(name="Mark", person_type="s")
p3 = ModelPerson(name="Paul", person_type="f", wants_accomodation=True)
p4 = ModelPerson(name="Barney", person_type="s")
room = ModelRoom(name="Hogwarts", room_type="o", people_in_room=[p1, p2, p3])
room.people_in_room.append(p4)
session.add_all([p1, p2, p3, room])
session.commit()

# print(session.query(Room).filter(room.name == 'Hogwarts').first())
#print(session.query(ModelPerson.id).all())
#print(session.query(ModelPerson).filter(ModelPerson.name == 'Pau').first())
