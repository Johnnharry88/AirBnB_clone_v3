#!/usr/bin/python3
"""Modules that defines the Class State"""
from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(test_basemodel):
    """Defines the test case for the state """

    def __init__(self, *args, **kwargs):
        """Tests  the args and kwargs """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ Test the name of state"""
        new = self.value()
        self.assertEqual('State', self.name)
