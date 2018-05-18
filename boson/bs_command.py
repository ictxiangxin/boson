import boson.bs_configure as configure


def bs_command_true_or_false(bool_string):
    bool_string = bool_string.lower()
    if bool_string == 'true':
        return True
    elif bool_string == 'false':
        return False
    else:
        raise ValueError('Invalid boolean boson_option: %s' % bool_string)


def bs_command_execute(command_list):
    for command_line in command_list:
        command = command_line[0][1:]
        arguments = command_line[1:]
        if command == 'start_symbol':
            configure.boson_option['start_symbol'] = arguments[0]
        elif command == 'analyzer_class_name':
            configure.boson_option['analyzer_class_name'] = arguments[0]
        elif command == 'grammar_class_name':
            configure.boson_option['grammar_class_name'] = arguments[0]
        else:
            raise ValueError('Invalid command: %s' % ' '.join(command))
