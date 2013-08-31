def commands():
    list = []

    list.append(
        sublime_command('update commands', 'shell_commander_generate_commands')
    )
    return list


def command(name, command):
    return {
        'caption': 'Shell Commander: %s' % (name),
        'command': command,
        'args': {
            'name': name
        }
    }
