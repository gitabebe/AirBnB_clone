#!/usr/bin/python3
"""
class BaseModel that defines all common attributes/methods
for other classes
"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """BaseModel class"""
    def __init__(self, *args, **kwargs):
        """class initialization"""
        valid_keys = {'id', 'created_at', 'updated_at'}
        if kwargs:
            for key, value in kwargs.items():
                if key not in valid_keys and key != '__class__':
                    raise KeyError(f"Unexpected keyword argument: {key}")
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """a string to reprsent base model"""
        return "[{}] ({}) {}".format(
                type(self).__name__, self.id, self.__dict__)

    def __repr__(self):
        """returns string function"""
        return self.__str__()

    def save(self):
        """updates updated_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__"""
        copy = dict(self.__dict__)
        copy['__class__'] = str(self.__class__.__name__)
        copy['created_at'] = self.created_at.isoformat()
        copy['updated_at'] = self.updated_at.isoformat()
        return copy
