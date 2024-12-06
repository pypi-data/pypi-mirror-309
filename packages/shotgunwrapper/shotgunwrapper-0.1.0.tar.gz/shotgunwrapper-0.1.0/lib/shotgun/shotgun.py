#!/bin/env/python

__doc__ = """
Contains wrapper class for shotgun api.
"""

import socket

import shotgun_api3

from shotgun import config
from shotgun.asset import Asset
from shotgun.base import Entity
from shotgun.logger import log
from shotgun.person import Person
from shotgun.playlist import Playlist
from shotgun.project import Project
from shotgun.sequence import Sequence
from shotgun.shot import Shot
from shotgun.task import Task
from shotgun.version import Version

# maps entity type string to wrapper class
entity_type_class_map = dict(
    [(cls.entity_type, cls) for cls in Entity.__subclasses__()]
)


class Shotgun(shotgun_api3.Shotgun):
    """
    Shotgun wrapper base class. Managed connection and starting point for
    all operations, e.g. ::

        >>> sg = Shotgun(name=<name>, apikey=<key>)
        >>> projects = sg.get_projects()

    Shotgun entity hierarchy:

        Shotgun
            `- Project
                `- Sequence
                    `- Shot
                        |- Version
                        |    `- Movie
                        `- Task
                            `- Person

    """

    def __init__(
        self,
        url=config.SG_SCRIPT_URL,
        name=config.SG_SCRIPT_NAME,
        apikey=config.SG_SCRIPT_KEY,
    ):
        super(Shotgun, self).__init__(url, name, apikey)
        self.url = url
        self.name = name
        self.apikey = apikey

    def __repr__(self):
        return '<{0} "{1}">'.format(self.__class__.__name__, self.name)

    def create_project(self, name, **data):
        """Creates and returns a new Project entity.

        :param name: project name
        :return: Project entity object
        """
        data.update({"name": name})
        results = self.create("Project", data=data)
        return Project(self, results)

    def find_entities(self, entity_type, filters):
        """Returns entities matching an entity type and filter list, e.g.
        find an asset with id 1440 ::

            sg.find_entities('Asset', [['id', 'is', 1440]])

        :param entity_type: the entity type string, e.g. Asset
        :param filters: list of filters to apply to the query, e.g. ::
            filters = [['id', 'is', 1440]]
        :returns wrapped entity object
        """
        entities = []
        entity_class = entity_type_class_map.get(entity_type)
        results = self.find(entity_type, filters, fields=entity_class.fields)
        for r in results:
            entity_type = r.get("type")
            entities.append(entity_class(self, data=r))
        return entities

    def get_projects(self, name=None, fields=None):
        """Returns a list of Project entities.

        :param name: project name
        :param fields: which fields to return (optional)
        :return: list of projects
        :raise: socket.gaierror if can't connect to shotgun.
        """

        fields = fields or Project.fields
        params = []

        if name:
            params.append(["name", "is", name])

        try:
            results = self.find("Project", params, fields=fields)
            projects = list()
            for r in results:
                projects.append(Project(self, data=r))
            return projects

        except socket.gaierror as err:
            log.error(err.message)
            raise

    def parent(self):
        return None

    def type(self):
        """Returns shotgun entity type as str."""
        return self.__class__.__name__
