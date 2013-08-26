from ShellCommander.src import Helper
from ShellCommander.src.CommandThread import CommandThread
from .AbstractWindow import AbstractWindow


class ShellCommanderRunPredefinedCommand(AbstractWindow):
    def run(self, **args):
        if 'name' in args:
            commands = Helper.plugin_setting('commands')
            name = args['name']

            if commands and name in commands:
                command = commands[name]
            else:
                return
        elif 'command' in args:
            command = args['command']
        else:
            return

        params = Helper.parameters(self)

        for key in params:
            if params[key]:
                command = command.replace('{{' + key + '}}', params[key])

        self.focus_on_console()

        if Helper.plugin_setting('ssh'):
            self.ssh_command(command)
        else:
            CommandThread(command).done(self.console).start()
