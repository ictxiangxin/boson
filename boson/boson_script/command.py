from typing import Dict

from boson.option import option
from boson.system.logger import logger


class CommandExecutor:
    def __init__(self):
        self.__boson_option_template: Dict[str, str | dict] = {
            'mode': (str, ('integration', 'table', 'library', 'binary')),
            'parser': {
                'start_symbol': (str, None),
                'analyzer': (str, ('slr', 'lr', 'lalr')),
                'conflict_resolver': {
                    'enable': (str, ('True', 'False')),
                    'shift_reduce': (str, ('order', 'shift', 'reduce')),
                    'reduce_reduce': (str, ('order', 'long', 'short')),
                },
            },
            'code': {
                'checker': (str, ('True', 'False')),
                'language': (str, ('python', 'c++', 'java', 'javascript')),
                'generator': {
                    'lexer': (str, ('True', 'False')),
                    'interpreter': (str, ('True', 'False')),
                    'comment': (str, ('True', 'False')),
                },
                'lexer': {
                    'unicode': (str, ('True', 'False')),
                    'compact_table': (str, ('True', 'False')),
                },
                'parser': {
                    'sparse_table': (str, ('True', 'False')),
                },
                'class_name': {
                    'token': (str, None),
                    'lexer': (str, None),
                    'parser': (str, None),
                    'grammar': (str, None),
                    'grammar_node': (str, None),
                    'interpreter': (str, None),
                    'semantic_node': (str, None),
                }
            }
        }
        self.__split_symbol = '_'

    def set_option(self, option_user: Dict[str, str | list | dict], option_system: Dict[str, str | list | dict], option_template: Dict[str, str | dict]):
        for key, value in option_user.items():
            if key in option_template:
                if isinstance(option_template[key], dict):
                    if not isinstance(value, dict):
                        raise ValueError(f'Option Type Invalid: Key={key}, Type={type(value).__name__}, ExpectType=dict')
                    self.set_option(value, option_system[key], option_template[key])
                else:
                    expect_type, rule = option_template[key]
                    if expect_type == str:
                        if not isinstance(value, str):
                            raise ValueError(f'Option Type Invalid: Key={key}, Type={type(value).__name__}, ExpectType=str')
                        if rule is not None and value not in rule:
                            raise ValueError(f'Option Value Invalid: Key={key}, Value={value}, ExpectValue={rule}')
                        option_system[key] = value
                    else:
                        raise RuntimeError('[Boson Option] Never Touch Here.')
            else:
                raise ValueError(f'Option Key Invalid: Key={key}, ExpectKey={list(option_template.keys())}')

    def execute(self, command_list: list) -> None:
        logger.info('[Boson Command] Execute Command.')
        for command_line in command_list:
            command = command_line[0][1:]
            match command:
                case 'option':
                    option_user: Dict[str, str | list | dict] = command_line[1][0]
                    self.set_option(option_user, option, self.__boson_option_template)
                case _:
                    raise ValueError(f'Invalid command: {command}')
