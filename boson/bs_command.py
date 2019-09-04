import boson.bs_configure as configure


def bs_command_execute(command_list):
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
        if command in ['start_symbol',
                       'lexical_token_class_name',
                       'grammar_analyzer_class_name',
                       'grammar_class_name',
                       'grammar_node_class_name',
                       'semantics_analyzer_class_name',
                       'generate_semantics_analyzer',
                       'code_comment',
                       'sparse_table',
                       ]:
            configure.boson_option[command] = arguments[0]
        else:
            raise ValueError('Invalid command: %s' % ' '.join(command_line))
