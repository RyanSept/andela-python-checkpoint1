import random


class Amity(object):
    def __init__(self):
        self.rooms = {}  # {'room_name':<obj: Room>}
        self.all_people = {}  # {'person_name':<obj: Person>}

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

            if room_type == 'l':
                room = LivingSpace(room_name)
            else:
                room = Office(room_name)

            self.rooms[room_name] = room  # add room object to amity
            counter += 1

    def room_exists(self, room_name):
        if room_name in self.rooms:
            return True
        else:
            return False

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
            person = Fellow(person_name)
            person.wants_accomodation = wants_accomodation
        elif typ == 'staff':
            person = Staff(person_name)

        self.all_people[person_name] = person
        habitable_rooms = []  # rooms person can be in
        for room_name, room in self.rooms.iteritems():
            if self.can_be_in_room(person, room):
                habitable_rooms.append(room)

        try:
            room = random.choice(habitable_rooms)
            room.people_in_room.append(person)
            return person
        except IndexError as error:
            message = ' (No room to add %s to.)' % (type(person).__name__)
            raise type(error)(error.message + message)

    def can_be_in_room(self, person, room):
        if person in room.people_in_room:
            return False
        if type(person) is Fellow:
            if type(room) is Office:
                return True
            if type(room) is LivingSpace and person.wants_accomodation:
                return True
        elif type(person) is Staff:
            if type(room) is LivingSpace:
                return False
            return True
        return False

    def get_room_by_name(self, room_name):
        if self.room_exists(room_name):
            return self.rooms[room_name]


class Room(object):
    def __init__(self, name):
        '''
        Creates room with given name
        '''
        self.name = name
        self.people_in_room = []


class Office(Room):
    max_capacity = 6


class LivingSpace(Room):
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
