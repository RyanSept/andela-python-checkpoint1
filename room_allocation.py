import random
#from models import ModelRoom, ModelPerson, session


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

    def add_person(self, person_name, typ, wants_accommodation=False):
        '''
        Creates person and puts them into room randomly. #isinstance
        args:
            person_name - name of person
            wants_accommodation - boolean
            typ - "fellow" or "staff"
        '''
        if typ not in ['fellow', 'staff']:
            raise TypeError

        if typ == 'fellow':
            person = Fellow(person_name)
            person.wants_accommodation = wants_accommodation
        elif typ == 'staff':
            person = Staff(person_name)

        self.all_people[person_name] = person
        habitable_rooms = []  # rooms person can be in
        for room_name, room in self.rooms.items():
            if self.can_be_in_room(person, room):
                habitable_rooms.append(room)

        try:
            room = random.choice(habitable_rooms)
            room.people_in_room[person.name] = person
            return person
        except IndexError as error:
            message = ' (No room to add %s to.)' % (type(person).__name__)
            raise type(error)  # (error.message + message)

    def can_be_in_room(self, person, room):
        if person in room.people_in_room.values() or room.is_full():
            return False
        if type(person) is Fellow:
            if type(room) is Office:
                return True
            if type(room) is LivingSpace and person.wants_accommodation:
                return True
            else:
                return False
        elif type(person) is Staff:
            if type(room) is LivingSpace:
                return False
            return True
        return False

    def get_room_by_name(self, room_name):
        if self.room_exists(room_name):
            return self.rooms[room_name]

    def get_person_room(self, person_name):
        for room in self.rooms.values():
            if person_name in room.people_in_room:
                return room

    def reallocate_person(self, person_name, room_name):
        '''
        Move person from the current room to a specified room
        args:
            person_name - name of person to be moved
            room_name - name of room to move person to
        '''
        if person_name not in self.all_people:
            return "Person does not exist."
        if room_name not in self.rooms:
            return "Room does not exist."

        current_room = self.get_person_room(person_name)
        person = current_room.people_in_room[person_name]
        new_room = self.rooms[room_name]

        if self.can_be_in_room(person, new_room):
            current_room.people_in_room.pop(person_name)
            new_room.people_in_room[person_name] = person
        else:
            return "Person cannot be in room."

    def print_allocations(self, filename=None):
        '''
        Prints out each room's name and the people in it;
        this can be piped into a file if specified in the filename parameter.
        Overwrites if piping.
        '''
        if len(self.rooms)<1:
            return "No rooms exist."
        all_data = ''''''
        separator = '-' * 37
        for room in self.rooms.values():
            people_in_room = ', '.join(room.people_in_room.keys())
            all_data += room.name + '\n' + separator +\
                '\n' + people_in_room + '\n'

        print(all_data)
        directory = "allocations/"
        if filename:
            f = open(directory + filename + '.txt', "w")
            f.write(all_data)
            f.close()

    def print_room(self, room_name):
        '''
        Prints names of people in specified room
        '''
        if room_name not in self.rooms:
            return "Room does not exist."
        people = self.get_room_by_name(room_name).people_in_room

        for name in people.keys():
            print(name)

    def is_valid_pathname(self, filename):
        for char in filename: 
            if char not in "\/:*?<>|":
                return True
            return False


class Room(object):
    def __init__(self, name):
        '''
        Creates room with given name
        '''
        self.name = name
        self.people_in_room = {}
        self.max_capacity = None

    def is_full(self):
        if len(self.people_in_room) >= self.max_capacity:
            return True
        return False

    def __repr__(self):
        return "<Room (name='%s')>" % (self.name)


class Office(Room):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_capacity = 6


class LivingSpace(Room):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_capacity = 4


class Person(object):
    def __init__(self, name):
        '''
        Creates person with given name
        '''
        self.name = name

    def __repr__(self):
        return "<Person (name='%s')>" % (self.name)


class Fellow(Person):
    def __init__(self, name):
        '''
        Creates person with given name
        '''
        self.name = name
        self.wants_accommodation = False


class Staff(Person):
    pass
