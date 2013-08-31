from ShellCommander.src import Helper

SSH_PREFIX = 'ssh:'


class Command:
    @classmethod
    def from_args(cls, args, params):
        if 'name' in args:
            commands = Helper.plugin_setting('commands')
            name = args['name']

            if commands and name in commands:
                return cls(commands[name], params)
            else:
                return
        elif 'command' in args:
            return cls(args['command'], params)
        else:
            return

    def __init__(self, command, params):
        if isinstance(command, dict):
            if 'desc' in command:
                self.desc = command['desc']

            command = command['command']

        self.is_ssh = (command.find('ssh:') == 0)
        self.command = self.extract_command(command, params)

    def extract_command(self, command, params):
        command = command.replace('ssh:', '').strip()

        for key in params:
            if params[key]:
                command = command.replace('{{' + key + '}}', params[key])

        return command

    def __str__(self):
        return self.command
