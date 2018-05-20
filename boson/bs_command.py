import boson.bs_configure as configure


def bs_command_execute(command_list):
    for command_line in command_list:
        command = command_line[0][1:]
        arguments = command_line[1:]
        if command in ['start_symbol',
                       'grammar_analyzer_class_name',
                       'grammar_class_name',
                       'grammar_node_name',
                       'semantics_analyzer_class_name',
                       'generate_semantics_analyzer',
                       'code_comment',
                       'sparse_table',
                       ]:
            configure.boson_option[command] = arguments[0]
        else:
            raise ValueError('Invalid command: %s' % ' '.join(command_line))
