import unittest
from unittest import TestCase
from room_allocation import Amity, Room, LivingSpace, Office, Person, Fellow, Staff


class Room_Allocation_Test(TestCase):
    ''' tests for room_allocation.py '''

    def test_subclass(self):
        self.assertTrue(issubclass(LivingSpace, Room))

    def test_can_allocate_person_room(self):
        amity = Amity()
        amity.create_room('Hogwarts', 'Camelot', 'Narnia', 'Valhalla')
        amity.add_person('Ryan', 'fellow')

        for room in amity.rooms:
            people_in_room = amity.print_room(room.name)
            print room.name, people_in_room
            if people_in_room:
                for person in people_in_room:
                    self.assertTrue(person.name == 'Ryan')
            else:
                self.assertTrue(bool(people_in_room) == True)

    def test_office_max_6(self):
        office = Office('Camelot')
        self.assertTrue(office.max_capacity == 6)

    def test_livingspace_max_4(self):
        livingspace = LivingSpace('Hogwarts')
        self.assertTrue(livingspace.max_capacity == 4)

    def test_cannot_allocate_staff_living_space(self):
        pass

    def test_cannot_add_person_twice(self):
        pass

    def test_default_wants_accomodation(self):
        pass

    def test_room_name_is_only_str(self):
        pass

    def test_unknown_type_add_person(self):  # if not fellow or staff
        pass

    def test_adding_person_when_no_rooms_exist(self):
        pass

if __name__ == '__main__':
    unittest.main()
