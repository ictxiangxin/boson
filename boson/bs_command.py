import boson.bs_configure as configure

option_list = list(configure.boson_option)


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
        if command in option_list:
            configure.boson_option[command] = arguments[0]
        else:
            raise ValueError('Invalid command: %s' % ' '.join(command_line))
