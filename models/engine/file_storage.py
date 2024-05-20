#!/usr/bin/python3
"""this is the file storage class for AirBnB"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex


class FileStorage:
    """Class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return: dictionary of __object"""
        dic = {}
        if cls:
            dictionary = self.__objects
            for key in dictionary:
                partition = key.replace('.', ' ')
                partition = shlex.split(partition)
                if (partition[0] == cls.__name__):
                    dic[key] = self.__objects[key]
            return (dic)
        else:
            return self.__objects

    def new(self, obj):
        """sets __object to given obj """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file """
        dict_x = {}
        for k, v in self.__objects.items():
            dict_x[k] = v.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as x:
            json.dump(dict_x, x)

    def reload(self):
        """Deserialize the file path to JSON file path """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for k, v in (json.load(f)).items():
                    v = eval(v["__class__"])(**v)
                    self.__objects[k] = v
        except FileNotFoundError:
            Exception

    def delete(self, obj=None):
        """ delete an existing element
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """ calls rmeove() method on session attribute """
        self.reload()

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching the given class name.
        """
        if cls:
            counter = 0
            for obj in self.__objects.values():
                if obj.__class__.__name__ == cls:
                    counter += 1
            return counter
        return len(self.__objects)

    def get(self, cls, id):
        """ retrieves """
        if cls in self.__objects.values() and id and type(id) == str:
            d_obj = self.all(cls)
            for key, value in d_obj.items():
                if key.split(".")[1] == id:
                    return value
        return None
