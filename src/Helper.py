import sublime
import re
from datetime import datetime


def plugin_setting(name):
    active_view = sublime.active_window().active_view()
    default_setting = sublime.load_settings('ShellCommander.sublime-settings').get(name, {})
    project_setting = active_view.settings().get('shell_commander')

    if project_setting and name in project_setting:
        default_setting.update(project_setting[name])

    return default_setting


def time():
    return datetime.now().strftime("%a %I:%M:%S%p")


def match_pattern(pattern, subject):
    if subject and pattern:
        pattern = re.compile(pattern)
        return pattern.match(subject)
    return False


def parameters(windowCommand):
    def main_folder(folders):
        if len(folders):
            return folders[0]
        return ""

    project_path = main_folder(windowCommand.window.folders())
    active_view = windowCommand.window.active_view()
    filename = None
    if active_view:
        filename = windowCommand.window.active_view().file_name()

    relative_filename = ''
    file_path = ''
    if filename:
        relative_filename = filename.replace(project_path + '/', '')
        pattern = re.compile(".+\\/.+\\..+$")
        file_path = pattern.sub("", filename)
    return {
        'project_path': project_path,
        'filename': filename,
        'relative_filename': relative_filename,
        'file_path': file_path
    }
