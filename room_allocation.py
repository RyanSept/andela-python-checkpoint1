import random
import os
from models import ModelRoom, ModelPerson, Base, create_engine, connect_db, exists


class Amity(object):
    def __init__(self):
        self.rooms = {}  # key is room_name value is obj
        self.all_people = {}  # key is person_name value is obj
        self.unallocated_people = {}

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
                return "Room name is not a string."

            room_name_split = room_name.split('~')
            if len(room_name_split) != 2:
                return '''
                Invalid argument(s).\n
                Hint: Append ~l|~o to the room name. e.g Hogwarts~l
                '''

            room_name = room_name_split[0]
            room_type = room_name_split[1]
            if room_type not in ['l', 'o']:
                return '''
                Invalid argument.\n
                Hint: Append either ~l for livingspace or ~o for office.
                '''

            if self.room_exists(room_name):
                print("Room '%s' already exists." % (room_name))
                continue
            # input validation ends here

            if room_type == 'l':
                room = LivingSpace(room_name)
            else:
                room = Office(room_name)

            self.rooms[room_name] = room  # add room object to amity
            counter += 1
        return "Room(s) created successfully."

    def room_exists(self, room_name):
        if room_name in self.rooms.keys():
            return True
        else:
            return False

    def add_person(self, person_name, typ, wants_accommodation=False):
        '''
        Creates person and puts them into room randomly.
        args:
            person_name - name of person
            wants_accommodation - boolean
            typ - "fellow" or "staff"
        '''
        if person_name in self.all_people:
            return "Person already exists."
        if typ not in ['fellow', 'staff']:
            return "Invalid person type."

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

        if habitable_rooms:
            room = random.choice(habitable_rooms)
            room.people_in_room[person.name] = person
            return person
        else:
            self.unallocated_people[person_name] = person
            return "Added person but there was no room to add person to."

    def can_be_in_room(self, person, room):
        if person in room.people_in_room.values() or room.is_full():
            return False
        if type(person) is Fellow:
            if type(room) is Office:
                return True
            if type(room) is LivingSpace and person.wants_accommodation:
                return True
            return False
        elif type(person) is Staff:
            if type(room) is LivingSpace:
                return False
            return True
        return False

    def get_room_by_name(self, room_name):
        if self.room_exists(room_name):
            return self.rooms[room_name]

    def get_person_rooms(self, person_name):
        rooms = []
        for room in self.rooms.values():
            if person_name in room.people_in_room:
                rooms.append(room)
        return rooms

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

        current_rooms = self.get_person_rooms(person_name)
        person = self.all_people[person_name]
        new_room = self.rooms[room_name]

        if self.can_be_in_room(person, new_room):
            if current_rooms:
                for cur_room in current_rooms:
                    if cur_room.typ == new_room.typ:
                        print(cur_room.typ)
                        cur_room.people_in_room.pop(person_name)
                        new_room.people_in_room[person_name] = person
                        if person_name in self.unallocated_people:
                            self.unallocated_people.pop(person_name)
                        return "Moved %s from %s to %s." % (person_name, cur_room.name, new_room.name)
                    else:
                        new_room.people_in_room[person_name] = person
                        return "Moved %s to %s." % (person_name, new_room.name)

            else:  # person is in unallocated
                new_room.people_in_room[person_name] = person
                self.unallocated_people.pop(person_name)
                return "Moved person to room %s." % (new_room.name)
        else:
            reason = "Hint: They might not want accommodation or the room might be full."
            return "%s cannot be in %s. %s" % (type(person).__name__, type(new_room).__name__, reason)

    def load_people(self, filepath):
        '''
        Loads people into amity from file
        args:
            filepath - directory of file to load people from
        '''
        if not os.path.isfile(filepath):
            return "Invalid file path."

        f = open(filepath, "r")
        data = f.read().upper()
        f.close()
        if len(data) < 1:
            return "File is empty."

        data = data.split('\n')
        for person_data in data:
            person_data = person_data.split(' ')
            person_name = person_data[0] + ' ' + person_data[1]

            if 'FELLOW' in person_data:
                switch = {'Y': True, 'N': False}
                try:
                    wants_accommodation = switch[person_data[3]]
                except KeyError:
                    return "File data was written in the wrong format."

                person = self.add_person(
                    person_name, 'fellow',
                    wants_accommodation=wants_accommodation)

            elif 'STAFF' in person_data:
                person = self.add_person(person_name, 'staff')

        return "Load was successful."

    def print_allocations(self, filename=None):
        '''
        Prints out each room's name and the people in it;
        this can be piped into a file if specified in the filename parameter.
        Overwrites if piping.
        '''
        if len(self.rooms) < 1:
            return "No rooms exist."
        all_data = ''''''  # string that we add each room and it's occupants to
        separator = '-' * 37
        for room in self.rooms.values():
            people_in_room = ', '.join(room.people_in_room.keys())
            all_data += room.name + '\n' + separator +\
                '\n' + people_in_room + '\n'

        if filename is None:
            return all_data

        directory = "textfiles/"
        filepath = directory + filename + '.txt'
        if self.is_valid_filename(filename):
            f = open(filepath, "w")
            f.write(all_data)
            f.close()
            return "Wrote to " + filepath + " successfully."
        else:
            return "Invalid filename."

    def print_room(self, room_name):
        '''
        Prints names of people in specified room
        '''
        if room_name not in self.rooms:
            return "Room does not exist."
        people = self.get_room_by_name(room_name).people_in_room

        if len(people.keys()) > 0:
            return people.keys()
        return "No people in %s." % (room_name)

    def is_valid_filename(self, filename):
        for char in filename:
            if char in "\/:*?<>|":
                return False
        return True

    def print_unallocated(self, filename=None):
        '''
        Print list of people not in a room
        '''
        if len(self.unallocated_people) < 1:
            return "No unallocated people exist."

        all_data = '\n'.join(self.unallocated_people.keys())

        if filename is None:
            return all_data

        directory = "test_files/"
        filepath = directory + filename + '.txt'
        if filename and self.is_valid_filename(filename):
            f = open(filepath, "w")
            f.write(all_data)
            f.close()
            return "Wrote to " + filepath + " successfully."
        else:
            return "Invalid filename."

    def save_state(self, db='amity'):
        '''
        Persists the data of the app in database and stores it in the 
        /databases folder
        args:
            db - sqlite database to save to (name to give databases)

        '''

        all_rows = []  # both people and room rows
        for room_obj in self.rooms.values():
            row = room_obj.to_db_row()
            row.people_in_room = room_obj.people_in_room_to_rows()
            all_rows.append(row)
            all_rows += row.people_in_room

        for person_obj in self.unallocated_people.values():
            row = person_obj.to_db_row()
            all_rows.append(row)

        directory = "databases/"
        filepath = directory + db + '.db'
        if self.is_valid_filename(db):
            with open(filepath, 'wb') as f:
                pass
            db = connect_db(filepath)

            for row in all_rows:
                try:
                    db.add(row)
                    db.commit()
                except:
                    pass
            return "Data was successfuly saved to " + filepath

    def load_state(self, dbpath):
        '''
        Loads data from a database into Amity.
        args:
            dbpath - sqlite database to load from
        '''
        if not os.path.exists(dbpath):
            return "Invalid file path."

        db = connect_db(dbpath)
        rooms = db.query(ModelRoom).all()
        people = db.query(ModelPerson).all()

        for room in rooms:
            if not room.name in self.rooms:
                self.rooms[room.name] = room.to_obj()
                people_in_room = room.people_in_room_to_objs()
                self.rooms[room.name].people_in_room = people_in_room
            else:
                continue

        for person in people:
            if not person.name in self.all_people:
                self.all_people[person.name] = person.to_obj()

            if not person.room_id:
                self.unallocated_people[person.name] = person.to_obj()

        return "Load successful!"


class Room(object):
    def __init__(self, name):
        '''
        Creates room with given name
        '''
        self.name = name
        self.people_in_room = {}
        self.max_capacity = None
        self.typ = type(self).__name__

    def is_full(self):
        if len(self.people_in_room) == self.max_capacity:
            return True
        return False

    def __repr__(self):
        return "<%s (name='%s')>" % (type(self).__name__, self.name)

    def to_db_row(self):
        room_type = type(self).__name__
        map_ = {'LivingSpace': 'l', 'Office': 'o'}
        row = ModelRoom(name=self.name, room_type=map_[room_type])
        return row

    def people_in_room_to_rows(self):
        people = []
        for person in self.people_in_room.values():
            people.append(person.to_db_row())

        return people


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

    def to_db_row(self):
        person_type = type(self).__name__
        map_ = {'Fellow': 'f', 'Staff': 's'}
        row = ModelPerson(name=self.name, person_type=map_[person_type])
        return row


class Fellow(Person):
    def __init__(self, name):
        '''
        Creates person with given name
        '''
        self.name = name
        self.wants_accommodation = False


class Staff(Person):
    pass
