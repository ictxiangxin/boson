import re
import boson.bs_configure as configure
from boson.bs_boson_bnf_analyzer import BosonBNFAnalyzer
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
    ('literal',       r'\'.*?[^\\]\'|\".*?[^\\]\"'),
    ('null',          r'~'),
    ('comment',       r'#[^\r\n]*'),
    ('command',       r'%[_a-zA-Z]+'),
    ('end',           r'\;'),
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


class BosonScriptAnalyzer:
    def __init__(self):
        self.__bnf_grammar_analyzer = BosonBNFAnalyzer()
        self.__sentence_set = set()
        self.__grammar_tuple_map = {}
        self.__none_grammar_tuple_set = set()
        self.__command_list = []
        self.__literal_map = {}
        self.__literal_reverse_map = {}
        self.__grammar_name_map = {}
        self.__temp_grammar_name_map = {}
        self.__sentence_grammar_map = {}
        self.__naive_sentence = set()
        self.__literal_number = 1
        self.__hidden_name_number = 0
        self.__grammar_number = 0
        self.__temp_grammar_number = 0

    def __get_value(self, grammar_tree_node):
        if isinstance(grammar_tree_node, tuple) and isinstance(grammar_tree_node[0], int):
            return self.__semantic_analysis(grammar_tree_node)
        else:
            return grammar_tree_node

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
        self.__sentence_add((hidden_name, name), ('0',))
        return hidden_name

    def __add_colin_closure(self, name):
        hidden_name = self.__generate_hidden_name()
        self.__sentence_add((hidden_name, hidden_name, name), ('{}0'.format(configure.boson_grammar_tuple_unpack), '1'))
        self.__sentence_add((hidden_name, configure.boson_null_symbol), tuple())
        return hidden_name

    def __add_optional(self, name):
        hidden_name = self.__generate_hidden_name()
        self.__sentence_add((hidden_name, name), ('0',))
        self.__sentence_add((hidden_name, configure.boson_null_symbol), tuple())
        return hidden_name

    def __add_hidden_derivation(self, derivation):
        hidden_name = self.__generate_hidden_name()
        self.__sentence_add((hidden_name,) + tuple(derivation), (configure.boson_grammar_tuple_all,))
        return hidden_name

    def __semantic_analysis(self, grammar_tree):
        reduce_number = grammar_tree[0]
        grammar_tuple = grammar_tree[1:]
        grammar_tuple = tuple(map(self.__get_value, grammar_tuple))
        if reduce_number == 0:
            return grammar_tuple[0]
        elif reduce_number == 1:
            return grammar_tuple[0]
        elif reduce_number == 2:
            return [grammar_tuple[0]]
        elif reduce_number == 3:
            return grammar_tuple[0] + [grammar_tuple[1]]
        elif reduce_number == 4:
            return grammar_tuple[0]
        elif reduce_number == 5:
            return grammar_tuple[0]
        elif reduce_number == 6:
            return None
        elif reduce_number == 7:
            command = grammar_tuple[0]
            arguments = grammar_tuple[1]
            literal_command = [command[1:]]
            for each_name in arguments:
                literal_command.append(each_name)
            self.__command_list.append(literal_command)
            return None
        elif reduce_number == 8:
            hidden_derivation = self.__add_hidden_derivation(grammar_tuple[0])
            return self.__add_optional(hidden_derivation)
        elif reduce_number == 9:
            if grammar_tuple[1] is None:
                return self.__add_hidden_derivation(grammar_tuple[0])
            else:
                hidden_derivation = self.__add_hidden_derivation(grammar_tuple[0])
                if grammar_tuple[1] == '+':
                    hidden_name = self.__add_positive_closure(hidden_derivation)
                elif grammar_tuple[1] == '*':
                    hidden_name = self.__add_colin_closure(hidden_derivation)
                else:
                    raise ValueError('Invalid closure symbol: {}'.format(grammar_tuple[1]))
                return hidden_name
        elif reduce_number == 10:
            return grammar_tuple[0], None
        elif reduce_number == 11:
            return grammar_tuple
        elif reduce_number == 12:
            return grammar_tuple[0]
        elif reduce_number == 13:
            return [configure.boson_null_symbol]
        elif reduce_number == 14:
            return [configure.boson_null_symbol]
        elif reduce_number == 15:
            return [grammar_tuple[0]]
        elif reduce_number == 16:
            return grammar_tuple[0] + [grammar_tuple[1]]
        elif reduce_number == 17:
            return grammar_tuple[0]
        elif reduce_number == 18:
            literal = grammar_tuple[0]
            literal_string = literal[1: -1]
            if literal_string in self.__literal_map:
                literal_symbol = self.__literal_map[literal_string]
            else:
                literal_symbol = configure.boson_literal_template.format(self.__literal_number)
                self.__literal_number += 1
                self.__literal_map[literal_string] = literal_symbol
                self.__literal_reverse_map[literal_symbol] = literal_string
            return literal_symbol
        elif reduce_number == 19:
            if grammar_tuple[1] is None:
                return grammar_tuple[0]
            else:
                if grammar_tuple[1] == '+':
                    hidden_name = self.__add_positive_closure(grammar_tuple[0])
                elif grammar_tuple[1] == '*':
                    hidden_name = self.__add_colin_closure(grammar_tuple[0])
                else:
                    raise ValueError('Invalid closure symbol: {}'.format(grammar_tuple[1]))
                return hidden_name
        elif reduce_number == 20:
            return [grammar_tuple[0]]
        elif reduce_number == 21:
            return grammar_tuple[0] + [grammar_tuple[1]]
        elif reduce_number == 22:
            return grammar_tuple[0] + [grammar_tuple[1]]
        elif reduce_number == 23:
            return [grammar_tuple[0]]
        elif reduce_number == 24:
            grammar_name = '{}{}'.format(configure.boson_grammar_name_prefix, self.__temp_grammar_number)
            self.__temp_grammar_number += 1
            self.__temp_grammar_name_map[grammar_name] = grammar_tuple[0]
            return grammar_name
        elif reduce_number == 25:
            if grammar_tuple[0] in self.__grammar_name_map:
                raise ValueError('Grammar name duplicate: {}'.format(grammar_tuple[0]))
            self.__grammar_name_map[grammar_tuple[0]] = grammar_tuple[1]
            return grammar_tuple[0]
        elif reduce_number == 26:
            return grammar_tuple[0]
        elif reduce_number == 27:
            return grammar_tuple[0]
        elif reduce_number == 28:
            return grammar_tuple[0], tuple(grammar_tuple[1])
        elif reduce_number == 29:
            return grammar_tuple[0][1:]
        elif reduce_number == 30:
            return '*' + grammar_tuple[1][1:]
        elif reduce_number == 31:
            return [grammar_tuple[0]]
        elif reduce_number == 32:
            return grammar_tuple[0] + [grammar_tuple[1]]
        elif reduce_number == 33:
            name = grammar_tuple[0]
            derivation_list = grammar_tuple[1]
            for derivation in derivation_list:
                sentence = tuple([name] + derivation[0])
                self.__sentence_set.add(sentence)
                if len(sentence) < 3:
                    self.__naive_sentence.add(sentence)
                grammar_name = derivation[1]
                if grammar_name is None:
                    self.__sentence_grammar_map[sentence] = self.__grammar_number
                    self.__none_grammar_tuple_set.add(sentence)
                elif grammar_name.startswith(configure.boson_grammar_name_prefix):
                    self.__sentence_grammar_map[sentence] = self.__grammar_number
                    self.__grammar_tuple_map[sentence] = self.__temp_grammar_name_map[grammar_name]
                else:
                    self.__grammar_tuple_map[sentence] = tuple(self.__grammar_name_map[grammar_name])
                    self.__sentence_grammar_map[sentence] = grammar_name
                self.__grammar_number += 1
            return None
        elif reduce_number == 34:
            return grammar_tuple[0]
        elif reduce_number == 35:
            return grammar_tuple[0]

    def grammar_analysis(self, token_list):
        grammar = self.__bnf_grammar_analyzer.grammar_analysis(token_list)
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

    def semantic_analysis(self, grammar_tree):
        self.__init__()
        self.__semantic_analysis(grammar_tree)
        grammar_package = GrammarPackage()
        grammar_package.command_list = self.__command_list
        grammar_package.sentence_set = self.__sentence_set
        grammar_package.grammar_tuple_map = self.__grammar_tuple_map
        grammar_package.none_grammar_tuple_set = self.__none_grammar_tuple_set
        grammar_package.literal_map = self.__literal_map
        grammar_package.literal_reverse_map = self.__literal_reverse_map
        grammar_package.grammar_name_map = self.__grammar_name_map
        grammar_package.sentence_grammar_map = self.__sentence_grammar_map
        grammar_package.naive_sentence = self.__naive_sentence
        return grammar_package

    def parse(self, token_list):
        grammar_tree = self.grammar_analysis(token_list)
        grammar_package = self.semantic_analysis(grammar_tree)
        return grammar_package


def bs_grammar_analysis(text: str):
    token_list = bs_tokenize(text)
    script_analyzer = BosonScriptAnalyzer()
    grammar_package = script_analyzer.parse(token_list)
    return grammar_package
