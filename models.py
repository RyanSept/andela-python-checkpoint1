from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.serializer import loads, dumps


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

    def to_obj(self):
        from room_allocation import LivingSpace, Office, Fellow, Staff
        if self.room_type == 'l':
            room = LivingSpace(self.name)
        elif self.room_type == 'o':
            room = Office(self.name)

        return room

    def people_in_room_to_objs(self):
        people = {}
        for person in self.people_in_room:
            people[person.name] = person.to_obj()

        return people


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

    def to_obj(self):
        from room_allocation import LivingSpace, Office, Fellow, Staff
        if self.person_type == 'f':
            person = Fellow(self.name)
            person.wants_accommodation = self.wants_accomodation
        elif self.person_type == 's':
            person = Staff(self.name)

        return person


def connect_db(db=':memory:'):
    engine = create_engine('sqlite:///' + db)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session
