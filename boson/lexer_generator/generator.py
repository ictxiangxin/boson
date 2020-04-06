from boson.lexer_generator.lexical_nfa import LexicalNFA
from boson.lexer_generator.regular_parser import RegularLexer
from boson.lexer_generator.regular_analyzer import BosonRegularAnalyzer
import boson.configure as configure


class LexerGenerator:
    def __init__(self, lexical_definition: dict):
        self.__lexical_definition: dict = dict(lexical_definition)
        self.__symbol_function_mapping: dict = {}
        self.__non_greedy_state_set: set = set()
        self.__lexical_dfa = None
        self.__compact_move_table: dict = {}

    def compact_move_table(self):
        return self.__compact_move_table

    def symbol_function_mapping(self):
        return self.__symbol_function_mapping

    def non_greedy_state_set(self):
        return self.__non_greedy_state_set

    def move_table(self) -> dict:
        return self.__lexical_dfa.move_table()

    def character_set(self) -> set:
        return self.__lexical_dfa.character_set()

    def start_state(self) -> int:
        return self.__lexical_dfa.start_state()

    def end_state_set(self) -> set:
        return self.__lexical_dfa.end_state_set()

    def lexical_symbol_mapping(self) -> dict:
        return self.__lexical_dfa.lexical_symbol_mapping()

    def generate_lexical_dfa(self) -> None:
        tokenizer = RegularLexer()
        reference_set = set()

        @tokenizer.register_function('reference')
        def _record_reference_symbol(token_string: str) -> str:
            reference_set.add(token_string[1:-1])
            return token_string

        reference_nfa_mapping = {}
        self.__symbol_function_mapping = {}
        self.__non_greedy_state_set = set()
        non_greedy_symbol_set = set()
        symbol_token_list_mapping = {}
        analyzer = BosonRegularAnalyzer(reference_nfa_mapping)
        nfa = LexicalNFA()
        for lexical_symbol, regular_definition in self.__lexical_definition.items():
            if regular_definition['function_list']:
                self.__symbol_function_mapping[lexical_symbol] = regular_definition['function_list']
            if regular_definition['non_greedy']:
                non_greedy_symbol_set.add(lexical_symbol)
            if tokenizer.tokenize(regular_definition['regular']) != tokenizer.no_error_index():
                raise ValueError('[Lexer Generator] Invalid Regular Expression: "{}".'.format(regular_definition[0]))
            symbol_token_list_mapping[lexical_symbol] = tokenizer.token_list()
        for lexical_symbol in reference_set:
            if lexical_symbol in symbol_token_list_mapping:
                reference_nfa_mapping[lexical_symbol] = analyzer.parse_to_lexical(symbol_token_list_mapping[lexical_symbol])
            else:
                raise ValueError('[Lexer Generator] Invalid Reference: "{}".'.format(lexical_symbol))
        for lexical_symbol, token_list in symbol_token_list_mapping.items():
            if not lexical_symbol.startswith(configure.boson_lexical_hidden_prefix):
                lexical_symbol_nfa = reference_nfa_mapping[lexical_symbol] if lexical_symbol in reference_nfa_mapping else analyzer.parse_to_lexical(token_list)
                nfa.add_lexical_symbol(lexical_symbol_nfa, lexical_symbol)
        nfa.construct()
        self.__lexical_dfa = nfa.transform_to_dfa()
        self.__lexical_dfa.minimize()
        for state, lexical_symbol in self.__lexical_dfa.lexical_symbol_mapping().items():
            if lexical_symbol in non_greedy_symbol_set:
                self.__non_greedy_state_set.add(state)

    def generate_compact_move_table(self) -> None:
        self.__compact_move_table = {}
        for from_state, move_table in self.__lexical_dfa.move_table().items():
            reverse_mapping = {}
            for character, to_state in move_table.items():
                reverse_mapping.setdefault(to_state, set())
                reverse_mapping[to_state].add(character)
            self.__compact_move_table.setdefault(from_state, [])
            for to_state, character_set in reverse_mapping.items():
                range_list = []
                scattered_character_set = set()
                scan_head = None
                scan = None
                reverse = False
                if configure.boson_lexical_wildcard in character_set:
                    if len(self.__lexical_dfa.character_set()) < 1.5 * len(character_set):
                        reverse = True
                        character_set = self.__lexical_dfa.character_set() - character_set
                for character in sorted(character_set - {configure.boson_lexical_wildcard}) + [configure.boson_lexical_reserved_character]:
                    if scan_head is None:
                        scan_head = character
                        scan = character
                    else:
                        if character == configure.boson_lexical_reserved_character or ord(character) - ord(scan) != 1:
                            if ord(scan) - ord(scan_head) > 1:
                                range_list.append((scan_head, scan))
                            else:
                                scattered_character_set.add(scan_head)
                                scattered_character_set.add(scan)
                            scan_head = character
                        scan = character
                has_wildcard = configure.boson_lexical_wildcard in character_set
                attribute = 0b00
                if reverse and not has_wildcard:
                    attribute = 0b10
                elif not reverse and has_wildcard:
                    attribute = 0b01
                self.__compact_move_table[from_state].append([attribute, scattered_character_set, range_list, to_state])
