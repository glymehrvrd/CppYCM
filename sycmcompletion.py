import sublime
import sublime_plugin
import os
import json
from threading import Thread

from .lib.ycmd_handler import YcmdHandle
from .lib.ycmd_events import Event

from .lib.utils import *
## ##
# MESSAGES TEMPLATES #
## ##
COMPLETION_ERROR_MSG = "[SYCM][Completion] Error {}"
COMPLETION_NOT_AVAILABLE_MSG = "[SYCM] No completion available"
ERROR_MESSAGE_TEMPLATE = "[{kind}] {text}"
GET_PATH_ERROR_MSG = "[SYCM][Path] Failed to replace '{}' -> '{}'"
NO_HMAC_MESSAGE = "[SYCM] You should generate HMAC throug the menu before using plugin"
NOTIFY_ERROR_MSG = "[SYCM][Notify] Error {}"
PRINT_ERROR_MESSAGE_TEMPLATE = "[SYCM] > {} ({},{})"


def plugin_loaded():
    pass


def plugin_unloaded():
    server().Shutdown()

_server = None


def server():
    '''
    return singleton server instance
    '''
    global _server
    if _server == None:
        _server = YcmdHandle.StartYcmdAndReturnHandle()
        _server.WaitUntilReady()
        t = Thread(None, load_extra_conf_func, 'LoadExtraConfAsync',
                   [_server, get_file_path()])
        t.daemon = True
        t.start()

        print('[SYCM] server registered, location: %s' %
              _server._server_location)
    return _server


def load_extra_conf_func(server, filepath):
    '''
    Thread that loads extra conf
    '''
    conf_path = find_recursive(filepath)
    server.LoadExtraConfFile(conf_path)


def goto_func(server, filepath, contents, row, col, callback):
    '''
    Thread that send goto declaration
    '''
    rst = server.SendGoToRequest(filepath=filepath,
                                 contents=contents,
                                 filetype='cpp',
                                 line_num=23,
                                 column_num=4)
    if rst == '':
        return
    data = json.loads(rst)
    row = data.get('line_num', 1) - 1
    col = data.get('column_num', 1) - 1
    callback(row, col)


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


def complete_func(server, filepath, contents, row, col, callback):
    '''
    Thread that send completion request
    '''
    rst = server.SendCodeCompletionRequest(filepath=filepath,
                                           contents=contents,
                                           filetype='cpp',
                                           line_num=row,
                                           column_num=col)
    if rst == '':
        return

    completions = json.loads(rst)['completions']

    data = []
    for comp in completions:
        data.append(
            (
                '{}\t{}'.format(comp.get('menu_text', ''),
                                comp.get('extra_menu_info', '')
                                ),
                comp.get('insertion_text', '')
            )
        )
    callback(data)


class SYCMCompletions(sublime_plugin.EventListener):

    def __init__(self):
        self.completions = []
        self.ready_from_defer = False
        self.view_cache = dict()
        self.view_line = dict()
        self.extra_conf_loaded = False

    def on_selection_modified_async(self, view):
        if not is_cpp(view) or view.is_scratch():
            return
        self.update_statusbar(view)

    def on_activated_async(self, view):
        '''
        Called when the file is finished loading
        '''
        if not is_cpp(view) or view.is_scratch():
            return
        # if is cpp, activate ycmd server
        server()

    def on_post_save_async(self, view):
        if not is_cpp(view) or view.is_scratch():
            return

        filepath = get_file_path(view.file_name())
        contents = view.substr(sublime.Region(0, view.size()))

        t = Thread(None, notification_func, 'NotifyAsync',
                   [server(), filepath, contents, self._on_errors])
        t.daemon = True
        t.start()

    def on_pre_close(self, view):
        view_id = view.id()
        if view_id in self.view_line:
            del self.view_line[view_id]
        if view_id in self.view_cache:
            del self.view_cache[view_id]

    def on_query_completions(self, view, prefix, locations):
        '''
        Sublime Text autocompletion event handler.
        '''
        if not is_cpp(view) or view.is_scratch():
            return

        # if completion should begin
        leftchar = view.substr(locations[0] - 2)
        thischar = view.substr(locations[0] - 1)
        if thischar == '>' and leftchar != '-':
            return
        if thischar == ':' and leftchar != ':':
            return

        print("[SYCM] #### START COMPLETION ####")

        if self.ready_from_defer is True:
            cpl = self.completions
            self.completions = []
            self.ready_from_defer = False
            return (cpl, sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

        filepath = get_file_path(view.file_name())
        contents = view.substr(sublime.Region(0, view.size()))

        # get 1-based location
        row, col = view.rowcol(locations[0])
        row = row + 1
        col = col + 1

        # start code-completion thread
        t = Thread(None, complete_func, 'CompleteAsync',
                   [server(), filepath, contents, row, col, self._complete])
        t.daemon = True
        t.start()

    def _complete(self, proposals):
        if len(proposals):
            active_view().run_command("hide_auto_complete")
            self.completions = proposals
            self.ready_from_defer = True
            self._run_auto_complete()
        else:
            sublime.status_message(COMPLETION_NOT_AVAILABLE_MSG)

    def _run_auto_complete(self):
        active_view().run_command("auto_complete", {
            'disable_auto_insert': True,
            'next_completion_if_showing': False,
            'auto_complete_commit_on_tab': True,
        })

    def _on_errors(self, data):
        data = json.loads(data)
        filepath = get_file_path()
        self.highlight_problems(active_view(),
                                [_ for _ in data
                                    if get_file_path(_['location']['filepath']) == filepath])
        self.update_statusbar(active_view(), force=True)

    def update_statusbar(self, view, force=False):
        row, col = get_selected_pos(view)
        view_id = view.id()
        text_point = view.text_point(row, col)

        if not force:
            beg, end = self.view_line.get(view_id, (None, None))
            if beg and end and sublime.Region(beg, end).contains(text_point):
                return

        errors_regions = self.view_cache.get(view_id, {}).get(row, {})
        for region, msg in errors_regions.items():
            if sublime.Region(*region).contains(text_point) and msg:
                view.set_status('clang-code-errors', msg)
                self.view_line[view_id] = region
                return
        if view_id in self.view_line:
            del self.view_line[view_id]
        view.erase_status('clang-code-errors')

    def highlight_problems(self, view, problems):
        view.erase_regions('clang-code-errors')
        view_id = view.id()
        view_cache = {}
        regions = []
        for problem in problems:
            lineno = problem['location']['line_num']
            colno = problem['location']['column_num']
            line_regions = view_cache.setdefault(lineno - 1, {})
            message = ERROR_MESSAGE_TEMPLATE.format(**problem)
            print(PRINT_ERROR_MESSAGE_TEMPLATE.format(message, lineno, colno))
            region = view.word(view.text_point(lineno - 1, colno - 1))
            regions.append(region)
            line_regions[(region.a, region.b)] = message
        self.view_cache[view_id] = view_cache
        style = (sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE |
                 sublime.DRAW_SQUIGGLY_UNDERLINE)
        view.add_regions(
            key='clang-code-errors',
            regions=regions,
            scope='invalid',
            flags=style)


class SycmGoto(sublime_plugin.TextCommand):

    '''
    Goto command
    '''

    def run(self, edit):
        # get 1-based location
        row, col = self.view.rowcol(self.view.sel()[0].begin())
        row = row + 1
        col = col + 1

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
