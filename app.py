"""
    Commands:
        create_room <room_name>...
        add_person <first_name> <second_name> <fellow|staff> [--wants_accomm=N]
        reallocate_person <first_name> <second_name> <room_name>
        load_people <filedir>
        print_allocations [--o=filename]
        print_unallocated [--o=filename]
        print_room <room_name>
        save_state [--db=sqlite_db]
        load_state <dbpath>
        quit
    Options:
        -h, --help  Show this screen and exit
        --o filename  Specify filename
        --db    Name of SQLite DB
        --accomm  If person needs accommodation [default='N']
"""

from docopt import docopt, DocoptExit
import cmd
import os
from room_allocation import Amity
from termcolor import cprint, colored
from pyfiglet import figlet_format


def docopt_cmd(func):
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def intro():
    pass


class App(cmd.Cmd):
    prompt = '<Amity>: '
    amity = Amity()

    @docopt_cmd
    def do_create_room(self, arg):
        '''
        Usage: create_room <room_name>...

        each room name should be supplied with a switch indicating if it is
        an office or livingspace. This is done by appending a tilde and the
        letter 'o' for office, and 'l' for livingspace

        e.g create_room Hogwarts~l Mordor~o
        '''

        room_names = arg['<room_name>']

        status = self.amity.create_room(*room_names)
        print(status)

    @docopt_cmd
    def do_add_person(self, arg):
        '''
        Usage: add_person <first_name> <second_name> <person_type> [--wants_accomm=N]

        Creates person and puts them into room randomly. 
            person_type - fellow|staff
        '''

        person_name = arg['<first_name>'] + ' ' + arg['<second_name>']
        person_type = arg['<person_type>']
        map_ = {'Y': True, 'N': False}
        try:
            if arg['--wants_accomm'] is None:
                arg['--wants_accomm'] = 'N'
            wants_accommodation = map_[arg['--wants_accomm'].upper()]
        except KeyError:
            print("Invalid option: " + arg['--wants_accomm'])
            return

        status = self.amity.add_person(person_name, person_type,
                                       wants_accommodation=wants_accommodation)

        if type(status) != str:
            print('Person added successfully!')

        else:
            print(status)

    @docopt_cmd
    def do_reallocate_person(self, arg):
        '''
        Usage: reallocate_person <first_name> <second_name> <room_name>

        Move person from the current room to a specified room
        '''

        room_name = arg['<room_name>']
        person_name = arg['<first_name>'] + ' ' + arg['<second_name>']

        status = self.amity.reallocate_person(person_name, room_name)
        print(status)

    @docopt_cmd
    def do_load_people(self, arg):
        '''
        Usage: load_people <filepath>

        Loads people into amity from file
        '''
        filepath = arg["<filepath>"]
        status = self.amity.load_people(filepath)
        print(status)

    @docopt_cmd
    def do_print_allocations(self, arg):
        '''
        Usage: print_allocations [--o=filename]

        Prints out each room's name and the people in it;
        this can be piped into a file if specified in the filename parameter.
        Each file is saved in the directory ___
        '''
        filename = arg['--o']

        if filename != None:
            status = self.amity.print_allocations(filename=filename)
        else:
            status = self.amity.print_allocations()
        print(status)

    @docopt_cmd
    def do_print_unallocated(self, arg):
        '''
        Usage: print_unallocated [--o=filename]

        Print list of people not in a room
        '''
        filename = arg['--o']

        if filename != None:
            status = self.amity.print_unallocated(filename=filename)
        else:
            status = self.amity.print_unallocated()

        print(status)

    @docopt_cmd
    def do_print_room(self, arg):
        '''
        Usage: print_room <room_name>

        Print occupants of a room
        '''

        room_name = arg['<room_name>']
        status = self.amity.print_room(room_name)
        if not type(status) is str:
            for name in status:
                print(name)
            return
        print(status)

    @docopt_cmd
    def do_save_state(self, arg):
        '''
        Usage: save_state [--db=sqlite_db]

        Persists the data of the app in database and stores it in the
        /databases folder
        '''
        db = arg['--db']

        if db is not None:
            status = self.amity.save_state(db=db)
        else:
            status = self.amity.save_state()

        print(status)

    @docopt_cmd
    def do_load_state(self, arg):
        '''
        Usage: load_state <dbpath>

        Loads data from a database into Amity.
        '''

        dbpath = arg['<dbpath>']
        status = self.amity.load_state(dbpath)
        print(status)


if __name__ == "__main__":
    App().cmdloop()
