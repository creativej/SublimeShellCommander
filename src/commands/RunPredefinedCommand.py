import sublime_plugin
from ShellCommander.src import Helper
from ShellCommander.src.CommandThread import CommandThread
from .AbstractWindow import AbstractWindow

class ShellCommanderRunPredefinedCommand(AbstractWindow):
    def run(self, **args):
        if 'name' in args:
            command = Helper.plugin_setting('commands')[args['name']]
        elif 'command' in args:
            command = args['command']
        else:
            return

        params = Helper.parameters(self)

        for key in params:
            if params[key]:
                command = command.replace('{{' + key + '}}', params[key])

        self.focus_on_console()
        self.console(
            '%s $: %s' % (Helper.time(), command),
            True
        )
        CommandThread(command).done(self.console).start()
