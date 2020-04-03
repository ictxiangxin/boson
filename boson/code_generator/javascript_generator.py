from boson.code_generator.generator import CodeGenerator
import boson.configure as configure


class JavaScriptCodeGenerator(CodeGenerator):
    def __init__(self, output_path: str, mode: str, checker: bool):
        super().__init__(output_path, 'javascript', mode, checker)

    def generate_code(self):
        if self._checker:
            self._generate_code('token.js', 'token.js')
            if self._template_data['option']['generate_lexer']:
                self._generate_code('lexer.js', 'lexer.js')
            if self._template_data['option']['generate_parser']:
                self._generate_code('parser.js', 'parser.js')
        else:
            self._generate_code('token.js', 'token.js')
            if self._template_data['option']['generate_lexer']:
                self._generate_code('lexer.js', 'lexer.js')
            if self._template_data['option']['generate_parser']:
                self._generate_code('grammar_node.js', 'grammar_node.js')
                self._generate_code('grammar.js', 'grammar.js')
                self._generate_code('parser.js', 'parser.js')
            if self._template_data['option']['generate_parser'] and configure.boson_option['generate_interpreter'] == 'yes':
                self._generate_code('interpreter.js', 'interpreter.js')
