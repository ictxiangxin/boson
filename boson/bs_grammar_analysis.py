import re
import boson.bs_configure as configure
from boson.bs_boson_script_analyzer import BosonGrammarAnalyzer, BosonSemanticsAnalyzer
from boson.bs_data_package import GrammarPackage


class LexicalToken:
    def __init__(self):
        self.__symbol = None
        self.__text = None
        self.__line = None

    def get_symbol(self):
        return self.__symbol

    def set_symbol(self, symbol: str):
        self.__symbol = symbol

    symbol = property(get_symbol, set_symbol)

    def get_text(self):
        return self.__text

    def set_text(self, text: str):
        self.__text = text

    text = property(get_text, set_text)

    def get_line(self):
        return self.__line

    def set_line(self, line: int):
        self.__line = line

    line = property(get_line, set_line)


token_tuple = [
    ('name',          r'[_a-zA-Z][_a-zA-Z0-9]*'),
    ('reduce',        r'\:'),
    ('or',            r'\|'),
    ('comma',         r'\,'),
    ('assign',        r'\='),
    ('plus',          r'\+'),
    ('star',          r'\*'),
    ('parentheses_l', r'\('),
    ('parentheses_r', r'\)'),
    ('bracket_l',     r'\['),
    ('bracket_r',     r'\]'),
    ('node',          r'\$[0-9]+\*{0,1}|\$\@|\$\$|\$\?'),
    ('string',        r'\'.*?[^\\]\'|\".*?[^\\]\"'),
    ('alphabet',      r'\/.*?[^\\]\/'),
    ('null',          r'~'),
    ('comment',       r'#[^\r\n]*'),
    ('command',       r'%[_a-zA-Z]+'),
    ('end',           r'\;'),
    ('except',        r'\^'),
    ('greedy',        r'\?'),
    ('skip',          r'[ \t]+'),
    ('newline',       r'\n|\r\n'),
    ('invalid',       r'.'),
]

token_regular_expression = '|'.join('(?P<{}>{})'.format(*pair) for pair in token_tuple)


def bs_tokenize(text: str):
    token_list = list()
    line = 1
    for one_token in re.finditer(token_regular_expression, text):
        symbol = one_token.lastgroup
        text = one_token.group(symbol)
        if symbol in ['skip', 'comment']:
            pass
        elif symbol == 'newline':
            line += 1
        elif symbol == 'invalid':
            raise RuntimeError('[Line: {}] Invalid token: {}'.format(line, text))
        else:
            token = LexicalToken()
            token.symbol = symbol
            token.text = text
            token.line = line
            token_list.append(token)
    token = LexicalToken()
    token.symbol = configure.boson_end_symbol
    token.text = ''
    token.line = line
    token_list.append(token)
    return token_list


semantic_analyzer = BosonSemanticsAnalyzer()


class BosonScriptAnalyzer:
    def __init__(self):
        self.__grammar_analyzer = BosonGrammarAnalyzer()
        self.__sentence_set = set()
        self.__grammar_tuple_map = {}
        self.__none_grammar_tuple_set = set()
        self.__command_list = []
        self.__literal_map = {}
        self.__literal_reverse_map = {}
        self.__sentence_grammar_map = {}
        self.__naive_sentence = set()
        self.__literal_number = 1
        self.__hidden_name_number = 0
        self.__grammar_number = 0

    def __generate_hidden_name(self):
        hidden_name = '{}{}'.format(configure.boson_hidden_name_prefix, self.__hidden_name_number)
        self.__hidden_name_number += 1
        return hidden_name

    def __sentence_add(self, sentence, grammar_tuple=None):
        self.__sentence_set.add(sentence)
        if grammar_tuple is None:
            self.__none_grammar_tuple_set.add(sentence)
        else:
            self.__grammar_tuple_map[sentence] = grammar_tuple

    def __add_positive_closure(self, name):
        hidden_name = self.__generate_hidden_name()
        self.__sentence_add((hidden_name, hidden_name, name), ('{}0'.format(configure.boson_grammar_tuple_unpack), '1'))
        self.__sentence_add((hidden_name, name))
        return hidden_name

    def __add_colin_closure(self, name):
        hidden_name = self.__generate_hidden_name()
        self.__sentence_add((hidden_name, hidden_name, name), ('{}0'.format(configure.boson_grammar_tuple_unpack), '1'))
        self.__sentence_add((hidden_name, configure.boson_null_symbol), tuple())
        return hidden_name

    def __add_optional(self, name):
        hidden_name = self.__generate_hidden_name()
        self.__sentence_add((hidden_name, name))
        self.__sentence_add((hidden_name, configure.boson_null_symbol), tuple())
        return hidden_name

    def __add_select(self, name_list):
        hidden_name = self.__generate_hidden_name()
        for name in name_list:
            sentence = (hidden_name, name)
            self.__sentence_add(sentence)
            self.__naive_sentence.add(sentence)
        return hidden_name

    def __add_hidden_derivation(self, derivation):
        hidden_name = self.__generate_hidden_name()
        self.__sentence_add((hidden_name,) + tuple(derivation))
        return hidden_name

    def init_semantic(self):
        @semantic_analyzer.semantics_entity('command')
        def _semantic_command(grammar_entity):
            self.__command_list.append(grammar_entity)

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
                if len(sentence) == 1 or (len(sentence) == 2 and not sentence[1].startswith(configure.boson_hidden_name_prefix)):
                    self.__naive_sentence.add(sentence)
                if len(derivation) == 1:
                    self.__none_grammar_tuple_set.add(sentence)
                    self.__sentence_grammar_map[sentence] = self.__grammar_number
                elif len(derivation) == 2:
                    self.__grammar_tuple_map[sentence] = tuple(derivation[1])
                    self.__sentence_grammar_map[sentence] = self.__grammar_number
                elif len(derivation) == 3:
                    self.__grammar_tuple_map[sentence] = tuple(derivation[2])
                    self.__sentence_grammar_map[sentence] = derivation[1]
                else:
                    raise RuntimeError('Never touch here.')
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
                    raise RuntimeError('Never touch here.')
            return name

        @semantic_analyzer.semantics_entity('complex_closure')
        def _semantic_complex_closure(grammar_entity):
            name = self.__add_hidden_derivation(grammar_entity[0])
            if len(grammar_entity) == 2:
                may_closure = grammar_entity[1]
                if may_closure == '+':
                    name = self.__add_positive_closure(name)
                elif may_closure == '*':
                    name = self.__add_colin_closure(name)
                else:
                    raise RuntimeError('Never touch here.')
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
                if isinstance(grammar_entity[1], str):
                    return grammar_entity[0] + grammar_entity[1][1:]
                else:
                    return grammar_entity[0][1:], tuple(grammar_entity[1])
            elif len(grammar_entity) == 3:
                return grammar_entity[0] + grammar_entity[1][1:], tuple(grammar_entity[2])
            else:
                raise RuntimeError('Never touch here.')

        @semantic_analyzer.semantics_entity('literal')
        def _semantic_literal(grammar_entity):
            literal = grammar_entity[0]
            literal_string = literal[1: -1]
            if literal_string in self.__literal_map:
                literal_symbol = self.__literal_map[literal_string]
            else:
                literal_symbol = configure.boson_literal_template.format(self.__literal_number)
                self.__literal_number += 1
                self.__literal_map[literal_string] = literal_symbol
                self.__literal_reverse_map[literal_symbol] = literal_string
            return literal_symbol

    def grammar_analysis(self, token_list):
        grammar = self.__grammar_analyzer.grammar_analysis(token_list)
        if grammar.error_index is None:
            return grammar.grammar_tree
        else:
            start_index = grammar.error_index
            end_index = grammar.error_index
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
            error_message = '\nGrammar Error [Line: {}] \n'.format(error_line)
            error_token_text_list = [token.text for token in error_token_list]
            error_message += '{}\n'.format(' '.join(error_token_text_list))
            error_message += ' ' * (sum([len(text) for text in error_token_text_list[:offset]]) + offset) + '^' * len(error_token_text_list[offset])
            raise ValueError(error_message)

    def semantics_analysis(self, grammar_tree):
        self.__init__()
        self.init_semantic()
        semantic_analyzer.semantics_analysis(grammar_tree)
        grammar_package = GrammarPackage()
        grammar_package.command_list = self.__command_list
        grammar_package.sentence_set = self.__sentence_set
        grammar_package.grammar_tuple_map = self.__grammar_tuple_map
        grammar_package.none_grammar_tuple_set = self.__none_grammar_tuple_set
        grammar_package.literal_map = self.__literal_map
        grammar_package.literal_reverse_map = self.__literal_reverse_map
        grammar_package.sentence_grammar_map = self.__sentence_grammar_map
        grammar_package.naive_sentence = self.__naive_sentence
        return grammar_package

    def parse(self, token_list):
        grammar_tree = self.grammar_analysis(token_list)
        grammar_package = self.semantics_analysis(grammar_tree)
        return grammar_package


def bs_grammar_analysis(text: str):
    token_list = bs_tokenize(text)
    script_analyzer = BosonScriptAnalyzer()
    grammar_package = script_analyzer.parse(token_list)
    return grammar_package
