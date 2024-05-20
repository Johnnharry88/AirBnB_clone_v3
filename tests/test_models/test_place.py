#!/usr/bin/python3
"""Module that deines test for Class Place"""
from tests.test_models.test_base_model import test_basemodel
from models.place import Place


class test_Place(test_basemodel):
    """Defines  test case for Place """

    def __init__(self, *args, **kwargs):
        """Test *args and **kwargs """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """Test id """
        alx = self.value()
        self.assertEqual(alx.city_id, None)

    def test_user_id(self):
        """ Test user id"""
        alx = self.value()
        self.assertEqual(alx.user_id, None)

    def test_name(self):
        """Test the str for name """
        alx = self.value()
        self.assertEqual(alx.name, None)

    def test_description(self):
        """Test description """
        alx = self.value()
        self.assertEqual(alx.description, None)

    def test_number_rooms(self):
        """Test room number """
        alx = self.value()
        self.assertEqual(alx.number_rooms, None)

    def test_number_bathrooms(self):
        """Test bethroom number """
        alx = self.value()
        self.assertEqual(alx.number_bathrooms, None)

    def test_max_guest(self):
        """Test maimum guest"""
        alx = self.value()
        self.assertEqual(alx.max_guest, None)

    def test_price_by_night(self):
        """Tests night price """
        alx = self.value()
        self.assertEqual(alx.price_by_night, None)

    def test_latitude(self):
        """Test latitude """
        alx = self.value()
        self.assertEqual(alx.latitude, None)

    def test_longitude(self):
        """Test longitude """
        alx = self.value()
        self.assertEqual(alx.latitude, None)
