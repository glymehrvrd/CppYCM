import sublime
import sublime_plugin
import json
from threading import Thread

from ..lib.ycmd_handler import server
from ..lib.utils import *

def goto_func(server, filepath, contents, row, col, callback):
    '''
    Thread that send goto declaration
    '''
    rst = server.SendGoToRequest(filepath=filepath,
                                 contents=contents,
                                 filetype='cpp',
                                 line_num=row,
                                 column_num=col)
    if rst == '':
        return
    data = json.loads(rst)
    row = data.get('line_num', 1) - 1
    col = data.get('column_num', 1) - 1
    callback(row, col)


class SycmGotoCommand(sublime_plugin.TextCommand):

    '''
    Goto command
    '''

    def run(self, edit):
        # prepare parameters
        row, col = get_row_col(self.view)
        filepath = get_file_path(self.view.file_name())
        contents = self.view.substr(sublime.Region(0, self.view.size()))

        # start goto thread
        t = Thread(None, goto_func, 'GotoAsync',
                   [server(), filepath, contents, row, col, self._goto])
        t.daemon = True
        t.start()

    def is_enabled(self):
        ''' 
        Determine if this command is enabled or not
        '''

        return is_cpp(self.view)

    def _goto(self, row, col):
        '''
        Goto declaration callback
        '''
        point = self.view.text_point(row, col)
        region = self.view.word(point)
        self.view.sel().clear()
        self.view.sel().add(region)
        self.view.show_at_center(region)
