import boson.configure as configure
from boson.boson_script.boson_script_parser import \
    BosonGrammarNode, \
    BosonLexer, \
    BosonParser, \
    BosonInterpreter, \
    BosonSemanticsNode


interpreter = BosonInterpreter()


def get_semantic_node_text_list(semantic_node: BosonSemanticsNode) -> list:
    return [node.get_text() for node in semantic_node.children()]


def get_semantic_node_data_list(semantic_node: BosonSemanticsNode) -> list:
    return [node.get_data() for node in semantic_node.children()]


class BosonScriptAnalyzer:
    def __init__(self):
        self.__parser: BosonParser = BosonParser()
        self.__sentence_set: set = set()
        self.__sentence_grammar_tuple_mapping: dict = {}
        self.__none_grammar_tuple_set: set = set()
        self.__command_list: list = []
        self.__literal_map: dict = {}
        self.__literal_reverse_map: dict = {}
        self.__sentence_grammar_name_mapping: dict = {}
        self.__naive_sentence_set: set = set()
        self.__literal_number: int = 1
        self.__hidden_name_number: int = 0
        self.__grammar_number: int = 0
        self.__lexical_definition: dict = {}
        self.__lexical_number: int = 0
        self.__hidden_derivation_cache: dict = {}
        self.__positive_closure_cache: dict = {}
        self.__colin_closure_cache: dict = {}
        self.__optional_cache: dict = {}

    def __generate_hidden_name(self, prefix: str = configure.boson_hidden_name_prefix) -> str:
        hidden_name = '{}{}'.format(prefix, self.__hidden_name_number)
        self.__hidden_name_number += 1
        return hidden_name

    def __sentence_add(self, sentence: tuple, grammar_tuple: tuple = None) -> None:
        self.__sentence_set.add(sentence)
        if grammar_tuple is None:
            self.__none_grammar_tuple_set.add(sentence)
        else:
            self.__sentence_grammar_tuple_mapping[sentence] = grammar_tuple

    def __add_positive_closure(self, name: str) -> str:
        if name in self.__positive_closure_cache:
            return self.__positive_closure_cache[name]
        else:
            hidden_name = self.__generate_hidden_name(configure.boson_operator_name_prefix)
            self.__positive_closure_cache[name] = hidden_name
            self.__sentence_add((hidden_name, hidden_name, name), ('{}0'.format(configure.boson_grammar_tuple_unpack), '1'))
            self.__sentence_add((hidden_name, name))
            return hidden_name

    def __add_colin_closure(self, name: str) -> str:
        if name in self.__colin_closure_cache:
            return self.__colin_closure_cache[name]
        else:
            hidden_name = self.__generate_hidden_name(configure.boson_operator_name_prefix)
            self.__colin_closure_cache[name] = hidden_name
            self.__sentence_add((hidden_name, hidden_name, name), ('{}0'.format(configure.boson_grammar_tuple_unpack), '1'))
            self.__sentence_add((hidden_name, configure.boson_null_symbol), tuple())
            return hidden_name

    def __add_optional(self, name: str) -> str:
        if name in self.__optional_cache:
            return self.__optional_cache[name]
        else:
            hidden_name = self.__generate_hidden_name(configure.boson_operator_name_prefix)
            self.__optional_cache[name] = hidden_name
            self.__sentence_add((hidden_name, name), ('{}0'.format(configure.boson_grammar_tuple_unpack),))
            self.__sentence_add((hidden_name, configure.boson_null_symbol), tuple())
            return hidden_name

    def __add_select(self, sentence_list: list) -> str:
        hidden_name = self.__generate_hidden_name()
        for sentence in sentence_list:
            select_sentence = (hidden_name,) + tuple(sentence)
            self.__sentence_add(select_sentence)
            self.__naive_sentence_set.add(select_sentence)
        return hidden_name

    def __add_hidden_derivation(self, derivation: list) -> str:
        derivation_tuple = tuple(derivation)
        if derivation_tuple in self.__hidden_derivation_cache:
            return self.__hidden_derivation_cache[derivation_tuple]
        else:
            hidden_name = self.__generate_hidden_name()
            self.__hidden_derivation_cache[derivation_tuple] = hidden_name
            self.__sentence_add((hidden_name,) + tuple(derivation))
            return hidden_name

    def command_list(self):
        return self.__command_list

    def lexical_definition(self):
        return self.__lexical_definition

    def sentence_set(self):
        return self.__sentence_set

    def sentence_grammar_tuple_mapping(self):
        return self.__sentence_grammar_tuple_mapping

    def none_grammar_tuple_set(self):
        return self.__none_grammar_tuple_set

    def literal_map(self):
        return self.__literal_map

    def literal_reverse_map(self):
        return self.__literal_reverse_map

    def sentence_grammar_name_mapping(self):
        return self.__sentence_grammar_name_mapping

    def naive_sentence_set(self):
        return self.__naive_sentence_set

    def init_semantic(self):
        @interpreter.register_action('command')
        def _semantic_command(semantic_node) -> BosonSemanticsNode:
            command_name = semantic_node[0].get_text()
            command_arguments = get_semantic_node_text_list(semantic_node[1])
            self.__command_list.append([command_name, command_arguments])
            return BosonSemanticsNode.null_node()

        @interpreter.register_action('lexical_define')
        def _semantic_lexical_define(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            lexical_name = semantic_node[0].get_text()
            definition = {
                'regular': semantic_node[1].get_text()[1:-1],
                'number': self.__lexical_number
            }
            self.__lexical_number += 1
            if len(semantic_node.children()) == 4:
                function_index = 3
                definition['non_greedy'] = semantic_node[2].get_text() == configure.boson_lexical_non_greedy_sign
            else:
                function_index = 2
                definition['non_greedy'] = False
            definition['function_list'] = get_semantic_node_text_list(semantic_node[function_index])
            self.__lexical_definition[lexical_name] = definition
            return BosonSemanticsNode.null_node()

        @interpreter.register_action('reduce')
        def _semantic_reduce(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            reduce_name = semantic_node[0].get_text()
            derivation_list = semantic_node[1]
            for derivation in derivation_list.children():
                derivation_body = derivation[0]
                if len(derivation_body.children()) == 0 and not derivation_body.is_null():
                    sentence = (reduce_name, derivation_body.get_text())
                elif len(derivation_body.children()) > 0:
                    sentence = (reduce_name,) + tuple(get_semantic_node_text_list(derivation_body))
                else:
                    sentence = (reduce_name, configure.boson_null_symbol)
                self.__sentence_set.add(sentence)
                if len(sentence) == 2:
                    for i in range(2):
                        if sentence[i].startswith(configure.boson_operator_name_prefix) or sentence[i].startswith(configure.boson_hidden_name_prefix):
                            break
                    else:
                        self.__naive_sentence_set.add(sentence)
                if len(derivation.children()) == 1:
                    self.__none_grammar_tuple_set.add(sentence)
                elif len(derivation.children()) == 2:
                    self.__sentence_grammar_tuple_mapping[sentence] = tuple(get_semantic_node_data_list(derivation[1]))
                elif len(derivation.children()) == 3:
                    self.__sentence_grammar_name_mapping[sentence] = derivation[1].get_text()
                    self.__sentence_grammar_tuple_mapping[sentence] = tuple(get_semantic_node_data_list(derivation[2]))
                else:
                    raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
                self.__grammar_number += 1
            return BosonSemanticsNode.null_node()

        @interpreter.register_action('name_closure')
        def _semantic_name_closure(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            name = semantic_node[0].get_text()
            if len(semantic_node.children()) == 2:
                if semantic_node[1].get_text() == '+':
                    name = self.__add_positive_closure(name)
                elif semantic_node[1].get_text() == '*':
                    name = self.__add_colin_closure(name)
                else:
                    raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
            name_closure_node = BosonSemanticsNode()
            name_closure_node.set_text(name)
            return name_closure_node

        @interpreter.register_action('complex_closure')
        def _semantic_complex_closure(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            name = self.__add_hidden_derivation(get_semantic_node_text_list(semantic_node[0]))
            if len(semantic_node.children()) == 2:
                closure = semantic_node[1].get_text()
                if closure == '+':
                    name = self.__add_positive_closure(name)
                elif closure == '*':
                    name = self.__add_colin_closure(name)
                else:
                    raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
            complex_closure_node = BosonSemanticsNode()
            complex_closure_node.set_text(name)
            return complex_closure_node

        @interpreter.register_action('complex_optional')
        def _semantic_complex_optional(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            complex_optional_node = BosonSemanticsNode()
            complex_optional_node.set_text(self.__add_optional(self.__add_hidden_derivation(get_semantic_node_text_list(semantic_node[0]))))
            return complex_optional_node

        @interpreter.register_action('select')
        def _semantic_select(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            select_node = BosonSemanticsNode()
            select_node.set_text(self.__add_select([get_semantic_node_text_list(node) for node in semantic_node.children()]))
            sentence_node = BosonSemanticsNode()
            sentence_node.append(select_node)
            return sentence_node

        @interpreter.register_action('getter_tuple')
        def _semantic_getter_tuple(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            getter_node = BosonSemanticsNode()
            getter_node.append(BosonSemanticsNode(configure.boson_grammar_tuple_unpack))
            getter_node.append(BosonSemanticsNode(semantic_node[0].get_text()[1:]))
            return getter_node

        @interpreter.register_action('grammar_node')
        def _semantic_grammar_node(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            if len(semantic_node.children()) == 1:
                grammar_node = semantic_node[0].get_text()[1:]
            elif len(semantic_node.children()) == 2:
                if semantic_node[0].get_text() == configure.boson_grammar_tuple_unpack:
                    grammar_node = semantic_node[0].get_text() + semantic_node[1].get_text()[1:]
                else:
                    grammar_node = (semantic_node[0].get_text()[1:], tuple(get_semantic_node_data_list(semantic_node[1])))
            elif len(semantic_node.children()) == 3:
                if semantic_node[0].get_text() == configure.boson_grammar_tuple_unpack:
                    grammar_node = (semantic_node[0].get_text() + semantic_node[1].get_text()[1:], tuple(get_semantic_node_data_list(semantic_node[2])))
                else:
                    grammar_node = (semantic_node[0].get_text()[1:], (semantic_node[1].get_text(),) + tuple(get_semantic_node_data_list(semantic_node[2])))
            elif len(semantic_node.children()) == 4:
                grammar_node = (semantic_node[0].get_text() + semantic_node[1].get_text()[1:], (semantic_node[2].get_text(),) + tuple(get_semantic_node_data_list(semantic_node[3])))
            else:
                raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
            return BosonSemanticsNode(grammar_node)

        @interpreter.register_action('literal')
        def _semantic_literal(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            literal_string = semantic_node[0].get_text()[1: -1]
            if literal_string in self.__literal_map:
                literal_symbol = self.__literal_map[literal_string]
            else:
                literal_symbol = configure.boson_symbol_template.format(self.__literal_number)
                self.__literal_number += 1
                self.__literal_map[literal_string] = literal_symbol
                self.__literal_reverse_map[literal_symbol] = literal_string
                self.__lexical_definition[literal_symbol] = {
                    'regular': '\\' + '\\'.join(literal_string),
                    'non_greedy': False,
                    'function_list': None
                }
            literal_node = BosonSemanticsNode()
            literal_node.set_text(literal_symbol)
            return literal_node

    def parse(self, token_list: list) -> BosonGrammarNode:
        grammar = self.__parser.parse(token_list)
        if grammar.error_index == grammar.no_error_index():
            return grammar.grammar_tree
        else:
            start_index = end_index = grammar.error_index
            error_line = token_list[grammar.error_index].line
            while start_index >= 0:
                if token_list[start_index].line == error_line:
                    start_index -= 1
                    continue
                else:
                    break
            while end_index < len(token_list):
                if token_list[end_index].line == error_line:
                    end_index += 1
                    continue
                else:
                    break
            offset = grammar.error_index - start_index - 1
            error_token_list = token_list[start_index + 1: end_index]
            error_message = '\n[Boson Script Analyzer] Syntax Error <Line: {}>\n'.format(error_line)
            error_token_text_list = [token.text for token in error_token_list]
            error_message += '{}\n'.format(' '.join(error_token_text_list))
            error_message += ' ' * (sum([len(text) for text in error_token_text_list[:offset]]) + offset) + '^' * len(error_token_text_list[offset])
            raise ValueError(error_message)

    def tokenize_and_parse(self, boson_script_text: str):
        lexer = BosonLexer()
        if lexer.tokenize(boson_script_text) != lexer.no_error_index():
            raise ValueError('[Boson Script Analyzer] Invalid Token [Line: {}, Index: {}]'.format(lexer.line(), lexer.error_index()))
        self.__init__()
        self.init_semantic()
        interpreter.execute(self.parse(lexer.token_list()))
