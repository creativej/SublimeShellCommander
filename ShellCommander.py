import sublime_plugin, os, re
from ShellCommander.CommandThread import CommandThread
from ShellCommander.Helpers import plugin_setting
from ShellCommander.Helpers import time
from ShellCommander.Helpers import match_pattern
import pprint, inspect

def main_folder(folders):
    if len(folders):
        return folders[0]
    return ""

def parameters(windowCommand):
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

class ShellCommander(sublime_plugin.WindowCommand):
    def console_view(self):
        try:
            self.view
            if self.view_not_exist(self.view):
                raise AttributeError()
        except AttributeError:
            self.view = self.window.new_file()
            self.view.set_scratch(True)
            args = {}
            if (self.window.active_group() > self.window.num_groups() - 1):
                args = {"forward": False}
            self.window.run_command('move_to_neighboring_group', args)
        return self.view

    def run(self, name):
        command = plugin_setting('commands')[name]

        params = parameters(self)

        for key in params:
            if params[key]:
                command = command.replace('{{' + key + '}}', params[key])

        self.focus_on_console()
        self.console(
            '%s $: %s' % (time(), command),
            True
        )
        CommandThread(command).done(self.console).start()

    def console_group(self):
        return self.window.get_view_index(self.console_view())[0]

    def focus_on_console(self):
        view = self.console_view()
        if self.window.active_group() == self.console_group():
            self.window.focus_view(view)

    def console(self, text, jump = False):
        self.console_view().run_command(
            'update_console_view',
            {"text": text + '\n', "jump": jump}
        )

    def view_not_exist(self, view):
        return self.window.get_view_index(self.view)[0] == -1

class UpdateConsoleViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, text, jump = False):
        regions = self.view.find_all('$')

        if len(regions):
            last_region = regions[len(regions) - 1]
            if jump:
                eof = self.view.layout_extent()[1]
                self.view.set_viewport_position((0, eof))
            self.view.insert(edit, last_region.end(), text)

class EventCommandHooks(sublime_plugin.EventListener):
    def on_post_save(self, view):
        self.execute_valid_hook(view, inspect.stack()[0][3])
    def on_pre_save(self, view):
        self.execute_valid_hook(view, inspect.stack()[0][3])
    def on_pre_close(self, view):
        self.execute_valid_hook(view, inspect.stack()[0][3])
    def on_close(self, view):
        self.execute_valid_hook(view, inspect.stack()[0][3])
    def on_activated(self, view):
        self.execute_valid_hook(view, inspect.stack()[0][3])
    def on_new(self, view):
        self.execute_valid_hook(view, inspect.stack()[0][3])

    def execute_valid_hook(self, view, name):
        hooks = self.hooks()
        if (hooks and name in hooks):
            self.execute_hook(view, hooks[name])

    def hooks(self):
        return plugin_setting('hooks')

    def execute_hook(self, view, data):
        if (
            'command' in data and
            match_pattern(data['pattern'], view.file_name())
        ):
            view.window().run_command("shell_commander", { "name": data['command'] })
