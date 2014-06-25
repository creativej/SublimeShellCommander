from .lib import WindowCommand
from .lib import Command
from .lib import Helper
from .lib import DefaultCommands
import sublime_plugin
import json
import imp
import inspect
import sublime
import os
from datetime import datetime


def plugin_path():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


class ShellCommanderRunPredefinedCommand(WindowCommand.WindowCommand):
    def run(self, **args):
        command = Command.Command.from_args(args, Helper.params(self))

        if not command:
            return

        self.command = command
        self.focus_on_console()
        self.run_command()


class ShellCommanderGenerateCommandsCommand(sublime_plugin.WindowCommand):
    def run(self, **args):
        commands = Helper.plugin_setting('commands')
        list = DefaultCommands.commands()
        for name in commands.keys():
            list.append(
                DefaultCommands.new(name, 'shell_commander_run_predefined')
            )

        default_commands_file = open("%s/Default.sublime-commands" % plugin_path(), "w")
        default_commands_file.write("// This is file generated from a Shell commander command at %s\n" % Helper.time())
        default_commands_file.write(json.dumps(list))
        default_commands_file.close()


class UpdateConsoleViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, text, jump=False):
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
            self.execute_hooks(view, hooks[name])

    def hooks(self):
        return Helper.plugin_setting('hooks')

    def execute_hooks(self, view, data):
        if isinstance(data, (list, tuple)):
            for hook in data:
                self.execute_hook(view, hook)
        else:
            self.execute_hook(view, data)

    def execute_hook(self, view, hook):
        if not Helper.match_pattern(hook['pattern'], view.file_name()):
            return

        if 'name' in hook:
            view.window().run_command("shell_commander_run_predefined", {"name": hook['name']})
        elif 'command' in hook:
            view.window().run_command("shell_commander_run_predefined", {"command": hook['command']})
