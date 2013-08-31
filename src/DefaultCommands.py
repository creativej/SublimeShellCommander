def commands():
    list = []

    list.append(
        new('update commands', 'shell_commander_generate_commands')
    )
    return list


def new(name, command):
    return {
        'caption': 'Shell Commander: %s' % (name),
        'command': command,
        'args': {
            'name': name
        }
    }
