from boson.code_generator.generator import CodeGenerator
from boson.option import option as boson_option


class CppCodeGenerator(CodeGenerator):
    def __init__(self, output_path: str, mode: str, checker: bool):
        super().__init__(output_path, 'c++', mode, checker)

    def generate_code(self) -> None:
        if self._checker:
            self._generate_code('boson.hpp', 'boson.hpp')
            self._generate_code('token.hpp', 'token.hpp')
            if self._template_data['option']['generate_lexer']:
                self._generate_code('lexer.hpp', 'lexer.hpp')
            if self._template_data['option']['generate_parser']:
                self._generate_code('parser.hpp', 'parser.hpp')
        else:
            self._generate_code('boson.hpp', 'boson.hpp')
            self._generate_code('token.hpp', 'token.hpp')
            if self._template_data['option']['generate_lexer']:
                self._generate_code('lexer.hpp', 'lexer.hpp')
            if self._template_data['option']['generate_parser']:
                self._generate_code('grammar_node.hpp', 'grammar_node.hpp')
                self._generate_code('grammar.hpp', 'grammar.hpp')
                self._generate_code('parser.hpp', 'parser.hpp')
            if self._template_data['option']['generate_parser'] and boson_option['code']['generate']['interpreter'] == 'True':
                self._generate_code('semantic_node.hpp', 'semantic_node.hpp')
                self._generate_code('interpreter.hpp', 'interpreter.hpp')
