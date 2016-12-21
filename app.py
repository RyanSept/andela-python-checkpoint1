"""
    Commands:
        amity create_room <room_name>...
        amity add_person <first_name> <second_name> <fellow|staff> [--wants_accomm=N]
        amity reallocate_person <first_name> <second_name> <room_name>
        amity load_people <filedir>
        amity print_allocations [--o=filename]
        amity print_unallocated [--o=filename]
        amity print_room <room_name>
        amity save_state [--db=sqlite_db]
        amity load_state <sqlite_db>
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
        '''

        room_name = arg['<room_name>']
        person_name = arg['<first_name>'] + ' ' + arg['<second_name>']

        status = self.amity.reallocate_person(person_name, room_name)
        print(status)

    @docopt_cmd
    def do_load_people(self, arg):
        '''
        Usage: load_people <filedir>
            filedir - directory of file to load people from
        '''
        filedir = arg["<filedir>"]
        print(filedir)
        status = self.amity.load_people(filedir)
        print(status)

if __name__ == "__main__":
    App().cmdloop()
