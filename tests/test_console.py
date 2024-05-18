#!/usr/bin/env python3
"""Module for performing TwestHBNBCommanf class."""

from console import HBNBCommand
from models.engine.file_storage import FileStorage
import unittest
import sys
from unittest.mock import patch
import datetime
from io import StringIO
import os
import re


class TestHBNBCommand(unittest.TestCase):

    """Tests HBNBCommand console."""

    attribute_val = {
        str: "foobar108",
        int: 1008,
        float: 1.08
    }

    reset_val = {
        str: "",
        int: 0,
        float: 0.0
    }

    test_rand_attr = {
        "strfoo": "barfoo",
        "intfoo": 248,
        "floatfoo": 9.8
    }

    def setUp(self):
        """Sets up test cases."""
        if os.path.isfile("file.json"):
            os.remove("file.json")
        self.resetStorage()

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_help(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        d = """
Documentetion of commands (help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(d, x.getvalue())

    def testhelp_EOF(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("help EOF")
        d = 'Handles End Of File character.\n        \n'
        self.assertEqual(d, x.getvalue())

    def testhelp_quit(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("help quit")
        d = 'Exits the program.\n        \n'
        self.assertEqual(d, x.getvalue())

    def testhelp_create(self):
        """Tests out the help command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("help create")
        d = 'Creates an instance.\n        \n'
        self.assertEqual(d, x.getvalue())

    def testhelp_show(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("help show")
        d = 'Prints the string representation of an instance.\n        \n'
        self.assertEqual(d, x.getvalue())

    def testhelp_destroy(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("help destroy")
        d = 'Deletes an instance based on the class name and id.\n        \n'
        self.assertEqual(d, x.getvalue())

    def testhelp_all(self):
        """Tests out the help command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("help all")
        d = 'Prints all string representation of all instances.\n        \n'
        self.assertEqual(d, x.getvalue())

    def testhelp_count(self):
        """Tests out the help command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("help count")
        d = 'Counts the instances of a class.\n        \n'
        self.assertEqual(d, x.getvalue())

    def testhelp_update(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("help update")
        d = 'Updates an instance by adding or updating attribute.\n        \n'
        self.assertEqual(d, x.getvalue())

    def testdo_quit(self):
        """Tests the quit commmand."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("quit")
        mesg = x.getvalue()
        self.assertTrue(len(mesg) == 0)
        self.assertEqual("", mesg)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("quit garbage")
        mesg = x.getvalue()
        self.assertTrue(len(mesg) == 0)
        self.assertEqual("", mesg)

    def testdo_EOF(self):
        """Tests EOF commmand."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("EOF")
        mesg = x.getvalue()
        self.assertTrue(len(mesg) == 1)
        self.assertEqual("\n", mesg)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("EOF garbage")
        mesg = x.getvalue()
        self.assertTrue(len(mesg) == 1)
        self.assertEqual("\n", mesg)

    def testemptyline(self):
        """Tests emptyline functionality."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("\n")
        d = ""
        self.assertEqual(d, x.getvalue())
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("                  \n")
        d = ""
        self.assertEqual(d, x.getvalue())

    def testdo_create(self):
        """Tests create for all classes."""
        for clas in self.classes():
            self.helptest_do_create(clas)

    def helptest_do_create(self, clas):
        """Helper method to test the create commmand."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("create {}".format(clas))
        u_id = x.getvalue()[:-1]
        self.assertTrue(len(u_id) > 0)
        key = "{}.{}".format(classname, u_id)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("all {}".format(clas))
        self.assertTrue(u_id in x.getvalue())

    def testdo_create_error(self):
        """Tests create command with errors."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("create")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("create garbage")
        msg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class doesn't exist **")

    def testdo_show(self):
        """Tests show for all classes."""
        for classname in self.classes():
            self.helptest_do_show(classname)
            self.helptest_show_advanced(classname)

    def helptest_do_show(self, classname):
        """Helps test the show command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("create {}".format(classname))
        u_id = x.getvalue()[:-1]
        self.assertTrue(len(u_id) > 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("show {} {}".format(classname, u_id))
        d = x.getvalue()[:-1]
        self.assertTrue(u_id in d)

    def testdo_show_error(self):
        """Tests show command with errors."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("show")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("show garbage")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("show BaseModel")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("show BaseModel 6524359")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** no instance found **")

    def helptest_show_advanced(self, classname):
        """Helps test .show() command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("create {}".format(classname))
        u_id = x.getvalue()[:-1]
        self.assertTrue(len(u_id) > 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, u_id))
        d = x.getvalue()
        self.assertTrue(u_id in d)

    def testdo_show_error_advanced(self):
        """Tests show() command with errors."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(".show()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("garbage.show()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("BaseModel.show()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('BaseModel.show("6524359")')
        mesg = x.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def testdo_destroy(self):
        """Tests destroy for all classes."""
        for classname in self.classes():
            self.helptest_do_destroy(classname)
            self.helptest_destroy_advanced(classname)

    def helptest_do_destroy(self, classname):
        """Helps test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("create {}".format(classname))
        u_id = x.getvalue()[:-1]
        self.assertTrue(len(u_id) > 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("destroy {} {}".format(classname, u_id))
        d = x.getvalue()[:-1]
        self.assertTrue(len(d) == 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(u_id in x.getvalue())

    def testdo_destroy_error(self):
        """Tests destroy command with errors."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("destroy")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("destroy garbage")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("destroy BaseModel")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("destroy BaseModel 6524359")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** no instance found **")

    def helptest_destroy_advanced(self, classname):
        """Helps to test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("create {}".format(classname))
        u_id = x.getvalue()[:-1]
        self.assertTrue(len(u_id) > 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('{}.destroy("{}")'.format(classname, u_id))
        d = x.getvalue()[:-1]
        self.assertTrue(len(d) == 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(u_id in x.getvalue())

    def testdo_destroy_err_advanced(self):
        """Tests destroy() command with errors."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(".destroy()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("garbage.destroy()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("BaseModel.destroy()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('BaseModel.destroy("6524359")')
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** no instance found **")

    def testdo_all(self):
        """Tests all for all classes."""
        for clas in self.classes():
            self.helptest_do_all(clas)
            self.helptest_all_advanced(clas)

    def helptest_do_all(self, classname):
        """Helps in testing the all command."""
        u_id = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("all")
        d = x.getvalue()[:-1]
        self.assertTrue(len(d) > 0)
        self.assertIn(u_id, d)

        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("all {}".format(classname))
        d = x.getvalue()[:-1]
        self.assertTrue(len(d) > 0)
        self.assertIn(u_id, d)

    def testdo_all_error(self):
        """Tests all command with errors."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("all garbage")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class doesn't exist **")

    def helptest_all_advanced(self, classname):
        """Helps in testing the .all() command."""
        u_id = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("{}.all()".format(classname))
        d = x.getvalue()[:-1]
        self.assertTrue(len(d) > 0)
        self.assertIn(u_id, d)

    def testdo_all_error_advanced(self):
        """Tests out the all() command with errors."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("garbage.all()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class doesn't exist **")

    def testcount_all(self):
        """Tests count for all classes."""
        for classname in self.classes():
            self.helptest_count_advanced(classname)

    def helptest_count_advanced(self, classname):
        """Helps test .count() command."""
        for a in range(20):
            u_id = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("{}.count()".format(classname))
        d = x.getvalue()[:-1]
        self.assertTrue(len(d) > 0)
        self.assertEqual(d, "20")

    def testdo_count_error(self):
        """Tests .count() command with errors."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("garbage.count()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(".count()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class name missing **")

    def testupdate_1(self):
        """Tests for update 1..."""
        classname = "BaseModel"
        attr = "foostr"
        val = "fooval"
        u_id = self.create_class(classname)
        comd = '{}.update("{}", "{}", "{}")'
        comd = comd.format(classname, u_id, attr, val)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(comd)
        d = x.getvalue()
        self.assertEqual(len(d), 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, u_id))
        d = x.getvalue()
        self.assertIn(attr, d)
        self.assertIn(val, d)

    def testupdate_2(self):
        """Tests update 1..."""
        classname = "User"
        attr = "foostr"
        val = "fooval"
        u_id = self.create_class(classname)
        comd = '{}.update("{}", "{}", "{}")'
        comd = comd.format(classname, u_id, attr, val)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(comd)
        d = x.getvalue()
        self.assertEqual(len(d), 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, u_id))
        d = x.getvalue()
        self.assertIn(attr, d)
        self.assertIn(val, d)

    def testupdate_3(self):
        """Tests for update 1..."""
        classname = "City"
        attr = "foostr"
        val = "fooval"
        u_id = self.create_class(classname)
        comd = '{}.update("{}", "{}", "{}")'
        comd = comd.format(classname, u_id, attr, val)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(comd)
        d = x.getvalue()
        self.assertEqual(len(d), 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, u_id))
        d = x.getvalue()
        self.assertIn(attr, d)
        self.assertIn(val, d)

    def testupdate_4(self):
        """Tests for update 1..."""
        classname = "State"
        attr = "foostr"
        val = "fooval"
        u_id = self.create_class(classname)
        comd = '{}.update("{}", "{}", "{}")'
        comd = comd.format(classname, u_id, attr, val)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(comd)
        d = x.getvalue()
        self.assertEqual(len(d), 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, u_id))
        d = x.getvalue()
        self.assertIn(attr, d)
        self.assertIn(val, d)

    def testupdate_5(self):
        """Tests for update 1..."""
        classname = "Amenity"
        attr = "foostr"
        val = "fooval"
        u_id = self.create_class(classname)
        comd = '{}.update("{}", "{}", "{}")'
        comd = comd.format(classname, u_id, attr, val)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(comd)
        d = x.getvalue()
        self.assertEqual(len(d), 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, u_id))
        d = x.getvalue()
        self.assertIn(attr, d)
        self.assertIn(val, d)

    def testupdate_6(self):
        """Tests for update 1..."""
        classname = "Review"
        attr = "foostr"
        val = "fooval"
        u_id = self.create_class(classname)
        comd = '{}.update("{}", "{}", "{}")'
        comd = comd.format(classname, u_id, attr, val)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(comd)
        d = x.getvalue()
        self.assertEqual(len(d), 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, u_id))
        d = x.getvalue()
        self.assertIn(attr, d)
        self.assertIn(val, d)

    def testupdate_7(self):
        """Tests for update 1..."""
        classname = "Place"
        attr = "foostr"
        val = "fooval"
        u_id = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        cmd = cmd.format(classname, u_id, attr, val)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBComm:wand().onecmd(cmd)
        d = x.getvalue()
        self.assertEqual(len(d), 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, u_id))
        d = x.getvalue()
        self.assertIn(attr, d)
        self.assertIn(val, d)

    def testupdate_everything(self):
        """Tests the update command with errthang, like a baws."""
        for classname, cls in self.classes().items():
            u_id = self.create_class(classname)
            for attr, val in self.test_random_attributes.items():
                if type(val) is not str:
                    pass
                quotes = (type(val) == str)
                self.helptest_update(classname, u_id, attr,
                                      val, quot, False)
                self.helptest_update(classname, u_id, attr,
                                      val, quot, True)
            pass
            if classname == "BaseModel":
                continue
            for attr, attr_type in self.attributes()[classname].items():
                if attr_type not in (str, int, float):
                    continue
                self.help_test_update(classname, uid, attr,
                                      self.attribute_values[attr_type],
                                      True, False)
                self.help_test_update(classname, uid, attr,
                                      self.attribute_values[attr_type],
                                      False, True)

    def helptest_update(self, classname, uid, attr, val, quot, func):
        """Tests method for update commmand."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile("file.json"):
            os.remove("file.json")
        u_id = self.create_class(classname)
        val_str = ('"{}"' if quot else '{}').format(val)
        if func:
            comd = '{}.update("{}", "{}", {})'
        else:
            comd = 'update {} {} {} {}'
        comd = comd.format(classname, u_id, attr, val_str)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(cmd)
        mesg = x.getvalue()[:-1]
        self.assertEqual(len(mesg), 0)
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, u_id))
        p = x.getvalue()
        self.assertIn(str(val), p)
        self.assertIn(attr, p)

    def test_do_update_error(self):
        """Tests the update command with errors."""
        u_id = self.create_class("BaseModel")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("update")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("update garbage")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("update BaseModel")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("update BaseModel 6534276893")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** no instance found **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('update BaseModel {}'.format(u_id))
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** attribute name missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('update BaseModel {} name'.format(u_id))
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** value missing **")

    def test_do_update_error_advanced(self):
        """Tests out the update() command with errors."""
        u_id = self.create_class("BaseModel")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd(".update()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("garbage.update()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("BaseModel.update()")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("BaseModel.update(6534276893)")
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** no instance found **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('BaseModel.update("{}")'.format(u_id))
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** attribute name missing **")
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd('BaseModel.update("{}", "name")'.format(u_id))
        mesg = x.getvalue()[:-1]
        self.assertEqual(mesg, "** value missing **")

    def create_class(self, classname):
        """Method that Creates a class for console tests."""
        with patch('sys.stdout', new=StringIO()) as x:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = x.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        return uid

    def helpload_dict(self, rep):
        """Helper method to test dictionary equality."""
        ex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        rs = ex.match(rep)
        self.assertIsNotNone(rs)
        r = rs.group(3)
        r = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", r)
        j = json.loads(s.replace("'", '"'))
        return j

    def classes(self):
        """Returns dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        clas = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return clas

    def attribute(self):
        """Returns valid attributes and their types for classname."""
        attr = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
                     {"place_id": str,
                      "user_id": str,
                      "text": str}
        }
        return attr


if __name__ == "__main__":
    unittest.main()
