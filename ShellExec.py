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

def sublime_commands_path():
    return os.path.join(plugin_path(), "Default.sublime-commands")

def update_sublime_commands(view):
    window = view.window()

    if not window:
        return

    with open(sublime_commands_path(), 'w+') as f:
        first_line = f.readline()

    command_project_path = first_line.replace("//", "").strip()

    if command_project_path != Helper.main_folder(window):
        window.run_command('shell_exec_generate_commands')


class ShellExecCommand(WindowCommand.WindowCommand):
    def run(self, **args):
        command = Command.Command.from_args(args, Helper.params(self))

        if not command:
            return

        self.command = command
        self.focus_on_console()
        self.run_command()


class ShellExecGenerateCommandsCommand(sublime_plugin.WindowCommand):
    def run(self, **args):
        commands = Helper.plugin_setting('commands')
        new_commands = DefaultCommands.commands()
        for name in commands.keys():
            new_commands.append(
                DefaultCommands.new(name, 'shell_exec')
            )

        default_commands_file = open(
            sublime_commands_path(),
            "w"
        )
        default_commands_file.write("// %s\n" % Helper.main_folder(self.window))
        default_commands_file.write("// This is file generated from a Shell Exec command at %s\n" % Helper.time())
        default_commands_file.write(json.dumps(new_commands))
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
        self.execute_valid_hook(view, 'on_post_save')

    def on_pre_save(self, view):
        self.execute_valid_hook(view, 'on_pre_save')

    def on_pre_close(self, view):
        self.execute_valid_hook(view, 'on_pre_close')

    def on_close(self, view):
        self.execute_valid_hook(view, 'on_close')

    def on_activated(self, view):
        update_sublime_commands(view)

        self.execute_valid_hook(view, 'on_activated')

    def on_new(self, view):
        self.execute_valid_hook(view, 'on_new')

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
            view.window().run_command("shell_exec", {"name": hook['name']})
        elif 'command' in hook:
            view.window().run_command("shell_exec", {"command": hook['command']})

