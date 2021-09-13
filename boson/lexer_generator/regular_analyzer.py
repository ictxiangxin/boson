from boson.lexer_generator.regular_parser import \
    BosonGrammarNode, \
    RegularParser, \
    RegularInterpreter, \
    BosonSemanticsNode
from boson.lexer_generator.lexical_nfa import \
    LexicalNFA, \
    bs_create_nfa_character, \
    bs_create_nfa_character_set, \
    bs_create_nfa_or, \
    bs_create_nfa_count_range, \
    bs_create_nfa_kleene_closure, \
    bs_create_nfa_plus_closure, \
    bs_create_nfa_link, \
    bs_create_nfa_reverse_delay_construct


interpreter = RegularInterpreter()


def get_semantic_node_text_list(semantic_node: BosonSemanticsNode) -> list:
    return [node.get_text() for node in semantic_node.children()]


def get_semantic_node_data_list(semantic_node: BosonSemanticsNode) -> list:
    return [node.get_data() for node in semantic_node.children()]


class BosonRegularAnalyzer:
    def __init__(self, reference_nfa_mapping: dict = None):
        self.__parser: RegularParser = RegularParser()
        self.__escape_character_mapping: dict = {
            'n': {'\n'},
            'r': {'\r'},
            't': {'\t'},
            'd': {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'},
            'w': {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
            'W': {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}
        }
        self.__lexical_nfa: (LexicalNFA, None) = None
        self.__reference_nfa_mapping: dict = {}
        if reference_nfa_mapping is not None:
            self.__reference_nfa_mapping = reference_nfa_mapping

    def init_semantic(self):
        @interpreter.register_action('regular_expression')
        def _semantic_regular_expression(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            self.__lexical_nfa = semantic_node[0].get_data()
            return BosonSemanticsNode.null_node()

        @interpreter.register_action('group')
        def _semantic_group(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            if len(semantic_node.children()) == 1:
                return semantic_node[0]
            elif len(semantic_node.children()) == 2:
                nfa = semantic_node[0].get_data()
                postfix = semantic_node[1]
                if len(postfix.children()) > 0:
                    min_count = int(postfix[0].get_text())
                    if len(postfix.children()) == 1:
                        if min_count == 0:
                            return BosonSemanticsNode(bs_create_nfa_kleene_closure(nfa))
                        elif min_count == 1:
                            return BosonSemanticsNode(bs_create_nfa_plus_closure(nfa))
                        else:
                            return BosonSemanticsNode(bs_create_nfa_link([bs_create_nfa_count_range(nfa, min_count, min_count), bs_create_nfa_kleene_closure(nfa)]))
                    max_count = int(postfix[1].get_text())
                    if min_count > max_count:
                        raise ValueError('[Boson Regular Analyzer] Min Count Must Less Than Max Count.')
                    return BosonSemanticsNode(bs_create_nfa_count_range(nfa, min_count, max_count))
                elif len(postfix.children()) == 0:
                    if postfix.get_text() == '*':
                        return BosonSemanticsNode(bs_create_nfa_kleene_closure(nfa))
                    elif postfix.get_text() == '+':
                        return BosonSemanticsNode(bs_create_nfa_plus_closure(nfa))
                    elif postfix.get_text() == '?':
                        return BosonSemanticsNode(bs_create_nfa_count_range(nfa, 0, 1))
                    else:
                        raise RuntimeError('[Boson Regular Analyzer] Never Touch Here.')
                else:
                    raise RuntimeError('[Boson Regular Analyzer] Never Touch Here.')
            else:
                raise RuntimeError('[Boson Regular Analyzer] Never Touch Here.')

        @interpreter.register_action('construct_number')
        def _semantic_construct_number(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            return BosonSemanticsNode(''.join(get_semantic_node_text_list(semantic_node)))

        @interpreter.register_action('simple_construct')
        def _semantic_character(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            character = semantic_node[0].get_text()
            if len(character) > 1 and character[0] == '\\':
                escape_character = character[1]
                return BosonSemanticsNode(bs_create_nfa_character_set(self.__escape_character_mapping.get(escape_character, {escape_character})))
            else:
                return BosonSemanticsNode(bs_create_nfa_character(character))

        @interpreter.register_action('select')
        def _semantic_select(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            if (len(semantic_node.children())) == 1:
                reverse = False
                select_list = semantic_node[0]
            else:
                reverse = True
                select_list = semantic_node[1]
            select_character_set = set()
            for each_select in select_list.children():
                if len(each_select.children()) == 0:
                    character = each_select.get_text()
                    if character[0] == '\\':
                        escape_character = character[1]
                        if escape_character in self.__escape_character_mapping:
                            select_character_set |= set(self.__escape_character_mapping[escape_character])
                        else:
                            select_character_set.add(escape_character)
                    else:
                        select_character_set.add(character[0])
                elif len(each_select.children()) == 2:
                    start_unicode, end_unicode = ord(each_select[0].get_text()), ord(each_select[1].get_text())
                    if start_unicode <= end_unicode:
                        character_range_set = set()
                        while start_unicode <= end_unicode:
                            character_range_set.add(chr(start_unicode))
                            start_unicode += 1
                        select_character_set |= character_range_set
                    else:
                        raise ValueError('[Boson Regular Analyzer] Character range invalid: <{}-{}>.'.format(each_select[0].get_text(), each_select[1].get_text()))
                else:
                    raise RuntimeError('[Boson Regular Analyzer] Never Touch Here.')
            if reverse:
                return BosonSemanticsNode(bs_create_nfa_reverse_delay_construct(select_character_set))
            else:
                return BosonSemanticsNode(bs_create_nfa_character_set(select_character_set))

        @interpreter.register_action('branch')
        def _semantic_branch(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            return BosonSemanticsNode(bs_create_nfa_link(get_semantic_node_data_list(semantic_node)))

        @interpreter.register_action('expression')
        def _semantic_expression(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            if len(semantic_node.children()) > 1:
                return BosonSemanticsNode(bs_create_nfa_or(get_semantic_node_data_list(semantic_node)))
            else:
                return semantic_node[0]

        @interpreter.register_action('wildcard_character')
        def _semantic_wildcard_character(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            return BosonSemanticsNode(bs_create_nfa_reverse_delay_construct(set()))

        @interpreter.register_action('reference')
        def _semantic_reference(semantic_node: BosonSemanticsNode) -> BosonSemanticsNode:
            lexical_symbol = semantic_node[0].get_text()[1:-1]
            if lexical_symbol in self.__reference_nfa_mapping:
                return BosonSemanticsNode(self.__reference_nfa_mapping[lexical_symbol])
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
