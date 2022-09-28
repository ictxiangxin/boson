from typing import Optional, Any, List, Dict, Set, Tuple

import boson.configure as configure
from boson.boson_script.boson_script_parser import \
    BosonToken, \
    BosonGrammar, \
    BosonGrammarNode, \
    BosonLexer, \
    BosonParser, \
    BosonInterpreter, \
    BosonSemanticsNode
from boson.boson_script.sentence_attribute import SentenceAttribute

interpreter = BosonInterpreter()


def get_semantic_node_data_list(semantic_node: BosonSemanticsNode) -> list:
    return [node.get_data() for node in semantic_node.children()]


def generate_naive_grammar_tuple(grammar_tuple: Tuple[str | tuple, ...], element_definition_map: Dict[str, int]) -> Tuple[str | tuple, ...]:
    grammar_node_list: List[str | tuple, ...] = []
    for node in grammar_tuple:
        if isinstance(node, tuple):
            grammar_node_list.append(generate_naive_grammar_tuple(node, element_definition_map))
        else:
            if node.startswith(configure.boson_grammar_tuple_unpack):
                node_index = node[1:]
                unpack = configure.boson_grammar_tuple_unpack
            else:
                node_index = node
                unpack = ''
            grammar_node_list.append(unpack + str(element_definition_map.get(node_index, node_index)))
    return tuple(grammar_node_list)


class BosonScriptAnalyzer:
    def __init__(self):
        self.__parser: BosonParser = BosonParser()
        self.__sentence_set: Set[Tuple[str, ...]] = set()
        self.__sentence_grammar_tuple_mapping: Dict[Tuple[str, ...], Tuple[str | tuple, ...]] = {}
        self.__sentence_attribute_mapping: Dict[Tuple[str, ...], SentenceAttribute] = {}
        self.__none_grammar_tuple_set: Set[Tuple[str, ...]] = set()
        self.__command_list: List[List[str | list | dict]] = []
        self.__literal_mapping: Dict[str, str] = {}
        self.__literal_reverse_mapping: Dict[str, str] = {}
        self.__sentence_grammar_name_mapping: Dict[Tuple[str, ...], str] = {}
        self.__naive_sentence_set: Set[Tuple[str, ...]] = set()
        self.__literal_number: int = 1
        self.__hidden_regular_number: int = 1
        self.__hidden_name_number: int = 0
        self.__lexical_definition: Dict[str, Dict[str, str | int | bool | Optional[List[str]]]] = {}
        self.__lexical_number: int = 0
        self.__hidden_derivation_cache: Dict[Tuple[str, ...], str] = {}
        self.__positive_closure_cache: Dict[str, str] = {}
        self.__colin_closure_cache: Dict[str, str] = {}
        self.__optional_cache: Dict[str, str] = {}
        self.__sentence_order_base_mapping: Dict[str, int] = {}
        self.__current_index: int = 1

    def __generate_hidden_name(self, prefix: str = configure.boson_hidden_name_prefix) -> str:
        hidden_name: str = '{}{}'.format(prefix, self.__hidden_name_number)
        self.__hidden_name_number += 1
        return hidden_name

    def __generate_index(self) -> int:
        index: int = self.__current_index
        self.__current_index += 1
        return index

    def __sentence_add(self, sentence: Tuple[str, ...], sentence_attribute: SentenceAttribute, grammar_tuple: Optional[Tuple[str | tuple, ...]] = None) -> None:
        self.__sentence_set.add(sentence)
        self.__sentence_attribute_mapping[sentence] = sentence_attribute
        if grammar_tuple is None:
            self.__none_grammar_tuple_set.add(sentence)
        else:
            self.__sentence_grammar_tuple_mapping[sentence] = grammar_tuple

    def __add_positive_closure(self, name: str) -> str:
        if name in self.__positive_closure_cache:
            return self.__positive_closure_cache[name]
        else:
            hidden_name: str = self.__generate_hidden_name(configure.boson_operator_name_prefix)
            self.__positive_closure_cache[name] = hidden_name
            attribute: SentenceAttribute = SentenceAttribute()
            attribute.parse_index = self.__generate_index()
            self.__sentence_add((hidden_name, hidden_name, name), attribute, ('{}0'.format(configure.boson_grammar_tuple_unpack), '1'))
            attribute: SentenceAttribute = SentenceAttribute()
            attribute.parse_index = self.__generate_index()
            self.__sentence_add((hidden_name, name), attribute)
            return hidden_name

    def __add_colin_closure(self, name: str) -> str:
        if name in self.__colin_closure_cache:
            return self.__colin_closure_cache[name]
        else:
            hidden_name: str = self.__generate_hidden_name(configure.boson_operator_name_prefix)
            self.__colin_closure_cache[name] = hidden_name
            attribute: SentenceAttribute = SentenceAttribute()
            attribute.parse_index = self.__generate_index()
            self.__sentence_add((hidden_name, hidden_name, name), attribute, ('{}0'.format(configure.boson_grammar_tuple_unpack), '1'))
            attribute: SentenceAttribute = SentenceAttribute()
            attribute.parse_index = self.__generate_index()
            self.__sentence_add((hidden_name, configure.boson_null_symbol), attribute, tuple())
            return hidden_name

    def __add_optional(self, name: str) -> str:
        if name in self.__optional_cache:
            return self.__optional_cache[name]
        else:
            hidden_name: str = self.__generate_hidden_name(configure.boson_operator_name_prefix)
            self.__optional_cache[name] = hidden_name
            attribute: SentenceAttribute = SentenceAttribute()
            attribute.parse_index = self.__generate_index()
            self.__sentence_add((hidden_name, name), attribute, ('{}0'.format(configure.boson_grammar_tuple_unpack),))
            attribute: SentenceAttribute = SentenceAttribute()
            attribute.parse_index = self.__generate_index()
            self.__sentence_add((hidden_name, configure.boson_null_symbol), attribute, tuple())
            return hidden_name

    def __add_select(self, sentence_list: List[List[str]]) -> str:
        hidden_name: str = self.__generate_hidden_name()
        for order, sentence in enumerate(sentence_list):
            select_sentence: Tuple[str, ...] = (hidden_name,) + tuple(sentence)
            attribute: SentenceAttribute = SentenceAttribute()
            attribute.parse_index = self.__generate_index()
            attribute.order = order
            self.__sentence_add(select_sentence, attribute)
            if len(select_sentence) == 2:
                for i in range(2):
                    if select_sentence[i].startswith(configure.boson_operator_name_prefix) or select_sentence[i].startswith(configure.boson_hidden_name_prefix):
                        break
                else:
                    self.__naive_sentence_set.add(select_sentence)
        return hidden_name

    def __add_hidden_derivation(self, derivation: List[str]) -> str:
        derivation_tuple: Tuple[str, ...] = tuple(derivation)
        if derivation_tuple in self.__hidden_derivation_cache:
            return self.__hidden_derivation_cache[derivation_tuple]
        else:
            hidden_name: str = self.__generate_hidden_name()
            self.__hidden_derivation_cache[derivation_tuple] = hidden_name
            attribute: SentenceAttribute = SentenceAttribute()
            attribute.parse_index = self.__generate_index()
            self.__sentence_add((hidden_name,) + tuple(derivation), attribute)
            return hidden_name

    def command_list(self) -> List[List[str | list]]:
        return self.__command_list

    def lexical_definition(self) -> Dict[str, Dict[str, str | int | bool | Optional[List[str]]]]:
        return self.__lexical_definition

    def sentence_set(self) -> Set[Tuple[str, ...]]:
        return self.__sentence_set

    def sentence_grammar_tuple_mapping(self) -> Dict[Tuple[str, ...], Tuple[str | tuple, ...]]:
        return self.__sentence_grammar_tuple_mapping

    def sentence_attribute_mapping(self) -> Dict[Tuple[str, ...], SentenceAttribute]:
        return self.__sentence_attribute_mapping

    def none_grammar_tuple_set(self) -> Set[Tuple[str, ...]]:
        return self.__none_grammar_tuple_set

    def literal_mapping(self) -> Dict[str, str]:
        return self.__literal_mapping

    def literal_reverse_mapping(self) -> Dict[str, str]:
        return self.__literal_reverse_mapping

    def sentence_grammar_name_mapping(self) -> Dict[Tuple[str, ...], str]:
        return self.__sentence_grammar_name_mapping

    def naive_sentence_set(self) -> Set[Tuple[str, ...]]:
        return self.__naive_sentence_set

    def init_semantic(self) -> None:
        @interpreter.register_action('command')
        def _semantic_command(semantic_node) -> BosonSemanticsNode:
            command_name: str = semantic_node[0].get_text()
            command_arguments: List[str | dict] = [node.get_text() if node.get_text() else node.get_data() for node in semantic_node[1].children()]
            self.__command_list.append([command_name, command_arguments])
            return BosonSemanticsNode.null_node()

        @interpreter.register_action('lexical_define')
        def _semantic_lexical_define(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            lexical_name: str = semantic_node[0].get_text()
            definition: Dict[str, str | int | bool | Optional[List[str]]] = {
                'regular': semantic_node[1].get_text()[1:-1],
                'number': self.__lexical_number
            }
            self.__lexical_number += 1
            if len(semantic_node.children()) == 4:
                function_index: int = 3
                definition['non_greedy'] = semantic_node[2].get_text() == configure.boson_lexical_non_greedy_sign
            else:
                function_index: int = 2
                definition['non_greedy'] = False
            definition['function_list'] = [node.get_text() for node in semantic_node[function_index].children()]
            self.__lexical_definition[lexical_name] = definition
            return BosonSemanticsNode.null_node()

        @interpreter.register_action('reduce')
        def _semantic_reduce(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            reduce_name: str = semantic_node[0].get_text()
            derivation_list: BosonSemanticsNode = semantic_node[1]
            self.__sentence_order_base_mapping.setdefault(reduce_name, 0)
            order_base: int = self.__sentence_order_base_mapping[reduce_name]
            for order, derivation in enumerate(derivation_list.children()):
                element_definition_map: Dict[str, int] = {}
                derivation_body = derivation[0]
                if len(derivation_body.children()) == 0 and not derivation_body.is_null():
                    sentence: Tuple[str, ...] = (reduce_name, derivation_body.get_text())
                elif len(derivation_body.children()) > 0:
                    derivation_symbol_list: List[str] = []
                    for element_index, node in enumerate(derivation_body.children()):
                        element_name = node.get_text()
                        definition_tuple: Tuple[Optional[str], Optional[Dict[str, int]]] = node.get_data()
                        derivation_symbol_list.append(element_name)
                        alias_name: Optional[str] = definition_tuple[0]
                        lower_level_element_definition_map: Optional[Dict[str, int]] = definition_tuple[1]
                        if lower_level_element_definition_map is not None:
                            for alias, sub_index in lower_level_element_definition_map.items():
                                if alias in element_definition_map:
                                    raise ValueError(f'[Boson Script Analyzer] Element Definition Duplicate: {alias}')
                                element_definition_map[alias] = sub_index
                        if alias_name is not None:
                            if alias_name in element_definition_map:
                                raise ValueError(f'[Boson Script Analyzer] Element Definition Duplicate: {alias_name}')
                            else:
                                element_definition_map[alias_name] = element_index
                    sentence: Tuple[str, ...] = (reduce_name,) + tuple(derivation_symbol_list)
                else:
                    sentence: Tuple[str, ...] = (reduce_name, configure.boson_null_symbol)
                if len(sentence) == 2:
                    for i in range(2):
                        if sentence[i].startswith(configure.boson_operator_name_prefix) or sentence[i].startswith(configure.boson_hidden_name_prefix):
                            break
                    else:
                        self.__naive_sentence_set.add(sentence)
                grammar_tuple: None = None
                attribute: SentenceAttribute = SentenceAttribute()
                attribute.parse_index = self.__generate_index()
                attribute.order = order_base + order
                if len(derivation.children()) == 1:
                    self.__none_grammar_tuple_set.add(sentence)
                else:
                    if derivation[1].children():
                        self.__sentence_grammar_name_mapping[sentence] = derivation[1][0].get_text()
                    grammar_tuple: Tuple[str | tuple, ...] = generate_naive_grammar_tuple(tuple(get_semantic_node_data_list(derivation[2])), element_definition_map)
                    if derivation[3].children():
                        attribute.custom = derivation[3][0].get_data()
                self.__sentence_add(sentence, attribute, grammar_tuple)
            self.__sentence_order_base_mapping[reduce_name] += len(derivation_list.children())
            return BosonSemanticsNode.null_node()

        @interpreter.register_action('element_definition')
        def _element_definition(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            element_definition_node: BosonSemanticsNode = BosonSemanticsNode()
            element_definition_node.set_text(semantic_node[0].get_text())
            lower_level_data: Optional[Tuple[Optional[str], Optional[Dict[str, int]]]] = semantic_node[0].get_data()
            element_alias: Optional[str] = None
            if len(semantic_node.children()) == 2:
                element_alias = semantic_node[1].get_text()
            if lower_level_data is None:
                element_definition_node.set_data((element_alias, None))
            else:
                element_definition_node.set_data((element_alias, lower_level_data[1]))
            return element_definition_node

        @interpreter.register_action('name_closure')
        def _semantic_name_closure(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            name: str = semantic_node[0].get_text()
            if len(semantic_node.children()) == 2:
                if semantic_node[1].get_text() == '+':
                    name: str = self.__add_positive_closure(name)
                elif semantic_node[1].get_text() == '*':
                    name: str = self.__add_colin_closure(name)
                else:
                    raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
            name_closure_node: BosonSemanticsNode = BosonSemanticsNode()
            name_closure_node.set_text(name)
            return name_closure_node

        @interpreter.register_action('complex_closure')
        def _semantic_complex_closure(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            lower_level_data: Tuple[None, Dict[str, int]] = semantic_node[0].get_data()
            name: str = semantic_node[0].get_text()
            if len(semantic_node.children()) == 2:
                closure: str = semantic_node[1].get_text()
                if closure == '+':
                    name: str = self.__add_positive_closure(name)
                elif closure == '*':
                    name: str = self.__add_colin_closure(name)
                else:
                    raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
            complex_closure_node: BosonSemanticsNode = BosonSemanticsNode()
            complex_closure_node.set_text(name)
            complex_closure_node.set_data((None, lower_level_data[1]))
            return complex_closure_node

        @interpreter.register_action('complex_optional')
        def _semantic_complex_optional(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            lower_level_data: Tuple[None, Dict[str, int]] = semantic_node[0].get_data()
            name: str = semantic_node[0].get_text()
            complex_optional_node: BosonSemanticsNode = BosonSemanticsNode()
            complex_optional_node.set_text(self.__add_optional(name))
            complex_optional_node.set_data((None, lower_level_data[1]))
            return complex_optional_node

        @interpreter.register_action('select')
        def _semantic_select(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            native_sentence_list: List[List[str]] = []
            element_definition_map: Dict[str, int] = {}
            for sentence in semantic_node.children():
                native_sentence: List[str] = []
                for index, element_definition in enumerate(sentence):
                    lower_level_data: Optional[Tuple[str, Optional[Dict[str, int]]]] = element_definition.get_data()
                    native_sentence.append(element_definition.get_text())
                    if lower_level_data[0] is not None:
                        element_definition_map[lower_level_data[0]] = index
                    if lower_level_data[1] is not None:
                        for alias, sub_index in lower_level_data[1].items():
                            if alias in element_definition_map:
                                raise ValueError(f'[Boson Script Analyzer] Element Definition Duplicate: {alias}.')
                            element_definition_map[alias] = sub_index
                native_sentence_list.append(native_sentence)
            select_node: BosonSemanticsNode = BosonSemanticsNode()
            select_node.set_text(self.__add_select(native_sentence_list))
            select_node.set_data((None, element_definition_map))
            sentence_node: BosonSemanticsNode = BosonSemanticsNode()
            sentence_node.append(select_node)
            return select_node

        @interpreter.register_action('getter_tuple')
        def _semantic_getter_tuple(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            number_text = semantic_node[0].get_text()
            if number_text.startswith('0x'):
                index = int(number_text, 16)
            else:
                index = int(number_text)
            getter_node: BosonSemanticsNode = BosonSemanticsNode()
            getter_node.append(BosonSemanticsNode(configure.boson_grammar_tuple_unpack))
            getter_node.append(BosonSemanticsNode(str(index)))
            return getter_node

        @interpreter.register_action('grammar_node')
        def _semantic_grammar_node(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            if len(semantic_node.children()) == 1:
                grammar_node: str = semantic_node[0].get_text()[1:]
            elif len(semantic_node.children()) == 2:
                if semantic_node[0].get_text() == configure.boson_grammar_tuple_unpack:
                    grammar_node: str = semantic_node[0].get_text() + semantic_node[1].get_text()[1:]
                else:
                    grammar_node: tuple = (semantic_node[0].get_text()[1:], tuple(get_semantic_node_data_list(semantic_node[1])))
            elif len(semantic_node.children()) == 3:
                if semantic_node[0].get_text() == configure.boson_grammar_tuple_unpack:
                    grammar_node: tuple = (semantic_node[0].get_text() + semantic_node[1].get_text()[1:], tuple(get_semantic_node_data_list(semantic_node[2])))
                else:
                    grammar_node: tuple = (semantic_node[0].get_text()[1:], (semantic_node[1].get_text(),) + tuple(get_semantic_node_data_list(semantic_node[2])))
            elif len(semantic_node.children()) == 4:
                grammar_node: tuple = (semantic_node[0].get_text() + semantic_node[1].get_text()[1:], (semantic_node[2].get_text(),) + tuple(get_semantic_node_data_list(semantic_node[3])))
            else:
                raise RuntimeError('[Boson Script Analyzer] Never Touch Here.')
            return BosonSemanticsNode(grammar_node)

        @interpreter.register_action('literal')
        def _semantic_literal(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            literal_string: str = semantic_node[0].get_text()[1: -1]
            if literal_string in self.__literal_mapping:
                literal_symbol: str = self.__literal_mapping[literal_string]
            else:
                literal_symbol: str = configure.boson_symbol_template.format(self.__literal_number)
                self.__literal_number += 1
                self.__literal_mapping[literal_string] = literal_symbol
                self.__literal_reverse_mapping[literal_symbol] = literal_string
                self.__lexical_definition[literal_symbol] = {
                    'regular': '\\' + '\\'.join(literal_string),
                    'non_greedy': False,
                    'function_list': None
                }
            literal_node: BosonSemanticsNode = BosonSemanticsNode()
            literal_node.set_text(literal_symbol)
            return literal_node

        @interpreter.register_action('regular')
        def _semantic_regular(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            regular_string: str = semantic_node[0].get_text()[1: -1]
            if regular_string in self.__literal_mapping:
                regular_symbol: str = self.__literal_mapping[regular_string]
            else:
                regular_symbol: str = configure.boson_symbol_template.format(self.__literal_number)
                self.__literal_number += 1
                self.__literal_mapping[regular_string] = regular_symbol
                self.__literal_reverse_mapping[regular_symbol] = semantic_node[0].get_text()
                if len(semantic_node.children()) == 2:
                    no_greedy = True
                else:
                    no_greedy = False
                self.__lexical_definition[regular_symbol] = {
                    'regular': regular_string,
                    'non_greedy': no_greedy,
                    'function_list': None
                }
            regular_node: BosonSemanticsNode = BosonSemanticsNode()
            regular_node.set_text(regular_symbol)
            return regular_node

        @interpreter.register_action('attribute')
        def _semantic_attribute(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            attribute: Dict[str, Any] = {}
            for key_value in semantic_node[0].children():
                key: str = key_value[0].get_text()
                value: BosonSemanticsNode = key_value[1]
                if value.get_text() == '':
                    attribute[key] = value.get_data()
                else:
                    attribute[key] = value.get_text()
            attribute_node: BosonSemanticsNode = BosonSemanticsNode()
            attribute_node.set_data(attribute)
            return attribute_node

        @interpreter.register_action('attribute_value_list')
        def _semantic_attribute_value_list(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            attribute_value_list: list = []
            for value_node in semantic_node.children():
                if value_node.get_text() == '':
                    attribute_value_list.append(value_node.get_data())
                else:
                    attribute_value_list.append(value_node.get_text())
            attribute_value_list_node: BosonSemanticsNode = BosonSemanticsNode()
            attribute_value_list_node.set_data(attribute_value_list)
            return attribute_value_list_node

        @interpreter.register_action('string')
        def _semantic_string(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            string_node: BosonSemanticsNode = BosonSemanticsNode()
            string_node.set_data(semantic_node[0].get_text()[1:-1])
            return string_node

        @interpreter.register_action('number')
        def _semantic_number(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            number_text: str = semantic_node[0].get_text()
            number_node: BosonSemanticsNode = BosonSemanticsNode()
            if number_text.startswith('0x'):
                number_node.set_data(int(number_text, 16))
            else:
                number_node.set_data(int(number_text))
            return number_node

    def parse(self, token_list: List[BosonToken]) -> BosonGrammarNode:
        grammar: BosonGrammar = self.__parser.parse(token_list)
        if grammar.error_index == grammar.no_error_index():
            return grammar.grammar_tree
        else:
            start_index: int = grammar.error_index
            end_index: int = grammar.error_index
            error_line: int = token_list[grammar.error_index].line
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
            offset: int = grammar.error_index - start_index - 1
            error_token_list: List[BosonToken] = token_list[start_index + 1: end_index]
            error_message: str = f'\n[Boson Script Analyzer] Syntax Error <Line: {error_line}>\n'
            error_token_text_list: List[str] = [token.text for token in error_token_list]
            error_message += '{}\n'.format(' '.join(error_token_text_list))
            error_message += ' ' * (sum([len(text) for text in error_token_text_list[:offset]]) + offset) + '^' * len(error_token_text_list[offset])
            raise ValueError(error_message)

    def tokenize_and_parse(self, boson_script_text: str) -> None:
        lexer: BosonLexer = BosonLexer()
        if lexer.tokenize(boson_script_text) != lexer.no_error_index():
            raise ValueError(f'[Boson Script Analyzer] Invalid Token [Line: {lexer.line()}, Index: {lexer.error_index()}]')
        self.__init__()
        self.init_semantic()
        interpreter.execute(self.parse(lexer.token_list()))
