from boson.lexer_generator.regular_parser import \
    BosonGrammarNode, \
    RegularParser, \
    RegularInterpreter
from boson.lexer_generator.lexical_nfa import \
    LexicalNFA, \
    bs_create_nfa_character, \
    bs_create_nfa_or, \
    bs_create_nfa_count_range, \
    bs_create_nfa_kleene_closure, \
    bs_create_nfa_plus_closure, \
    bs_create_nfa_link, \
    bs_create_nfa_reverse_delay_construct


interpreter = RegularInterpreter()


class BosonRegularAnalyzer:
    def __init__(self, reference_nfa_mapping: dict = None):
        self.__parser: RegularParser = RegularParser()
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
        @interpreter.register_action('regular_expression')
        def _semantic_regular_expression(semantic_node_list):
            self.__lexical_nfa = semantic_node_list[0]

        @interpreter.register_action('group')
        def _semantic_group(semantic_node_list):
            if len(semantic_node_list) == 1:
                return semantic_node_list[0]
            elif len(semantic_node_list) == 2:
                nfa, postfix = semantic_node_list
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

        @interpreter.register_action('construct_number')
        def _semantic_construct_number(semantic_node_list):
            return ''.join(semantic_node_list)

        @interpreter.register_action('simple_construct')
        def _semantic_character(semantic_node_list):
            character = semantic_node_list[0]
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

        @interpreter.register_action('select')
        def _semantic_select(semantic_node_list):
            reverse = False
            select_list = semantic_node_list[0]
            if len(semantic_node_list) == 2:
                reverse = True
                select_list = semantic_node_list[1]
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

        @interpreter.register_action('branch')
        def _semantic_branch(semantic_node_list):
            return bs_create_nfa_link(semantic_node_list)

        @interpreter.register_action('expression')
        def _semantic_expression(semantic_node_list):
            if len(semantic_node_list) > 1:
                return bs_create_nfa_or(semantic_node_list)
            else:
                return semantic_node_list[0]

        @interpreter.register_action('wildcard_character')
        def _semantic_wildcard_character(semantic_node_list):
            return bs_create_nfa_reverse_delay_construct(set())

        @interpreter.register_action('complex_construct')
        def _semantic_complex_construct(semantic_node_list):
            return semantic_node_list[0]

        @interpreter.register_action('sub_expression')
        def _semantic_sub_expression(semantic_node_list):
            return semantic_node_list[0]

        @interpreter.register_action('reference')
        def _semantic_reference(semantic_node_list):
            lexical_symbol = semantic_node_list[0][1:-1]
            if lexical_symbol in self.__reference_nfa_mapping:
                return self.__reference_nfa_mapping[lexical_symbol]
            else:
                raise ValueError('[Boson Regular Analyzer] Circular Reference.')

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
            error_message = '\n[Boson Regular Analyzer] Syntax Error [Line: {}] \n'.format(error_line)
            error_token_text_list = [token.text for token in error_token_list]
            error_message += '{}\n'.format(' '.join(error_token_text_list))
            error_message += ' ' * (sum([len(text) for text in error_token_text_list[:offset]]) + offset) + '^' * len(error_token_text_list[offset])
            raise ValueError(error_message)

    def parse_to_lexical(self, token_list: list) -> LexicalNFA:
        self.init_semantic()
        interpreter.execute(self.parse(token_list))
        return self.__lexical_nfa