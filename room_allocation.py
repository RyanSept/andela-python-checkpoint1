import random


class Amity(object):
    rooms = []  # objects
    all_people = []  # objects

    def create_room(self, *args):
        '''
        Creates a room
        args:
            *args - arbitrary number of room names
        '''
        room_names = list(args)
        indx = 0
        for room_name in room_names:
            if self.room_exists(room_name):
                print 'The room %s already exists.' % ()
                return False

            if indx % 2 == 0:
                room = LivingSpace(room_name)
            else:
                room = Office(room_name)
            self.rooms.append(room)
            indx += 1
        print self.rooms

    def add_person(self, person_name, typ, wants_accomodation=False):
        '''
        Creates person and puts them into room randomly. #isinstance
        args:
            person_name - name of person
            wants_accomodation - boolean
            typ - "fellow" or "staff"
        '''
        if typ == 'fellow':
            person = Fellow(person_name)
            person.wants_accomodation = wants_accomodation

        elif typ == 'staff':
            person = Staff(person_name)

        else:
            print "Unknown person type"
            return False

        self.all_people.append(person)
        while True:
            room = random.choice(self.rooms)
            if self.can_be_in_room(person, room):
                break

        room.people_in_room.append(person)

    def print_allocations(self):
        '''
        Iterates through all Amity's rooms and returns the people in them
        '''

    def print_room(self, name):
        '''
        print people's names in room of given name
        returns list
        '''
        if not self.room_exists(name):
            return []

        for room in self.rooms:
            if room.name == name:
                return room.people_in_room
            else:
                print "Room is empty"
                return []

    def room_exists(self, name):
        for room in self.rooms:
            if room.name == name:
                return True
            else:
                return False

    def can_be_in_room(self, person, room):
        if person in room.people_in_room:
            return False
        if type(person) is Fellow:
            if type(room) is Office:
                return True
            if type(room) is LivingSpace and person.wants_accomodation:
                return True
        else:
            if type(room) is LivingSpace:
                return False
            return True
        return False

    def get_persons_name(self):
        

class Room(object):

    def __init__(self, name):
        '''
        Creates person with given name
        '''
        self.name = name
        self.people_in_room = []
        self.current_capacity = len(self.people_in_room)

    def remove_person(self, person, room):
        '''
        Puts person into specified room.
        args:
            person - Person object
            room - Room object
    '''
    def reallocate_person(self, person, room_to_add):
        '''
        Removes person from room and adds them to specified room
        args:
            person - Person object
            room_to_add - Room object
        '''


class LivingSpace(Room):
    max_capacity = 4


class Office(Room):
    max_capacity = 6


class Person(object):
    current_room = None

    def __init__(self, name):
        '''
        Creates person with given name
        '''
        self.name = name

    def __str__(self):
        return self.name


class Staff(Person):
    pass


class Fellow(Person):
    def __init__(self, name):
        '''
        Creates person with given name
        '''
        self.name = name
        self.wants_accomodation = False


