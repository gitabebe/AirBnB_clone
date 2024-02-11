#!/usr/bin/python3
"""
class FileStorage that serializes instances to a JSON file and
deserialzes JSON file to instances
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """FileStorage class"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        jsonData = {}
        for key, value in self.__objects.items():
            jsonData[key] = value.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(jsonData, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for key, obj_dict in data.items():
                    class_name = obj_dict['__class__']
                    del obj_dict['__class__']
                    try:
                        obj = globals()[class_name](**obj_dict)
                        self.__objects[key] = obj
                    except TypeError as e:
                        print(f"Error loading object {key}: {e}")
        except FileNotFoundError:
            pass
