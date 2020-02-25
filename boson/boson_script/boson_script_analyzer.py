import boson.configure as configure
from boson.boson_script.boson_script_parser import BosonGrammarNode, BosonLexicalAnalyzer, BosonGrammarAnalyzer, BosonSemanticsAnalyzer


semantic_analyzer = BosonSemanticsAnalyzer()


class BosonScriptAnalyzer:
    def __init__(self):
        self.__grammar_analyzer: BosonGrammarAnalyzer = BosonGrammarAnalyzer()
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

    def __add_select(self, name_list: list) -> str:
        hidden_name = self.__generate_hidden_name()
        for name in name_list:
            sentence = (hidden_name, name)
            self.__sentence_add(sentence)
            self.__naive_sentence_set.add(sentence)
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
        @semantic_analyzer.semantics_entity('command')
        def _semantic_command(grammar_entity):
            self.__command_list.append(grammar_entity)

        @semantic_analyzer.semantics_entity('lexical_define')
        def _semantic_lexical_define(grammar_entity):
            grammar_entity[1] = grammar_entity[1][1:-1]
            self.__lexical_definition[grammar_entity[0]] = grammar_entity[1:]

        @semantic_analyzer.semantics_entity('regular_expression')
        def _semantic_regular_expression(grammar_entity):
            return [grammar_entity[0][1:-1], grammar_entity[1] if len(grammar_entity) > 1 else []]

        @semantic_analyzer.semantics_entity('reduce')
        def _semantic_reduce(grammar_entity):
            reduce_name = grammar_entity[0]
            derivation_list = grammar_entity[1]
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

        @semantic_analyzer.semantics_entity('name_closure')
        def _semantic_name_closure(grammar_entity):
            name = grammar_entity[0]
            if len(grammar_entity) == 2:
                if grammar_entity[1] == '+':
                    name = self.__add_positive_closure(name)
                elif grammar_entity[1] == '*':
                    name = self.__add_colin_closure(name)
                else:
                    raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
            return name

        @semantic_analyzer.semantics_entity('complex_closure')
        def _semantic_complex_closure(grammar_entity):
            name = self.__add_hidden_derivation(grammar_entity[0])
            if len(grammar_entity) == 2:
                closure = grammar_entity[1][0]
                if closure == '+':
                    name = self.__add_positive_closure(name)
                elif closure == '*':
                    name = self.__add_colin_closure(name)
                else:
                    raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
            return name

        @semantic_analyzer.semantics_entity('complex_optional')
        def _semantic_complex_optional(grammar_entity):
            return self.__add_optional(self.__add_hidden_derivation(grammar_entity[0]))

        @semantic_analyzer.semantics_entity('select')
        def _semantic_select(grammar_entity):
            return [self.__add_select(grammar_entity)]

        @semantic_analyzer.semantics_entity('grammar_node')
        def _semantic_grammar_node(grammar_entity):
            if len(grammar_entity) == 1:
                return grammar_entity[0][1:]
            elif len(grammar_entity) == 2:
                if grammar_entity[0] == configure.boson_grammar_tuple_unpack:
                    return grammar_entity[0] + grammar_entity[1][1:]
                else:
                    return grammar_entity[0][1:], tuple(grammar_entity[1])
            elif len(grammar_entity) == 3:
                if grammar_entity[0] == configure.boson_grammar_tuple_unpack:
                    return grammar_entity[0] + grammar_entity[1][1:], tuple(grammar_entity[2])
                else:
                    return grammar_entity[0], (grammar_entity[1],) + tuple(grammar_entity[2])
            elif len(grammar_entity) == 4:
                return grammar_entity[0] + grammar_entity[1][1:], (grammar_entity[2],) + tuple(grammar_entity[3])
            else:
                raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')

        @semantic_analyzer.semantics_entity('literal')
        def _semantic_literal(grammar_entity):
            literal_string = grammar_entity[0][1: -1]
            if literal_string in self.__literal_map:
                literal_symbol = self.__literal_map[literal_string]
            else:
                literal_symbol = configure.boson_symbol_template.format(self.__literal_number)
                self.__literal_number += 1
                self.__literal_map[literal_string] = literal_symbol
                self.__literal_reverse_map[literal_symbol] = literal_string
                self.__lexical_definition[literal_symbol] = ['\\' + '\\'.join(literal_string)]
            return literal_symbol

    def grammar_analysis(self, token_list: list) -> BosonGrammarNode:
        grammar = self.__grammar_analyzer.grammar_analysis(token_list)
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
        tokenizer = BosonLexicalAnalyzer()
        if tokenizer.tokenize(boson_script_text) != tokenizer.no_error_line():
            raise ValueError('[Boson Script Analyzer] Invalid Token [Line: {}]'.format(tokenizer.error_line()))
        self.__init__()
        self.init_semantic()
        semantic_analyzer.semantics_analysis(self.grammar_analysis(tokenizer.token_list()))
