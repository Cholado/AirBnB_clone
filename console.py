#!/usr/bin/python3
"""
Module - console
"""

from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import cmd
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
import models
import shlex
import ast
from models import storage
classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
ints = "number_rooms, number_bathrooms, max_guest, price_by_night"
floats = "latitude, longitud"
commands = ["all", "count", "show", "destroy", "update"]


class HBNBCommand(cmd.Cmd):
    """
    class console - entry point of the command interpreter
    """
    prompt = '(hbnb)'

    def default(self, line):
        """Parses input by splitting arguments"""
        clase = line.split(".", 1)
        if len(clase) < 2:
            return
        if clase[0] not in classes:
            return
        command = clase[1].split("(", 1)
        if command[0] not in commands or len(command) < 2:
            return
        args = command[1][:-1]
        if command[0] == "show":
            return self.do_show(clase[0] + " " + args)
        if command[0] == "all":
            return self.do_all(clase[0] + " " + args)
        if command[0] == "count":
            return self.do_count(clase[0] + " " + args)
        if command[0] == "destroy":
            return self.do_destroy(clase[0] + " " + args)
        if command[0] == "update":
            if len(args) < 1:
                return
            attr_val = args.split(",", 1)
            if len(attr_val) < 2:
                return
            else:
                args = args.split(",", 2)
                return self.do_update(" ".join([clase[0]] + args))

    def do_count(self, args):
        """Retrieve the number of instances of a class"""
        args = shlex.split(args)
        if len(args) < 1:
            return
        _nb_objects = 0
        items = storage.all()
        for key in items:
            if items[key].__class__.__name__ == args[0]:
                _nb_objects += 1
        print(_nb_objects)

    def do_EOF(self, args):
        """
        public instance method
        exit console - returns 0 on program success
        """
        return True

    def emptyline(self):
        """
        public instance method
        checks if no input given, empty line + ENTER shouldn’t execute anything
        """
        pass

    def do_quit(self, args):
        """
        public instance method
        quit console - returns 0 on program success
        """
        return True

    def do_create(self, args):
        """
        public instance method
        Creates a new instance of BaseModel
        saves it (to the JSON file) and prints the id.
        """
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            instance = eval(args[0])()
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, args):
        """
        public instance method
        Prints the string representation of an instance
        based on the class name and id
        """
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]  # args 0 is name, args 1 es id
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, args):
        """
        public instance method
        Deletes an instance based on the class name and id
        Save the change into the JSON file
        """
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, args):
        """
        public instance method
        Prints all string representation
        of all instances based or not on the class name.
        """
        args = shlex.split(args)
        my_list = []
        if len(args) == 0:
            for item in models.storage.all().values():
                my_list.append(str(item))
            print("", end="")
            print(", ".join(my_list), end="")
            print("")

        elif args[0] in classes:
            for key in models.storage.all():
                if args[0] in key:
                    my_list.append(str(models.storage.all()[key]))
            print("", end="")
            print(", ".join(my_list), end="")
            print("")
        else:
            print("** class doesn't exist **")

    def do_update(self, args):
        """
        public instance method
        Updates an instance based on the class name and id
        by adding or updating attribute
        save the change into the JSON file
        """
        args = shlex.split(args)
        if len(args) == 0:
            print("** class name missing **")
            return False
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            try:
                                if isinstance(args[2], datetime) is True:
                                    pass
                                if args[0] in classes:
                                    if isinstance(args[2], ints) is True:
                                        args[3] = int(args[3])
                                    elif isinstance(args[2], floats) is True:
                                        args[3] = float(args[3])
                            except:
                                pass
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
