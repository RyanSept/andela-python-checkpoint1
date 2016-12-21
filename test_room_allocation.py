import unittest
from unittest import TestCase
from unittest.mock import mock_open, patch
from room_allocation import Amity, Room, LivingSpace,\
    Office, Person, Fellow, Staff
import sqlite3


class Test_Room_Allocation(TestCase):
    ''' test room_allocation.py'''

    def setUp(self):
        self.amity = Amity()

    def test_sets_room_name(self):
        self.amity.create_room('Hogwarts~l')
        room = self.amity.get_room_by_name('Hogwarts')
        self.assertTrue(room.name)

    def test_sets_person_name(self):
        self.amity.create_room('Camelot~o')
        person = self.amity.add_person('John', 'fellow')
        self.assertTrue(person.name)

    def test_can_create_room(self):
        room_to_check = 'Hogwarts'
        self.amity.create_room('Hogwarts~l', 'Camelot~o',
                               'Narnia~l', 'Valhalla~o')
        amity_room_names = list(self.amity.rooms.keys())

        self.assertIn(room_to_check, amity_room_names)

    def test_cannot_create_duplicate_room(self):
        room_name = 'Hogwarts'
        self.amity.create_room(room_name + '~l')
        self.amity.create_room(room_name + '~l')

        amity_room_names = list(self.amity.rooms.keys())
        occurence_count = amity_room_names.count(room_name)

        self.assertLess(occurence_count, 2)

    def test_none_string_room_name(self):
        status = self.amity.create_room(9)
        self.assertEqual(status, "Room name is not a string.")

    def test_can_add_person_to_system(self):
        person_name = 'Ryan'
        self.amity.create_room('Hogwarts~l')
        self.amity.add_person(person_name, 'fellow', wants_accommodation=True)
        self.assertIn(person_name, self.amity.all_people)

    def test_adds_fellow_to_livingspace(self):
        person_name = 'Jude'
        self.amity.create_room('Hogwarts~l')
        person = self.amity.add_person(
            person_name, 'fellow', wants_accommodation=True)
        room = self.amity.get_room_by_name('Hogwarts')

        self.assertIn(person, room.people_in_room.values())

    def test_add_person_when_no_room_exists(self):
        '''Test add_person when no room they can stay in or no rooms at all'''
        person_name = "Dude"
        result = self.amity.add_person(person_name, 'fellow')
        self.assertEqual(result, "No room to add person to.")

    def test_wrong_add_person_type_param(self):
        person_name = 'Guy'
        self.amity.create_room('Camelot~o')
        status = self.amity.add_person(person_name, 'pikachu')

        self.assertEqual(status, "Invalid person type.")

    def test_doesnt_add_staff_to_livingspace(self):
        person_name = 'John Doe'
        self.amity.create_room('Narnia~l', 'Hogwarts~l', 'Camelot~o')
        person = self.amity.add_person(person_name, 'staff')
        room = self.amity.get_room_by_name('Narnia')

        self.assertNotIn(person, room.people_in_room)

    def test_cannot_add_more_than_6_people_to_office(self):
        people = ['Paul', 'Ryan', 'Barney',
                  'Mark', 'Angie', 'David', 'Stephen']
        self.amity.create_room('Narnia~o', 'Hogwarts~l', 'Camelot~o')
        # add 7 people
        for person in people:
            self.amity.add_person(person, 'staff')
            self.amity.reallocate_person(person, 'Camelot')

        camelot = self.amity.get_room_by_name('Camelot')
        self.assertLess(len(camelot.people_in_room), 7)

    def test_cannot_add_more_than_4_people_to_livingspace(self):
        people = ['Paul', 'Ryan', 'Barney', 'Mark', 'Angie']
        self.amity.create_room('Narnia~l', 'Hogwarts~l', 'Camelot~o')
        # add 7 people
        for person in people:
            self.amity.add_person(person, 'fellow', wants_accommodation=True)
            self.amity.reallocate_person(person, 'Hogwarts')
        hogwarts = self.amity.get_room_by_name('Hogwarts')
        self.assertLess(len(hogwarts.people_in_room), 5)

    def test_cannot_reallocate_to_wrong_room(self):
        self.amity.create_room("Camelot~o", "Hogwarts~l")
        self.amity.add_person("Lancelot", 'staff')

        status = self.amity.reallocate_person("Lancelot", 'Hogwarts')
        self.assertEqual(status, "Person cannot be in room.")

        self.amity.add_person("Arthur", 'fellow')  # doesn't want accommodation
        status2 = self.amity.reallocate_person("Arthur", 'Hogwarts')
        self.assertEqual(status2, "Person cannot be in room.")

    def test_cannot_reallocate_non_existent_person(self):
        self.amity.create_room('Hogwarts~l')
        status = self.amity.reallocate_person('Dumbledore', 'Hogwarts')
        self.assertEqual(status, "Person does not exist.")

    def test_cannot_reallocate_to_non_existent_room(self):
        self.amity.create_room("Camelot~o", "Hogwarts~l")
        self.amity.add_person("Potter", "fellow")
        status = self.amity.reallocate_person("Potter", "Non_Existent_Room")
        self.assertEqual(status, "Room does not exist.")

    def test_reallocate_removes_from_unallocated(self):
        pass

    def test_print_room_nonexistent_room_name(self):
        status = self.amity.print_room("NonExistentRoom")
        self.assertEqual(status, "Room does not exist.")

    def test_print_allocations_no_rooms_exist(self):
        status = self.amity.print_allocations()
        self.assertEqual(status, "No rooms exist.")

    def test_print_allocations_pipes_to_file(self):
        person = 'Paul'
        self.amity.create_room('Hogwarts~l')
        self.amity.add_person(person, 'fellow', wants_accommodation=True)
        self.amity.print_allocations(filename="test_amity")
        repr_in_file = 'Hogwarts' + '\n' + ('-' * 37) +\
            '\n' + 'Paul' + '\n'

        directory = "test_files/"
        f = open(directory + 'test_amity.txt', 'r')
        data = f.read()
        f.close()

        self.assertEqual(data, repr_in_file)

    def test_print_allocations_illegal_filename_chars(self):
        self.amity.create_room('Hogwarts~l')
        status = self.amity.print_allocations(filename="/<>bad|*name@")
        self.assertEqual(status, "Invalid filename.")

    def test_persists_to_specified_db(self):
        pass

    def test_loads_people(self):
        self.amity.create_room('Hogwarts~l')
        self.amity.load_people('test_files/test_load.txt')

        hogwarts = self.amity.get_room_by_name('Hogwarts').people_in_room

        self.assertIn('FOHN DOE', hogwarts)

    def test_load_people_empty_file(self):
        status = self.amity.load_people('test_files/empty_file.txt')
        self.assertEqual(status, "File is empty.")

    def test_load_people_wrong_format(self):
        filepath = 'test_files/wrong_format.txt'
        with open(filepath,'w') as f:
            f.write('Y JOHN DOE FELLOW')

        status = self.amity.load_people(filepath)
        self.assertEqual(status, "File data was written in the wrong format.")

    def test_load_people_invalid_filedir(self):
        status = self.amity.load_people('nonexistentdir/randomfilename.txt')
        self.assertEqual(status, "Invalid file path.")

    def test_saves_state(self):
        person = 'Jude Law'
        self.amity.create_room('Hogwarts~l')
        self.amity.add_person(person, 'fellow', wants_accommodation=True)

        self.amity.save_state(db='test')

        conn = sqlite3.connect('databases/test.db')
        database = conn.cursor()
        result = database.execute("SELECT * FROM rooms WHERE name='Hogwarts'")
        result = result.fetchall()[0][1]  # name

        self.assertEqual(result, 'Hogwarts')

    def test_loads_state(self):
        self.amity.load_state('databases/test_load.db')
        hogwarts = self.amity.get_room_by_name('Camelot').people_in_room
        self.assertIn('John Doe', hogwarts)


if __name__ == '__main__':
    unittest.main()
