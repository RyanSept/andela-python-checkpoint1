import random
from models import Person, Room, session


class Amity(object):
    def __init__(self):
        self.db = session

    def create_room(self, *args):
        ''' Creates a room in Amity
            args:
                *args - arbitrary number of room_names

            each room name should be supplied with a switch indicating if it is
            an office or livingspace. This is done by appending a tilde and the
            letter 'o' for office, and 'l' for livingspace

            eg.
            create_room('Hogwarts~l','Mordor~o')
        '''

        room_names = args

        counter = 0
        for room_name in room_names:
            # validation of input
            if type(room_name) is not str:
                raise TypeError

            room_name_split = room_name.split('~')
            if len(room_name_split) != 2:
                raise ValueError

            room_name = room_name_split[0]
            room_type = room_name_split[1]
            if room_type not in ['l', 'o']:
                raise TypeError

            if self.room_exists(room_name):
                # print "Room '%s' already exists." % (room_name)
                continue
            # input validation ends here

            room = Room(name=room_name, room_type=room_type)
            self.add_to_db(room)

            counter += 1

    def room_exists(self, room_name):
        exists = self.db.query(Room).filter(Room.name == room_name).all()
        return bool(exists)

    def add_person(self, person_name, typ, wants_accomodation=False):
        '''
        Creates person and puts them into room randomly. #isinstance
        args:
            person_name - name of person
            wants_accomodation - boolean
            typ - "fellow" or "staff"
        '''
        if typ not in ['fellow', 'staff']:
            raise TypeError

        if typ == 'fellow':
            person = Person(name=person_name, person_type='f',
                            wants_accomodation=wants_accomodation)
        elif typ == 'staff':
            person = Person(name=person_name, person_type='s',
                            wants_accomodation=wants_accomodation)

        self.add_to_db(person)
        habitable_rooms = []
        rooms = self.db.query(Room).all()
        for room in rooms:
            if self.can_be_in_room(person, room):
                habitable_rooms.append(room)

        try:
            room = random.choice(habitable_rooms)
            room.people_in_room.append(person)
            return person
        except IndexError as error:
            message = ' (No room to add %s to.)' % (type(person).__name__)
            raise type(error)  # (error.message + message)

    def can_be_in_room(self, person, room):
        if person in room.people_in_room:
            return False
        if person.person_type == 'f':
            if room.room_type == 'o':
                return True
            if room == 'l' and person.wants_accomodation:
                return True
        elif person.person_type == 's':
            if room.room_type == 'l':
                return False
            return True
        return False

    def get_room_by_name(self, room_name):
        if self.room_exists(room_name):
            room = self.db.query(Room).filter(Room.name == room_name).first()
            return room

    def get_person_by_name(self, person_name):
        person = self.db.query(Person).filter(
            Person.name == person_name).first()
        return person

    def add_to_db(self, *args):
        self.db.add_all(args)
        self.db.commit()


class Office(object):
    max_capacity = 6


class LivingSpace(object):
    max_capacity = 4


class Person(object):
    def __init__(self, name):
        '''
        Creates person with given name
        '''
        self.name = name


class Fellow(Person):
    def __init__(self, name):
        '''
        Creates person with given name
        '''
        self.name = name
        self.wants_accomodation = False


class Staff(Person):
    pass
