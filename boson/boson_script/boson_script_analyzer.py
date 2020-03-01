import boson.configure as configure
from boson.boson_script.boson_script_parser import BosonGrammarNode, BosonLexer, BosonParser, BosonInterpreter


interpreter = BosonInterpreter()


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
        hidden_name = self.__generate_hidden_name(configure.boson_operator_name_prefix)
        self.__sentence_add((hidden_name, hidden_name, name), ('{}0'.format(configure.boson_grammar_tuple_unpack), '1'))
        self.__sentence_add((hidden_name, name))
        return hidden_name

    def __add_colin_closure(self, name: str) -> str:
        hidden_name = self.__generate_hidden_name(configure.boson_operator_name_prefix)
        self.__sentence_add((hidden_name, hidden_name, name), ('{}0'.format(configure.boson_grammar_tuple_unpack), '1'))
        self.__sentence_add((hidden_name, configure.boson_null_symbol), tuple())
        return hidden_name

    def __add_optional(self, name: str) -> str:
        hidden_name = self.__generate_hidden_name(configure.boson_operator_name_prefix)
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
        hidden_name = self.__generate_hidden_name()
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
        def _semantic_command(semantic_node_list):
            self.__command_list.append(semantic_node_list)

        @interpreter.register_action('lexical_define')
        def _semantic_lexical_define(semantic_node_list):
            semantic_node_list[1] = semantic_node_list[1][1:-1]
            self.__lexical_definition[semantic_node_list[0]] = semantic_node_list[1:]

        @interpreter.register_action('regular_expression')
        def _semantic_regular_expression(semantic_node_list):
            return [semantic_node_list[0][1:-1], semantic_node_list[1] if len(semantic_node_list) > 1 else []]

        @interpreter.register_action('reduce')
        def _semantic_reduce(semantic_node_list):
            reduce_name = semantic_node_list[0]
            derivation_list = semantic_node_list[1]
            for derivation in derivation_list:
                derivation_body = derivation[0]
                if isinstance(derivation_body, str):
                    sentence = (reduce_name, derivation_body)
                elif isinstance(derivation_body, list):
                    sentence = tuple([reduce_name] + derivation_body)
                else:
                    sentence = (reduce_name, configure.boson_null_symbol)
                self.__sentence_set.add(sentence)
                if len(sentence) == 1:
                    self.__naive_sentence_set.add(sentence)
                if len(sentence) == 2:
                    for i in range(2):
                        if sentence[i].startswith(configure.boson_operator_name_prefix) or sentence[i].startswith(configure.boson_hidden_name_prefix):
                            break
                    else:
                        self.__naive_sentence_set.add(sentence)
                if len(derivation) == 1:
                    self.__none_grammar_tuple_set.add(sentence)
                elif len(derivation) == 2:
                    self.__sentence_grammar_tuple_mapping[sentence] = tuple(derivation[1])
                elif len(derivation) == 3:
                    self.__sentence_grammar_tuple_mapping[sentence] = tuple(derivation[2])
                    self.__sentence_grammar_name_mapping[sentence] = derivation[1]
                else:
                    raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
                self.__grammar_number += 1

        @interpreter.register_action('name_closure')
        def _semantic_name_closure(semantic_node_list):
            name = semantic_node_list[0]
            if len(semantic_node_list) == 2:
                if semantic_node_list[1] == '+':
                    name = self.__add_positive_closure(name)
                elif semantic_node_list[1] == '*':
                    name = self.__add_colin_closure(name)
                else:
                    raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
            return name

        @interpreter.register_action('complex_closure')
        def _semantic_complex_closure(semantic_node_list):
            name = self.__add_hidden_derivation(semantic_node_list[0])
            if len(semantic_node_list) == 2:
                closure = semantic_node_list[1][0]
                if closure == '+':
                    name = self.__add_positive_closure(name)
                elif closure == '*':
                    name = self.__add_colin_closure(name)
                else:
                    raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
            return name

        @interpreter.register_action('complex_optional')
        def _semantic_complex_optional(semantic_node_list):
            return self.__add_optional(self.__add_hidden_derivation(semantic_node_list[0]))

        @interpreter.register_action('select')
        def _semantic_select(semantic_node_list):
            return [self.__add_select(semantic_node_list)]

        @interpreter.register_action('grammar_node')
        def _semantic_grammar_node(semantic_node_list):
            if len(semantic_node_list) == 1:
                return semantic_node_list[0][1:]
            elif len(semantic_node_list) == 2:
                if semantic_node_list[0] == configure.boson_grammar_tuple_unpack:
                    return semantic_node_list[0] + semantic_node_list[1][1:]
                else:
                    return semantic_node_list[0][1:], tuple(semantic_node_list[1])
            elif len(semantic_node_list) == 3:
                if semantic_node_list[0] == configure.boson_grammar_tuple_unpack:
                    return semantic_node_list[0] + semantic_node_list[1][1:], tuple(semantic_node_list[2])
                else:
                    return semantic_node_list[0], (semantic_node_list[1],) + tuple(semantic_node_list[2])
            elif len(semantic_node_list) == 4:
                return semantic_node_list[0] + semantic_node_list[1][1:], (semantic_node_list[2],) + tuple(semantic_node_list[3])
            else:
                raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')

        @interpreter.register_action('literal')
        def _semantic_literal(semantic_node_list):
            literal_string = semantic_node_list[0][1: -1]
            if literal_string in self.__literal_map:
                literal_symbol = self.__literal_map[literal_string]
            else:
                literal_symbol = configure.boson_symbol_template.format(self.__literal_number)
                self.__literal_number += 1
                self.__literal_map[literal_string] = literal_symbol
                self.__literal_reverse_map[literal_symbol] = literal_string
                self.__lexical_definition[literal_symbol] = ['\\' + '\\'.join(literal_string)]
            return literal_symbol

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
        if lexer.tokenize(boson_script_text) != lexer.no_error_line():
            raise ValueError('[Boson Script Analyzer] Invalid Token [Line: {}]'.format(lexer.error_line()))
        self.__init__()
        self.init_semantic()
        interpreter.execute(self.parse(lexer.token_list()))
