#!/usr/bin/env python

__doc__ = """
Contains Version base class.
"""

from shotgun.base import Entity
from shotgun.logger import log


class Version(Entity):
    """Shotgun Version entity."""

    entity_type = "Version"

    fields = [
        "id",
        "description",
        "code",
        "sg_path_to_frames",
        "sg_status_list",
        "sg_uploaded_movie",
    ]

    def __init__(self, *args, **kwargs):
        super(Version, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<{0} "{1}">'.format(self.__class__.__name__, self.data.code)

    @property
    def movie(self):
        from shotgun.media import Movie

        return Movie(self, self.data.sg_uploaded_movie)
