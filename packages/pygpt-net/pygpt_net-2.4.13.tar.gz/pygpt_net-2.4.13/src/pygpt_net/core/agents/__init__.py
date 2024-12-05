#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.11.14 01:00:00                  #
# ================================================== #

from .legacy import Legacy
from .memory import Memory
from .provider import Provider
from .runner import Runner
from .tools import Tools

class Agents:
    def __init__(self, window=None):
        """
        Agents core

        :param window: Window instance
        """
        self.window = window
        self.legacy = Legacy(window)
        self.memory = Memory(window)
        self.provider = Provider(window)
        self.runner = Runner(window)
        self.tools = Tools(window)
