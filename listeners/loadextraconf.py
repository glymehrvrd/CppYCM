import sublime
import sublime_plugin
import json
from threading import Thread

from ..lib.ycmd_handler import server
from ..lib.utils import *
from ..lib.msgs import MsgTemplates


def load_extra_conf_func(server, filepath):
    '''
    Thread that loads extra conf
    '''
    conf_path = find_recursive(filepath)
    if not conf_path:
        sublime.status_message(
            '[C++YouCompleteMe] .ycm_extra_conf.py not found. All C++YouCompleteMe function not avaliable.')
        print('[C++YouCompleteMe] .ycm_extra_conf.py not found.')
        return

    server.WaitUntilReady()
    server.LoadExtraConfFile(conf_path)
    print(MsgTemplates.LOAD_EXTRA_CONF_FINISHED)


class CppYCMLoadExtraConfListener(sublime_plugin.EventListener):

    '''
    Activate ycmd server and loads extra_conf on cpp file loaded.
    '''

    def on_activated_async(self, view):
        '''
        Called when a view gains input focus.
        '''
        if not is_cpp(view) or view.is_scratch():
            return
        # if is cpp, activate ycmd server
        server(view.file_name())
        t = Thread(None, load_extra_conf_func, 'LoadExtraConfAsync',
                   [server(), get_file_path(view.file_name())])
        t.daemon = True
        t.start()
