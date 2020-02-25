from boson.lexer_generator.regular_parser import \
    BosonGrammarNode, \
    RegularAnalyzer, \
    RegularSemanticsAnalyzer
from boson.lexer_generator.lexical_nfa import \
    LexicalNFA, \
    bs_create_nfa_character, \
    bs_create_nfa_or, \
    bs_create_nfa_count_range, \
    bs_create_nfa_kleene_closure, \
    bs_create_nfa_plus_closure, \
    bs_create_nfa_link, \
    bs_create_nfa_reverse_delay_construct


semantic_analyzer = RegularSemanticsAnalyzer()


class BosonRegularAnalyzer:
    def __init__(self, reference_nfa_mapping: dict = None):
        self.__grammar_analyzer: RegularAnalyzer = RegularAnalyzer()
        self.__escape_character_mapping: dict = {
            'n': '\n',
            'r': '\r',
            't': '\t',
            'd': '0123456789',
            'w': 'abcdefghijklmnopqrstuvwxyz',
            'W': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        }
        self.__lexical_nfa: (LexicalNFA, None) = None
        self.__reference_nfa_mapping: dict = {}
        if reference_nfa_mapping is not None:
            self.__reference_nfa_mapping = reference_nfa_mapping

    def init_semantic(self):
        @semantic_analyzer.semantics_entity('regular_expression')
        def _semantic_regular_expression(grammar_entity):
            self.__lexical_nfa = grammar_entity[0]

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
                        raise RuntimeError('[Boson Regular Analyzer] Never Touch Here.')
                else:
                    raise RuntimeError('[Boson Regular Analyzer] Never Touch Here.')
            else:
                raise RuntimeError('[Boson Regular Analyzer] Never Touch Here.')

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
                        raise ValueError('[Boson Regular Analyzer] Character range invalid: <{}-{}>.'.format(each_select[0], each_select[1]))
                else:
                    raise RuntimeError('[Boson Regular Analyzer] Never Touch Here.')
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
            if lexical_symbol in self.__reference_nfa_mapping:
                return self.__reference_nfa_mapping[lexical_symbol]
            else:
                raise ValueError('[Boson Regular Analyzer] Circular Reference.')

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
            error_message = '\n[Boson Regular Analyzer] Syntax Error [Line: {}] \n'.format(error_line)
            error_token_text_list = [token.text for token in error_token_list]
            error_message += '{}\n'.format(' '.join(error_token_text_list))
            error_message += ' ' * (sum([len(text) for text in error_token_text_list[:offset]]) + offset) + '^' * len(error_token_text_list[offset])
            raise ValueError(error_message)

    def parse_to_lexical(self, token_list: list) -> LexicalNFA:
        self.init_semantic()
        semantic_analyzer.semantics_analysis(self.grammar_analysis(token_list))
        return self.__lexical_nfa
