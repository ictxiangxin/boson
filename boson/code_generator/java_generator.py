import boson.configure as configure
from boson.code_generator.generator import CodeGenerator


class JavaCodeGenerator(CodeGenerator):
    def __init__(self, output_path: str, mode: str, checker: bool):
        super().__init__(output_path, 'java', mode, checker)

    def generate_code(self) -> None:
        if self._checker:
            self._generate_code('token.java', configure.boson_option['token_class_name'] + '.java')
            if self._template_data['option']['generate_lexer']:
                self._generate_code('lexer.java', configure.boson_option['lexer_class_name'] + '.java')
            if self._template_data['option']['generate_parser']:
                self._generate_code('parser.java', configure.boson_option['parser_class_name'] + '.java')
        else:
            self._generate_code('token.java', configure.boson_option['token_class_name'] + '.java')
            if self._template_data['option']['generate_lexer']:
                self._generate_code('lexer.java', configure.boson_option['lexer_class_name'] + '.java')
            if self._template_data['option']['generate_parser']:
                self._generate_code('grammar_node.java', configure.boson_option['grammar_node_class_name'] + '.java')
                self._generate_code('grammar.java', configure.boson_option['grammar_class_name'] + '.java')
                self._generate_code('parser.java', configure.boson_option['parser_class_name'] + '.java')
            if self._template_data['option']['generate_parser'] and configure.boson_option['generate_interpreter'] == 'yes':
                self._generate_code('semantic_node.java', configure.boson_option['semantic_node_class_name'] + '.java')
                self._generate_code('interpreter.java', configure.boson_option['interpreter_class_name'] + '.java')
