import unittest
from unittest import TestCase
from room_allocation import Amity, Room, LivingSpace, Office, Person, Fellow, Staff


class Test_Room_Allocation(TestCase):
    ''' test room_allocation.py'''

    def test_livingspace_subclass_room(self):
        self.assertTrue(issubclass(LivingSpace, Room))

    def test_office_subclass_room(self):
        self.assertTrue(issubclass(Office, Room))

    def test_fellow_subclass_person(self):
        self.assertTrue(issubclass(Fellow, Person))

    def test_staff_sublcass_person(self):
        self.assertTrue(issubclass(Staff, Person))

    def test_office_max_6(self):
        office = Office('Camelot')
        self.assertTrue(office.max_capacity == 6)

    def test_livingspace_max_4(self):
        livingspace = LivingSpace('Hogwarts')
        self.assertTrue(livingspace.max_capacity == 4)

if __name__ == '__main__':
    unittest.main()
