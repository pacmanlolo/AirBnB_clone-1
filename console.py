#!/usr/bin/python3
"""Defines the HBnB console."""

import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for HBnB.

    Attributes:
        prompt (str): The command prompt.
        classes (set): The set of available class names.
    """

    prompt = "(hbnb) "
    classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formatting - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parentheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')

            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """Method to exit the HBNB console"""
        return True

    def help_quit(self):
        """Prints the help documentation for the quit command"""
        print("Exits the HBNB console")
        print("Usage: quit")

    def do_EOF(self, line):
        """Method to handle the EOF signal"""
        return True

    def emptyline(self):
        """Empty line doesn't execute previous command"""
        pass

    def do_create(self, arg):
        """Create a new instance of BaseModel"""
        if not arg:
            print("** class name missing **")
            return
        try:
            new_inst = eval(arg)()
            new_inst.save()
            print(new_inst.id)
        except Exception:
            print("** class doesn't exist **")

    def help_create(self):
        """Prints the help documentation for the create command"""
        print("Creates a new instance of a specified class")
        print("Usage: create <class_name>")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key in storage.all():
                print(storage.all()[key])
            else:
                print("** no instance found **")

    def help_show(self):
        """Prints the help documentation for the show command"""
        print("Prints the string representation of an instance")
        print("Usage: show <class_name> <id>")

    def do_destroy(self, arg):
        """Deletes an instance"""
        if not arg:
            print("** class name missing **")
            return
        args = arg.split()
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key in storage.all():
                storage.all().pop(key)
                storage.save()
            else:
                print("** no instance found **")

    def help_destroy(self):
        """Prints the help documentation for the destroy command"""
        print("Deletes an instance")
        print("Usage: destroy <class_name> <id>")

    def do_all(self, arg):
        """Prints all string representations of all instances"""
        args = arg.split()
        obj_list = []
        if len(args) == 0:
            obj_list = list(storage.all().values())
        elif args[0] in HBNBCommand.classes:
            obj_list = [obj for obj in storage.all().values() if obj.__class__.__name__ == args[0]]
        else:
            print("** class doesn't exist **")
            return
        print("[", end="")
        print(', '.join(str(obj) for obj in obj_list), end="")
        print("]")

    def help_all(self):
        """Prints the help documentation for the all command"""
        print("Prints the string representations of all instances")
        print("Usage: all [class_name]")

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        instance = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3]
        if attr_name in HBNBCommand.types:
            attr_value = HBNBCommand.types[attr_name](attr_value)
        setattr(instance, attr_name, attr_value)
        instance.save()

    def help_update(self):
        """Prints the help documentation for the update command"""
        print("Updates an instance based on the class name and id")
        print("Usage: update <class_name> <id> <attribute_name> <attribute_value>")

    def do_count(self, arg):
        """Counts the number of instances of a class"""
        if arg not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            count = 0
            for obj in storage.all().values():
                if obj.__class__.__name__ == arg:
                    count += 1
            print(count)

    def help_count(self):
        """Prints the help documentation for the count command"""
        print("Counts the number of instances of a class")
        print("Usage: count <class_name>")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
