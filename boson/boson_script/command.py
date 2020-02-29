import boson.configure as configure


class CommandExecutor:
    def __init__(self):
        self.__boson_option_enumeration = {
            'start_symbol': None,
            'lexical_token_class_name': None,
            'lexical_analyzer_class_name': None,
            'grammar_analyzer_class_name': None,
            'grammar_class_name': None,
            'grammar_node_class_name': None,
            'semantics_analyzer_class_name': None,
            'semantics_node_class_name': None,
            'generate_semantics_analyzer': {'yes', 'no'},
            'generate_lexical_analyzer': {'yes', 'no'},
            'code_comment': {'yes', 'no'},
            'sparse_table': {'yes', 'no'},
            'conflict_resolver': {'yes', 'no'},
            'shift_reduce_conflict_resolver': {'shift', 'reduce'},
            'reduce_reduce_conflict_resolver': {'long', 'short'},
        }
        self.__split_symbol = '_'

    def normalize_command(self, origin_command: str) -> str:
        command = ''
        for c in origin_command:
            prefix = ''
            if len(command) != 0 and command[-1] != self.__split_symbol:
                prefix = self.__split_symbol
            if c.isupper():
                command += prefix + c.lower()
            else:
                command += c
        return command

    def execute(self, command_list: list) -> None:
        for command_line in command_list:
            command = self.normalize_command(command_line[0][1:])
            if command in configure.boson_option:
                option_value = command_line[1:][0][0]
                value_enumeration = self.__boson_option_enumeration[command]
                if value_enumeration is None or option_value in value_enumeration:
                    configure.boson_option[command] = option_value
                else:
                    raise ValueError('[Command Executor] Command "{}" can only be {}'.format(command, value_enumeration))
            else:
                raise ValueError('Invalid command: %s' % ' '.join(command_line))
