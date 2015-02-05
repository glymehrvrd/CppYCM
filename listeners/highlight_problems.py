import sublime
import sublime_plugin
import json
from threading import Thread

from ..lib.ycmd_handler import server
from ..lib.utils import *
from ..lib.msgs import MsgTemplates

class SYCMHighlightProblemsListener(sublime_plugin.EventListener):

    def on_selection_modified_async(self, view):
        if not is_cpp(view) or view.is_scratch():
            return
        # update_statusbar(view)

    def on_post_save_async(self, view):
        if not is_cpp(view) or view.is_scratch():
            return
        # run highlight problems command
        view.window().run_command('sycm_highlight_problems')
        