import sublime
import re
import json
from datetime import datetime


def plugin_setting(name):
    active_view = sublime.active_window().active_view()
    default_setting = sublime.load_settings('ShellExec.sublime-settings').get(name, {})

    if not active_view:
        return {}

    project_setting = active_view.settings().get('shell_exec', {})

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

def main_folder(window):
    folders = window.folders()
    if folders and len(folders):
        return folders[0]
    return ""

def params(windowCommand):
    project_path = main_folder(windowCommand.window)
    active_view = windowCommand.window.active_view()
    filename = None
    active_symbol = ''

    if active_view:
        filename = windowCommand.window.active_view().file_name()
        active_symbol = active_view.substr(active_view.word(active_view.sel()[0]))

    relative_filename = ''
    file_path = ''
    if filename:
        relative_filename = filename.replace(project_path + '/', '')
        pattern = re.compile(".+\\/.+\\..+$")
        file_path = pattern.sub("", filename)

    return {
        'project_path': project_path,
        'filename': filename,
        'relative_filename': json.dumps(relative_filename),
        'file_path': file_path,
        'active_symbol': active_symbol
    }


