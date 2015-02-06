import os
import sublime


def get_plugin_path():
    '''
    Get path of the CppYCM plugin
    '''
    plugin_path = os.path.abspath(
        os.path.join(sublime.packages_path(), 'CppYCM'))
    return plugin_path


def get_ycmd_path():
    '''
    Get path of the ycmd server
    '''
    settings = sublime.load_settings('CppYCM.sublime-settings')
    ycmd_path = settings.get('ycmd_path', os.path.join(
        get_plugin_path(), 'server')).replace('${packages}', sublime.packages_path())
    ycmd_path = os.path.join(ycmd_path, 'ycmd')
    return ycmd_path


def get_python_path():
    '''
    Get path of python
    '''
    settings = sublime.load_settings('CppYCM.sublime-settings')
    python_path = settings.get('python_path', 'python')
    return python_path


def get_file_path(filepath=None):
    '''
    Get path of the editing file. 
    '''
    if not filepath:
        filepath = active_view().file_name()
    if not filepath:
        filepath = 'tmpfile.cpp'
    return filepath


def check_ycmd_server():
    return os.path.exists(get_ycmd_path())


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
    Determine if the given view is c++ code
    '''
    try:
        return view.match_selector(view.sel()[0].begin(), 'source.c++')
    except:
        return False


def active_view():
    '''
    return active view
    '''
    return sublime.active_window().active_view()


def get_row_col(view, location=None):
    '''
    return 1-based row and column of selected region
    if location is None, set location to cursor location.
    '''
    try:
        if not location:
            location = view.sel()[0].begin()
        row, col = view.rowcol(location)
        return (row + 1, col + 1)
    except:
        return None


def update_statusbar(self, view, view_line, view_cache, force=False):
    row, col = get_row_col(view)
    view_id = view.id()
    text_point = view.text_point(row, col)

    if not force:
        beg, end = view_line.get(view_id, (None, None))
        if beg and end and sublime.Region(beg, end).contains(text_point):
            return

    errors_regions = view_cache.get(view_id, {}).get(row, {})
    for region, msg in errors_regions.items():
        if sublime.Region(*region).contains(text_point) and msg:
            view.set_status('clang-code-errors', msg)
            view_line[view_id] = region
            return
    if view_id in view_line:
        del view_line[view_id]
    view.erase_status('clang-code-errors')
