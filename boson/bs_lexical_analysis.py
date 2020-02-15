import boson.bs_configure as configure
from boson.bs_regular_expression_analyzer import BosonGrammarNode, RegularExpressionLexicalAnalyzer, RegularExpressionAnalyzer, RegularExpressionSemanticsAnalyzer
from boson.bs_lexical_generate import LexicalNFA, bs_create_nfa_character, bs_create_nfa_or, bs_create_nfa_count_range, bs_create_nfa_kleene_closure, bs_create_nfa_plus_closure, bs_create_nfa_link, bs_create_nfa_reverse_delay_construct
from boson.bs_data_package import LexicalPackage


semantic_analyzer = RegularExpressionSemanticsAnalyzer()


class BosonRegularExpressionAnalyzer:
    def __init__(self, symbol_regular_mapping: dict = None, symbol_nfa_mapping: dict = None):
        self.__grammar_analyzer: RegularExpressionAnalyzer = RegularExpressionAnalyzer()
        self.__escape_character_mapping: dict = {
            'n': '\n',
            'r': '\r',
            't': '\t',
            'd': '0123456789',
            'w': 'abcdefghijklmnopqrstuvwxyz',
            'W': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        }
        self.__nfa: (LexicalNFA, None) = None
        self.__symbol_regular_mapping: dict = {}
        self.__symbol_nfa_mapping: dict = {}
        if symbol_regular_mapping is not None:
            self.__symbol_regular_mapping = symbol_regular_mapping
        if symbol_nfa_mapping is not None:
            self.__symbol_nfa_mapping = symbol_nfa_mapping

    def init_semantic(self):
        @semantic_analyzer.semantics_entity('regular_expression')
        def _semantic_regular_expression(grammar_entity):
            self.__nfa = grammar_entity[0]

        @semantic_analyzer.semantics_entity('group')
        def _semantic_group(grammar_entity):
            if len(grammar_entity) == 1:
                return grammar_entity[0]
            elif len(grammar_entity) == 2:
                nfa, postfix = grammar_entity
                if isinstance(postfix, list):
                    return bs_create_nfa_count_range(nfa, int(postfix[0]), int(postfix[1]))
                elif isinstance(postfix, str):
                    if postfix == '*':
                        return bs_create_nfa_kleene_closure(nfa)
                    elif postfix == '+':
                        return bs_create_nfa_plus_closure(nfa)
                    elif postfix == '?':
                        return bs_create_nfa_count_range(nfa, 0, 1)
                    else:
                        raise RuntimeError('Never touch here.')
                else:
                    raise RuntimeError('Never touch here.')
            else:
                raise RuntimeError('Never touch here.')

        @semantic_analyzer.semantics_entity('construct_number')
        def _semantic_construct_number(grammar_entity):
            return ''.join(grammar_entity)

        @semantic_analyzer.semantics_entity('simple_construct')
        def _semantic_character(grammar_entity):
            character = grammar_entity[0]
            if len(character) > 1 and character[0] == '\\':
                escape_character = character[1]
                if escape_character in self.__escape_character_mapping:
                    mapping_character = self.__escape_character_mapping[escape_character]
                    if len(mapping_character) > 1:
                        nfa_list = []
                        for character in mapping_character:
                            nfa_list.append(bs_create_nfa_character(character))
                        return bs_create_nfa_or(nfa_list)
                    else:
                        return bs_create_nfa_character(mapping_character)
                else:
                    return bs_create_nfa_character(escape_character)
            else:
                return bs_create_nfa_character(character)

        @semantic_analyzer.semantics_entity('select')
        def _semantic_select(grammar_entity):
            reverse = False
            select_list = grammar_entity[0]
            if len(grammar_entity) == 2:
                reverse = True
                select_list = grammar_entity[1]
            select_character_set = set()
            for each_select in select_list:
                if isinstance(each_select, str):
                    if each_select[0] == '\\':
                        escape_character = each_select[1]
                        if escape_character in self.__escape_character_mapping:
                            select_character_set |= set(self.__escape_character_mapping[escape_character])
                        else:
                            select_character_set.add(escape_character)
                    else:
                        select_character_set.add(each_select[0])
                elif isinstance(each_select, list):
                    start_ascii, end_ascii = (ord(each_select[0]), ord(each_select[1]))
                    if start_ascii <= end_ascii:
                        character_range_set = set()
                        while start_ascii <= end_ascii:
                            character_range_set.add(chr(start_ascii))
                            start_ascii += 1
                        select_character_set |= character_range_set
                    else:
                        raise ValueError('Character range invalid.')
                else:
                    raise RuntimeError('Never touch here.')
            if reverse:
                return bs_create_nfa_reverse_delay_construct(select_character_set)
            else:
                nfa_list = []
                for character in select_character_set:
                    nfa_list.append(bs_create_nfa_character(character))
                return bs_create_nfa_or(nfa_list)

        @semantic_analyzer.semantics_entity('branch')
        def _semantic_branch(grammar_entity):
            return bs_create_nfa_link(grammar_entity)

        @semantic_analyzer.semantics_entity('expression')
        def _semantic_expression(grammar_entity):
            if len(grammar_entity) > 1:
                return bs_create_nfa_or(grammar_entity)
            else:
                return grammar_entity[0]

        @semantic_analyzer.semantics_entity('wildcard_character')
        def _semantic_wildcard_character(grammar_entity):
            return bs_create_nfa_reverse_delay_construct(set())

        @semantic_analyzer.semantics_entity('complex_construct')
        def _semantic_complex_construct(grammar_entity):
            return grammar_entity[0]

        @semantic_analyzer.semantics_entity('sub_expression')
        def _semantic_sub_expression(grammar_entity):
            return grammar_entity[0]

        @semantic_analyzer.semantics_entity('reference')
        def _semantic_reference(grammar_entity):
            lexical_symbol = grammar_entity[0][1:-1]
            if lexical_symbol in self.__symbol_nfa_mapping:
                return self.__symbol_nfa_mapping[lexical_symbol]
            elif lexical_symbol in self.__symbol_regular_mapping:
                regular_expression = self.__symbol_regular_mapping[lexical_symbol][0]
                reference_nfa = bs_regular_expression_to_nfa(regular_expression, self.__symbol_regular_mapping, self.__symbol_nfa_mapping)
                self.init_semantic()
                self.__symbol_nfa_mapping[lexical_symbol] = reference_nfa
                return reference_nfa
            else:
                raise ValueError('Regular Expression Invalid Reference: "{}"'.format(lexical_symbol))

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
            error_message = '\nRegular Expression Grammar Error [Line: {}] \n'.format(error_line)
            error_token_text_list = [token.text for token in error_token_list]
            error_message += '{}\n'.format(' '.join(error_token_text_list))
            error_message += ' ' * (sum([len(text) for text in error_token_text_list[:offset]]) + offset) + '^' * len(error_token_text_list[offset])
            raise ValueError(error_message)

    def semantics_analysis(self, grammar_tree: BosonGrammarNode) -> LexicalNFA:
        self.__init__(self.__symbol_regular_mapping, self.__symbol_nfa_mapping)
        self.init_semantic()
        semantic_analyzer.semantics_analysis(grammar_tree)
        return self.__nfa

    def parse(self, token_list) -> LexicalNFA:
        grammar_tree = self.grammar_analysis(token_list)
        regular_expression_nfa = self.semantics_analysis(grammar_tree)
        return regular_expression_nfa


def bs_regular_expression_to_nfa(text: str, symbol_regular_mapping: dict = None, symbol_nfa_mapping: dict = None) -> LexicalNFA:
    tokenizer = RegularExpressionLexicalAnalyzer()
    if tokenizer.tokenize(text) != tokenizer.no_error_line():
        raise ValueError('Regular Expression Invalid: "{}"'.format(text))
    token_list = tokenizer.token_list()
    script_analyzer = BosonRegularExpressionAnalyzer(symbol_regular_mapping, symbol_nfa_mapping)
    regular_expression_nfa = script_analyzer.parse(token_list)
    return regular_expression_nfa


def bs_lexical_analysis(lexical_regular_expression: dict) -> LexicalPackage:
    lexical_package = LexicalPackage()
    nfa = LexicalNFA()
    symbol_function_mapping = {}
    non_greedy_symbol_set = set()
    symbol_nfa_mapping = {}
    for lexical_symbol, regular_expression in lexical_regular_expression.items():
        if not lexical_symbol.startswith(configure.boson_lexical_hidden_prefix):
            if len(regular_expression) > 1:
                function_list = None
                if isinstance(regular_expression[1], list):
                    function_list = regular_expression[1]
                else:
                    non_greedy_symbol_set.add(lexical_symbol)
                if len(regular_expression) == 3:
                    function_list = regular_expression[2]
                if function_list is not None:
                    symbol_function_mapping[lexical_symbol] = function_list
            if lexical_symbol in symbol_nfa_mapping:
                nfa.add_lexical_symbol(symbol_nfa_mapping[lexical_symbol], lexical_symbol)
            else:
                new_nfa = bs_regular_expression_to_nfa(regular_expression[0], lexical_regular_expression, symbol_nfa_mapping)
                symbol_nfa_mapping[lexical_symbol] = new_nfa
                nfa.add_lexical_symbol(new_nfa, lexical_symbol)
    nfa.construct()
    dfa = nfa.transform_to_dfa()
    dfa.minimize()
    dfa.simplify()
    non_greedy_state_set = set()
    for state, lexical_symbol in dfa.lexical_symbol_mapping().items():
        if lexical_symbol in non_greedy_symbol_set:
            non_greedy_state_set.add(state)
    lexical_package.move_table = dfa.move_table()
    lexical_package.compact_move_table = dfa.compact_move_table()
    lexical_package.start_state = dfa.start_state()
    lexical_package.end_state_set = dfa.end_state_set()
    lexical_package.character_set = dfa.character_set()
    lexical_package.lexical_symbol_mapping = dfa.lexical_symbol_mapping()
    lexical_package.symbol_function_mapping = symbol_function_mapping
    lexical_package.non_greedy_state_set = non_greedy_state_set
    return lexical_package
