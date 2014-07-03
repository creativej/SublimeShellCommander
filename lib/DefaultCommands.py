def commands():
    command_lists = []

    command_lists.append(
        new('update commands', 'shell_exec_generate_commands')
    )
    return command_lists


def new(name, command):
    return {
        'caption': 'Shell exec: %s' % (name),
        'command': command,
        'args': {
            'name': name
        }
    }
