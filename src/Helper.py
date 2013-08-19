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
