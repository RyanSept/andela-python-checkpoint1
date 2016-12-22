# Amity Room Allocation

Amity Room Allocation is a system that allows for allocation of fellows and
staff to rooms, either offices or livingspaces in Amity. A fellow can be in both
a livingspace and office whereas a member of staff can only be in an office. A 
livingspace has a maximum capacity of 4 whereas an office has 6.

Usage 
----------

      create_room <room_name>...
        Creates a room in Amity
       
      add_person <first_name> <second_name><person_type> [--wants_accomm=N]
        Creates person and puts them into room randomly.
      
      reallocate_person <first_name> <second_name> <room_name>
         Move person from the current room to a
         specified room
      
      load_people <filepath>
         Loads people into amity from file
      
      print_allocations [--o=filename]
         Prints out each room's name and the people
         in it; this can be piped into a file if
         specified in the filename parameter. Each file
         is saved in the directory textfiles.
  
      print_unallocated [--o=filename]
         Print list of people not in a room
      
      print_room <room_name>
         Print occupants of a room
      
      save_state [--db=sqlite_db]
        Persists the data of the app in database and
        stores it in the /databases folder.
      
      load_state <dbpath>
        Loads data from a database into Amity.
    
##Installation and Setup
1. Navigate to a directory of choice on terminal.
2. Clone this repository on that directory using `git clone https://github.com/RyanSept/andela-python-checkpoint1.git`
3. Navigate to the repo's folder on your computer terminal and do `git checkout develop`
4. Install the requirements in `requirements.txt` using `pip install -r requirements.txt`
5. Run the application with `python app.py`