import os
import sublime

def get_plugin_path():
    plugin_path = os.path.join(sublime.packages_path(), 'SYCM')
    return plugin_path

def get_ycmd_path():
    ycmd_path = os.path.join(get_plugin_path(), 'server', 'ycmd')
    return ycmd_path


def find_recursive(path):
    '''
    find ycm_extra_conf in path and all directories above it.
    '''
    path = os.path.dirname(path)
    while(True):
        if os.path.exists(os.path.join(path, '.ycm_extra_conf.py')):
            return os.path.join(path, '.ycm_extra_conf.py')
        parent_dir = os.path.dirname(path)
        if parent_dir == path:
            break
        else:
            path = parent_dir
    return ''


def is_cpp(view):
    '''
    Determine if the given view location is c++ code
    '''
    try:
        return view.match_selector(view.sel()[0].begin(), 'source.c++')
    except:
        return False


def active_view():
    return sublime.active_window().active_view()


def get_file_path(filepath=None):
    '''
    Get path of the editing file. 
    '''
    if not filepath:
        filepath = active_view().file_name()
    if not filepath:
        filepath = 'tmpfile.cpp'
    return filepath


def get_selected_pos(view):
    '''
    return 1-based row and column of selected region
    '''
    try:
        row, col = view.rowcol(view.sel()[0].end())
        return (row + 1, col + 1)
    except:
        return None

