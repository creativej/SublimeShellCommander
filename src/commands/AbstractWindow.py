import sublime_plugin
from ShellCommander.src import Helper

class AbstractWindow(sublime_plugin.WindowCommand):
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

    def console_group(self):
        return self.window.get_view_index(self.console_view())[0]

    def focus_on_console(self):
        view = self.console_view()
        if self.window.active_group() == self.console_group():
            self.window.focus_view(view)
        else:
            previous_view = self.window.active_view()
            self.window.focus_view(view)
            self.window.focus_view(previous_view)

    def console(self, text, jump = False):
        self.console_view().run_command(
            'update_console_view',
            {"text": text + '\n', "jump": jump}
        )

    def view_not_exist(self, view):
        return self.window.get_view_index(self.view)[0] == -1

