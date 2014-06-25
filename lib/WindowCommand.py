import sublime_plugin
from . import Helper


class WindowCommand(sublime_plugin.WindowCommand):
    def console_view(self):
        try:
            if (self.view_not_exist(self.view())):
                raise AttributeError()
        except AttributeError:
            self.view(self.window.new_file())
            self.view().set_scratch(True)
            self.open_shell(self.view())

        return self.view()

    def view(self, view=None):
        if view:
            self.normal_view = view
        else:
            return self.normal_view

    def open_shell(self, view):
        self.window.run_command('repl_open', {
            "type": "subprocess",
            "encoding": {"windows": "$win_cmd_encoding",
                         "linux": "utf-8",
                         "osx": "utf-8"},
            "cmd": {"windows": ["cmd.exe"],
                    "linux": ["bash", "-i"],
                    "osx": ["bash", "-i"]},
            "cwd": "$file_path",
            "cmd_postfix": "\n",
            "env": {},
            "suppress_echo": True,
            "view_id": view.id(),
            "syntax": "Packages/Text/Plain text.tmLanguage"
        })

    def console(self, text, jump=False):
        view = self.console_view()

        # A hack to make sure bash has exit previous jobs and ready for the next
        view.run_command('repl_enter')
        view.run_command('repl_enter')
        view.run_command('repl_enter')

        view.run_command(
            'update_console_view',
            {"text": text, "jump": jump}
        )
        view.run_command('repl_enter')

    def view_not_exist(self, view):
        return self.window.get_view_index(view)[0] == -1

    def run_command(self, view=None, visible=True):
        self.console(str(self.command))

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
