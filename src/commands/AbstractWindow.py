import sublime_plugin
from ShellCommander.src import Helper

VIEW_PREFIX = 'SSH'


class AbstractWindow(sublime_plugin.WindowCommand):
    def console_view(self):
        try:
            if (self.view_not_exist(self.view())):
                raise AttributeError()
        except AttributeError:
            self.ssh_initiated = False
            self.view(self.window.new_file())
            self.view().set_scratch(True)
            self.open_shell(self.view())

        return self.view()

    def view(self, view=None):
        if self.command.is_ssh:
            if view:
                self.ssh_view = view
            else:
                return self.ssh_view
        else:
            if view:
                self.normal_view = view
            else:
                return self.normal_view

    def init_ssh(self):
        ssh = Helper.plugin_setting('ssh')
        if ssh:
            self.console('ssh %s@%s' % (ssh['user'], ssh['host']), False)
            self.ssh_initiated = True
        else:
            print("Can't connect to ssh because no detail is specified.")

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
        view.run_command(
            'update_console_view',
            {"text": text, "jump": jump}
        )
        view.run_command('repl_enter')

    def view_not_exist(self, view):
        return self.window.get_view_index(view)[0] == -1

    def run_command(self, view=None, visible=True):
        if not view:
            view = self.console_view()

        if self.command.is_ssh:
            if not self.ssh_initiated:
                self.init_ssh()

            if visible:
                self.console('echo "%s: %s"' % (Helper.time(), self.command), True)

        self.console(str(self.command))

        if self.command.is_ssh:
            self.console('echo Done!')

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
