import sublime_plugin
from ShellCommander.src import Helper

VIEW_PREFIX = 'SSH'


class AbstractWindow(sublime_plugin.WindowCommand):
    def console_view(self):
        ssh = Helper.plugin_setting('ssh')

        try:
            self.view

            if self.view_not_exist(self.view):
                raise AttributeError()
        except AttributeError:
            self.view = self.window.new_file()
            self.view.set_scratch(True)

            if ssh:
                self.init_ssh(ssh['host'], ssh['user'], self.view)
            else:
                args = {}
                if (self.window.active_group() > self.window.num_groups() - 1):
                    args = {"forward": False}
                self.window.run_command('move_to_neighboring_group', args)
        return self.view

    def init_ssh(self, host, user, view=None):
        ssh_setup = '%s@%s' % (user, host)

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

        self.ssh_command('ssh %s' % (ssh_setup), view, False)

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

    def console(self, text, jump=False):
        self.console_view().run_command(
            'update_console_view',
            {"text": text, "jump": jump}
        )

    def view_not_exist(self, view):
        return self.window.get_view_index(self.view)[0] == -1

    def ssh_command(self, command, view=None, visible=True):
        if not view:
            view = self.console_view()

        if visible:
            self.console('echo "%s: %s"' % (Helper.time(), command), True)
            view.run_command('repl_enter')

        self.console(command)
        view.run_command('repl_enter')
        self.console('echo "Done!"')
        view.run_command('repl_enter')
