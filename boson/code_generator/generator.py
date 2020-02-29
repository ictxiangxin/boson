import jinja2
from boson.lexer_generator.generator import LexerGenerator
from boson.parser_generator.bottom_up_generator.canonical_generator import BottomUpCanonicalParserGenerator
import boson.configure as configure


class CodeGenerator:
    def __init__(self, language: str):
        self.__language: str = language
        self.__template_data: dict = {
            'configure': configure,
            'option': {
                'generate_lexer': False,
                'generate_parser': False,
            },
            'lexer': None,
            'parser': None,
        }

    def dispose_lexer(self, lexer_generator: LexerGenerator) -> None:
        self.__template_data['option']['generate_lexer'] = True
        self.__template_data['lexer'] = {
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
        self.__template_data['option']['generate_parser'] = True
        if isinstance(parser_generator, BottomUpCanonicalParserGenerator):
            self.__template_data['parser'] = {
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
            raise ValueError('[Code Generator] Invalid Parser Generator Type: "{}".'.format(type(parser_generator)))

    def generate_code(self) -> str:
        environment = jinja2.Environment(loader=jinja2.PackageLoader(configure.boson_package_name, configure.boson_template_directory))
        template = environment.get_template(self.__language + configure.boson_template_postfix)
        return template.render(self.__template_data)
