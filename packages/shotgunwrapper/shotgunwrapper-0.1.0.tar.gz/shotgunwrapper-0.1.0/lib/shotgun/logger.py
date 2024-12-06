#!/usr/bin/env python

__doc__ = """
Contains logger setup.
"""

import logging

from shotgun import config

log = logging.Logger("shotgun")
log.setLevel(config.LOG_LEVEL)

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
log.addHandler(streamHandler)
