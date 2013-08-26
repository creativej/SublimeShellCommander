import sublime_plugin
import inspect
from ShellCommander.src import Helper


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
