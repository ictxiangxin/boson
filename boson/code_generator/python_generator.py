from boson.code_generator.generator import CodeGenerator
import boson.configure as configure


class PythonCodeGenerator(CodeGenerator):
    def __init__(self, output_path: str, mode: str, checker: bool):
        super().__init__(output_path, 'python', mode, checker)

    def generate_code(self):
        if self._checker:
            self._generate_code('__init__.py', '__init__.py')
            self._generate_code('token.py', 'token.py')
            if self._template_data['option']['generate_lexer']:
                self._generate_code('lexer.py', 'lexer.py')
            if self._template_data['option']['generate_parser']:
                self._generate_code('parser.py', 'parser.py')
        else:
            self._generate_code('__init__.py', '__init__.py')
            self._generate_code('token.py', 'token.py')
            if self._template_data['option']['generate_lexer']:
                self._generate_code('lexer.py', 'lexer.py')
            if self._template_data['option']['generate_parser']:
                self._generate_code('grammar_node.py', 'grammar_node.py')
                self._generate_code('grammar.py', 'grammar.py')
                self._generate_code('parser.py', 'parser.py')
            if self._template_data['option']['generate_parser'] and configure.boson_option['generate_interpreter'] == 'yes':
                self._generate_code('semantic_node.py', 'semantic_node.py')
                self._generate_code('interpreter.py', 'interpreter.py')
