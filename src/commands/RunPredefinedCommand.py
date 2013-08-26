from ShellCommander.src.Command import Command
from ShellCommander.src import Helper
from .AbstractWindow import AbstractWindow


class ShellCommanderRunPredefinedCommand(AbstractWindow):
    def run(self, **args):
        command = Command.from_args(args, Helper.params(self))

        if not command:
            return

        self.command = command
        self.focus_on_console()
        self.run_command()
