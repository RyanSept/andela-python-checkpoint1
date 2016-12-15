import unittest
from unittest import TestCase
from room_allocation import Amity, Room, LivingSpace, Office, Person, Fellow, Staff


class Test_Room_Allocation(TestCase):
    ''' test room_allocation.py'''

    def setUp(self):
        self.amity = Amity()

    def test_office_max_6(self):
        office = Office('Camelot~o')
        self.assertTrue(office.max_capacity == 6)

    def test_livingspace_max_4(self):
        livingspace = LivingSpace('Hogwarts~l')
        self.assertTrue(livingspace.max_capacity == 4)

    def test_can_create_room(self):
        self.amity.create_room('Hogwarts~l')
        room = self.amity.get_room_by_name('Hogwarts')
        self.assertTrue(room.name)

    def test_sets_person_name(self):
        self.amity.create_room('Camelot~o')
        person = self.amity.add_person('John', 'fellow')
        self.assertTrue(person.name)

    def test_cannot_create_duplicate_room(self):
        room_name = 'Hogwarts'
        self.amity.create_room(room_name + '~l')
        self.amity.create_room(room_name + '~l')

        amity_rooms = self.amity.db.query(Room)
        occurence_count = len(amity_rooms.filter(Room.name == room_name).all())

        self.assertLess(occurence_count, 2)

    def test_none_string_room_name(self):
        with self.assertRaises(TypeError):
            self.amity.create_room(9)

    def test_can_add_person_to_system(self):
        person_name = 'Ryan'
        self.amity.create_room('Hogwarts~l')
        self.amity.add_person(person_name, 'fellow', wants_accomodation=True)
        person = self.amity.get_person_by_name(person_name)
        self.assertTrue(person)

    def test_adds_fellow_to_livingspace(self):
        person_name = 'Jude'
        self.amity.create_room('Hogwarts~l')
        person = self.amity.add_person(
            person_name, 'fellow', wants_accomodation=True)
        room = self.amity.get_room_by_name('Hogwarts')

        self.assertIn(person, room.people_in_room)

    def test_add_person_when_no_room_exists(self):
        '''Test add_person when no room they can stay in or no rooms at all'''
        person_name = "Dude"
        with self.assertRaises(IndexError):
            person = self.amity.add_person(person_name, 'fellow')

    def test_wrong_add_person_type_param(self):
        person_name = 'Guy'
        self.amity.create_room('Camelot~o')
        with self.assertRaises(TypeError):
            self.amity.add_person(person_name, 'pikachu')

    def test_doesnt_add_staff_to_livingspace(self):
        person_name = 'John Doe'
        self.amity.create_room('Narnia~l', 'Hogwarts~l', 'Camelot~o')
        person = self.amity.add_person(person_name, 'staff')
        room = self.amity.get_room_by_name('Narnia')

        self.assertNotIn(person, room.people_in_room)

    def test_cannot_add_more_than_6_to_office(self):
        pass

    def test_cannot_add_more_than_4_to_livingspace(self):
        pass

if __name__ == '__main__':
    unittest.main()
