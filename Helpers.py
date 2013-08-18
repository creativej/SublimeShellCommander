import sublime, re
from datetime import datetime

def plugin_setting(name = None):
    setting = sublime.load_settings('ShellCommander.sublime-settings').get
    if name:
        return setting(name)
    return setting

def time():
    return datetime.now().strftime("%a %I:%M:%S%p")

def match_pattern(pattern, subject):
    if subject and pattern:
        pattern = re.compile(pattern)
        return pattern.match(subject)
    return False
