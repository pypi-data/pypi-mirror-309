#!/bin/env/python

__doc__ = """
Shotgun API wrapper.
"""

__prog__ = "shotgunwrapper"
__version__ = "0.1.0"
__author__ = "ryan@rsg.io"

import envstack

envstack.init(__prog__)

from .shotgun import Shotgun
