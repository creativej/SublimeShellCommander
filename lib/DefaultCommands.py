def commands():
    list = []

    list.append(
        new('update commands', 'shell_exec_generate_commands')
    )
    return list


def new(name, command):
    return {
        'caption': 'Shell exec: %s' % (name),
        'command': command,
        'args': {
            'name': name
        }
    }
