import os.path
from typing import Any, Dict

from jinja2 import Environment, PackageLoader, Template

import boson.configure as configure
from boson.lexer_generator.generator import LexerGenerator
from boson.option import option as boson_option
from boson.parser_generator.bottom_up_generator.canonical_generator import BottomUpCanonicalParserGenerator
from boson.system.logger import logger


class CodeGenerator:
    def __init__(self, output_path: str, language: str, mode: str, checker: bool):
        self._output_path: str = output_path
        self._language: str = language
        self._mode: str = mode
        self._checker: bool = checker
        self.__environment: Environment = Environment(
            loader=PackageLoader(
                configure.boson_package_name,
                os.path.join(configure.boson_template_directory, self._mode, self._language, 'checker' if self._checker else ''),
                encoding=configure.boson_default_encoding))
        self._template_data: Dict[str, Any] = {
            'configure': configure,
            'boson_code_option': boson_option['code'],
            'option': {
                'generate_lexer': False,
                'generate_parser': False,
            },
            'lexer': None,
            'parser': None,
        }

    def _generate_code(self, template_file: str, output_file: str) -> None:
        template: Template = self.__environment.get_template(template_file + configure.boson_template_postfix)
        code_text: str = template.render(self._template_data)
        with open(os.path.join(self._output_path, output_file), 'w', encoding=configure.boson_default_encoding) as code_file:
            code_file.write(code_text)

    def dispose_lexer(self, lexer_generator: LexerGenerator) -> None:
        logger.info('[Code Generator] Dispose Lexer.')
        self._template_data['option']['generate_lexer'] = True
        self._template_data['lexer'] = {
            'move_table': lexer_generator.move_table(),
            'compact_move_table': lexer_generator.compact_move_table(),
            'symbol_function_mapping': lexer_generator.symbol_function_mapping(),
            'non_greedy_state_set': lexer_generator.non_greedy_state_set(),
            'character_set': lexer_generator.character_set(),
            'start_state': lexer_generator.start_state(),
            'end_state_set': lexer_generator.end_state_set(),
            'lexical_symbol_mapping': lexer_generator.lexical_symbol_mapping(),
        }

    def dispose_parser(self, parser_generator):
        logger.info('[Code Generator] Dispose Parser.')
        self._template_data['option']['generate_parser'] = True
        if isinstance(parser_generator, BottomUpCanonicalParserGenerator):
            self._template_data['parser'] = {
                'terminal_index_mapping': parser_generator.terminal_index_mapping(),
                'action_table': parser_generator.action_table(),
                'sparse_action_table': parser_generator.sparse_action_table(),
                'goto_table': parser_generator.goto_table(),
                'sparse_goto_table': parser_generator.sparse_goto_table(),
                'sentence_index_grammar_tuple_mapping': parser_generator.sentence_index_grammar_tuple_mapping(),
                'reduce_symbol_count': parser_generator.reduce_symbol_count(),
                'reduce_non_terminal_index': parser_generator.reduce_non_terminal_index(),
                'none_grammar_tuple_sentence_index_set': parser_generator.none_grammar_tuple_sentence_index_set(),
                'reduce_number_grammar_name_mapping': parser_generator.reduce_number_grammar_name_mapping(),
                'naive_reduce_number_set': parser_generator.naive_reduce_number_set(),
            }
        else:
            raise ValueError(f'[Code Generator] Invalid Parser Generator Type: "{type(parser_generator)}".')
