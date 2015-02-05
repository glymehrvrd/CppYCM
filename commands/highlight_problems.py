import sublime
import sublime_plugin
import json
from threading import Thread

from ..lib.ycmd_handler import server
from ..lib.utils import *
from ..lib.ycmd_events import Event
from ..lib.msgs import MsgTemplates


def notification_func(server, filepath, contents, callback):
    '''
    Thread that send event notification
    '''
    data = server.SendEventNotification(Event.FileReadyToParse,
                                        filepath=filepath,
                                        contents=contents,
                                        filetype='cpp')
    if data == '':
        return
    callback(data)


class SycmHighlightProblemsCommand(sublime_plugin.WindowCommand):

    '''
    Goto command
    '''

    def __init__(self, window):
        self.window = window
        self.output_panel = self.window.create_output_panel(
            'SYCM.{}'.format(self.window.id()))
        self.output_panel_name = 'output.SYCM.{}'.format(self.window.id())

    def run(self):
        view = active_view()
        filepath = get_file_path(view.file_name())
        contents = view.substr(sublime.Region(0, view.size()))

        t = Thread(None, notification_func, 'NotifyAsync',
                   [server(), filepath, contents, self._on_errors])
        t.daemon = True
        t.start()

    def is_enabled(self):
        ''' 
        Determine if this command is enabled or not
        '''
        return is_cpp(active_view())

    def _on_errors(self, data):
        view = active_view()
        data = json.loads(data)
        filepath = get_file_path(view.file_name())
        self.highlight_problems(view,
                                [_ for _ in data
                                    if get_file_path(_['location']['filepath']) == filepath])
        # self.update_statusbar(active_view(), force=True)

    def highlight_problems(self, view, problems):
        view.erase_regions('clang-code-errors')
        view_id = view.id()
        view_cache = {}
        regions = []
        # erase output panel
        self.output_panel.set_read_only(False)
        self.output_panel.run_command('select_all')
        self.output_panel.run_command('right_delete')
        for problem in problems:
            lineno = problem['location']['line_num']
            colno = problem['location']['column_num']
            line_regions = view_cache.setdefault(lineno - 1, {})
            message = MsgTemplates.ERROR_MESSAGE_TEMPLATE.format(**problem)
            problem_output = MsgTemplates.PRINT_ERROR_MESSAGE_TEMPLATE.format(
                message, lineno, colno)
            self.output_panel.run_command(
                'insert', {'characters': problem_output}
            )

            region = view.word(view.text_point(lineno - 1, colno - 1))
            regions.append(region)
            line_regions[(region.a, region.b)] = message

        self.output_panel.set_read_only(True)
        self.window.run_command(
            'show_panel', {'panel': self.output_panel_name})
        # self.view_cache[view_id] = view_cache
        style = (sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE |
                 sublime.DRAW_SQUIGGLY_UNDERLINE)
        view.add_regions(
            key='clang-code-errors',
            regions=regions,
            scope='invalid',
            flags=style)
