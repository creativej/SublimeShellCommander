import sublime, re
from datetime import datetime

def plugin_setting(name):
    setting = sublime.load_settings('ShellCommander.sublime-settings').get
    project_setting = sublime.active_window().active_view().settings().get('shell_commander')
    if name in project_setting:
        return project_setting[name]
    return setting(name)

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

    project_path = main_folder(windowCommand.window.folders());
    active_view = windowCommand.window.active_view()
    filename = None
    if active_view:
        filename = windowCommand.window.active_view().file_name()

    relative_filename = ''
    if filename:
        relative_filename = filename.replace(project_path + '/', '')

    return {
        'project_path': project_path,
        'filename': filename,
        'relative_filename': relative_filename
    }
