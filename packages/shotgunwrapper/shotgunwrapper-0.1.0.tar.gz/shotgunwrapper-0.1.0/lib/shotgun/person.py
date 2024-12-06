#!/usr/bin/env python

__doc__ = """
Contains Person base class.
"""

from shotgun.base import Entity
from shotgun.logger import log


class Person(Entity):
    """Shotgun Person entity."""

    entity_type = "HumanUser"

    fields = [
        "id",
        "department",
        "email",
        "login",
        "name",
        "sg_status_list",
    ]

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<{0} "{1}">'.format(self.__class__.__name__, self.data.name)
