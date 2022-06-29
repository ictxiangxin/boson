from boson.code_generator.generator import CodeGenerator
from boson.option import option as boson_option
from boson.system.logger import logger


class JavaScriptCodeGenerator(CodeGenerator):
    def __init__(self, output_path: str, mode: str, checker: bool):
        super().__init__(output_path, 'javascript', mode, checker)

    def generate_code(self) -> None:
        logger.info('[JavaScript Code Generator] Generate Code.')
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
            if self._template_data['option']['generate_parser'] and boson_option['code']['generator']['interpreter'] == 'True':
                self._generate_code('semantic_node.js', 'semantic_node.js')
                self._generate_code('interpreter.js', 'interpreter.js')
