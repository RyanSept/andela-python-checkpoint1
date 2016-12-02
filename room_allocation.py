import random


class Amity(object):
    pass


class Room(object):
    def __init__(self, name):
        '''
        Creates person with given name
        '''
        self.name = name
        self.people_in_room = []
        self.current_capacity = len(self.people_in_room)


class Office(Room):
    pass

class LivingSpace(Room):
    pass


class Person(object):
    pass


class Fellow(Person):
    pass


class Staff(Person):
    pass
