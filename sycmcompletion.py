import sublime
import sublime_plugin
import os
import json

from .lib.ycmd_handler import server

from .listeners import *
from .commands import *

def plugin_loaded():
    pass


def plugin_unloaded():
    server().Shutdown()
