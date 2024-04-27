#!/usr/bin/python3
""" new class for sqlAlchemy """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ create tables in environmental"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns dictionary of __object"""
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            alx = self.__session.query(cls)
            for x in alx:
                key = "{}.{}".format(type(x).__name__, x.id)
                dic[key] = x
        else:
            list_x = [State, City, User, Place, Review, Amenity]
            for a in list_x:
                alx = self.__session.query(a)
                for x in alx:
                    key = "{}.{}".format(type(x).__name__, x.id)
                    dic[key] = x
        return (dic)

    def new(self, obj):
        """adds new element in the table"""
        self.__session.add(obj)

    def save(self):
        """saves changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes element in the table"""
        if obj:
            self.session.delete(obj)

    def reload(self):
        """configuration and reloads datatbase"""
        Base.metadata.create_all(self.__engine)
        xty = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(xty)
        self.__session = Session()

    def close(self):
        """Closes database session"""
        self.__session.close()
