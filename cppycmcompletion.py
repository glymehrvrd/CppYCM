import sublime
import sublime_plugin
import os
import json

from .lib.utils import *
from .lib.ycmd_handler import server

from .listeners import *
from .commands import *

def plugin_loaded():
    if not check_ycmd_server():
        sublime.message_dialog('Ycmd is not found, see https://github.com/glymehrvrd/CppYCM#installation for install instructions.')


def plugin_unloaded():
    server().Shutdown()
