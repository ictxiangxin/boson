import boson.bs_configure as configure


def bs_command_execute(command_list: list):
    for command_line in command_list:
        origin_command = command_line[0][1:]
        arguments = command_line[1:]
        command = ''
        for c in origin_command:
            prefix = ''
            if len(command) != 0 and command[-1] != '_':
                prefix = '_'
            if c.isupper():
                command += prefix + c.lower()
            else:
                command += c
        if command in configure.boson_option:
            option_value = arguments[0]
            value_enumeration = configure.boson_option_enumeration[command]
            if value_enumeration is None or option_value in value_enumeration:
                configure.boson_option[command] = arguments[0]
            else:
                raise ValueError('Command "{}" can only be {}'.format(command, value_enumeration))
        else:
            raise ValueError('Invalid command: %s' % ' '.join(command_line))
