import sublime
import sublime_plugin
import json
from threading import Thread

from ..lib.ycmd_handler import server
from ..lib.utils import *
from ..lib.msgs import MsgTemplates


class CppYCMHighlightProblemsListener(sublime_plugin.EventListener):

    def on_selection_modified_async(self, view):
        if not is_cpp(view) or view.is_scratch():
            return
        # Not work in st3, output panel wouldn't call this callback
        # from ..commands.highlight_problems import output_panel
        # if output_panel and (view.id() == output_panel.id()):
        #     sublime.message_dialog('match!')
        # update_statusbar(view)

    def on_post_save_async(self, view):
        if not is_cpp(view) or view.is_scratch():
            return
        # run highlight problems command
        if check_highlight_on_save():
            view.window().run_command('cppycm_highlight_problems')
