from boson.code_generator.generator import CodeGenerator
from boson.option import option as boson_option


class JavaCodeGenerator(CodeGenerator):
    def __init__(self, output_path: str, mode: str, checker: bool):
        super().__init__(output_path, 'java', mode, checker)

    def generate_code(self) -> None:
        if self._checker:
            self._generate_code('token.java', boson_option['code']['class_name']['token'] + '.java')
            if self._template_data['option']['generate_lexer']:
                self._generate_code('lexer.java', boson_option['code']['class_name']['lexer'] + '.java')
            if self._template_data['option']['generate_parser']:
                self._generate_code('parser.java', boson_option['code']['class_name']['parser'] + '.java')
        else:
            self._generate_code('token.java', boson_option['code']['class_name']['token'] + '.java')
            if self._template_data['option']['generate_lexer']:
                self._generate_code('lexer.java', boson_option['code']['class_name']['lexer'] + '.java')
            if self._template_data['option']['generate_parser']:
                self._generate_code('grammar_node.java', boson_option['code']['class_name']['grammar_node'] + '.java')
                self._generate_code('grammar.java', boson_option['code']['class_name']['grammar'] + '.java')
                self._generate_code('parser.java', boson_option['code']['class_name']['parser'] + '.java')
            if self._template_data['option']['generate_parser'] and boson_option['code']['generate']['interpreter'] == 'True':
                self._generate_code('semantic_node.java', boson_option['code']['class_name']['semantic_node'] + '.java')
                self._generate_code('interpreter.java', boson_option['code']['class_name']['interpreter'] + '.java')
