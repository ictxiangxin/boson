from typing import Optional, List, Dict, Tuple, Set

import boson.configure as configure
from boson.lexer_generator.lexical_dfa import LexicalDFA
from boson.lexer_generator.lexical_nfa import LexicalNFA
from boson.lexer_generator.regular_analyzer import BosonRegularAnalyzer
from boson.lexer_generator.regular_parser import RegularLexer
from boson.system.logger import logger


class LexerGenerator:
    def __init__(self, lexical_definition: Dict[str, Dict[str, str | int | bool | Optional[List[str]]]]):
        self.__lexical_definition: Dict[str, Dict[str, str | int | bool | Optional[List[str]]]] = dict(lexical_definition)
        self.__symbol_function_mapping: Dict[str, List[str]] = {}
        self.__non_greedy_state_set: Set[int] = set()
        self.__lexical_dfa: Optional[LexicalDFA] = None
        self.__compact_move_table: Dict[int, List[list]] = {}

    def compact_move_table(self) -> Dict[int, List[list]]:
        return self.__compact_move_table

    def symbol_function_mapping(self) -> Dict[str, List[str]]:
        return self.__symbol_function_mapping

    def non_greedy_state_set(self) -> Set[int]:
        return self.__non_greedy_state_set

    def move_table(self) -> Dict[int, Dict[str, int]]:
        return self.__lexical_dfa.move_table()

    def character_set(self) -> Set[str]:
        return self.__lexical_dfa.character_set()

    def start_state(self) -> int:
        return self.__lexical_dfa.start_state()

    def end_state_set(self) -> Set[int]:
        return self.__lexical_dfa.end_state_set()

    def lexical_symbol_mapping(self) -> Dict[int, str]:
        return self.__lexical_dfa.lexical_symbol_mapping()

    def generate_lexical_dfa(self) -> None:
        logger.info('[Lexer Generator] Generate Lexical DFA.')
        tokenizer: RegularLexer = RegularLexer()
        reference_set: Set[str] = set()

        @tokenizer.register_function('reference')
        def _record_reference_symbol(token_string: str) -> str:
            reference_set.add(token_string[1:-1])
            return token_string

        reference_nfa_mapping: Dict[str, LexicalNFA] = {}
        self.__symbol_function_mapping: Dict[str, List[str]] = {}
        self.__non_greedy_state_set: Set[int] = set()
        non_greedy_symbol_set: Set[str] = set()
        symbol_token_list_mapping: Dict[str, list] = {}
        analyzer: BosonRegularAnalyzer = BosonRegularAnalyzer(reference_nfa_mapping)
        nfa: LexicalNFA = LexicalNFA()
        for lexical_symbol, regular_definition in self.__lexical_definition.items():
            if regular_definition['function_list']:
                self.__symbol_function_mapping[lexical_symbol] = regular_definition['function_list']
            if regular_definition['non_greedy']:
                non_greedy_symbol_set.add(lexical_symbol)
            tokenizer_error_index: int = tokenizer.tokenize(regular_definition['regular'])
            if tokenizer_error_index != tokenizer.no_error_index():
                raise ValueError('[Lexer Generator] Invalid Regular Expression: "{}", Error Index: {}'.format(regular_definition['regular'], tokenizer_error_index))
            symbol_token_list_mapping[lexical_symbol] = tokenizer.token_list()
        for lexical_symbol in reference_set:
            if lexical_symbol in symbol_token_list_mapping:
                reference_nfa_mapping[lexical_symbol] = analyzer.parse_to_lexical(symbol_token_list_mapping[lexical_symbol])
            else:
                raise ValueError('[Lexer Generator] Invalid Reference: "{}".'.format(lexical_symbol))
        for lexical_symbol, token_list in symbol_token_list_mapping.items():
            if not lexical_symbol.startswith(configure.boson_lexical_hidden_prefix):
                lexical_symbol_nfa: LexicalNFA = reference_nfa_mapping[lexical_symbol] if lexical_symbol in reference_nfa_mapping else analyzer.parse_to_lexical(token_list)
                nfa.add_lexical_symbol(lexical_symbol_nfa, (lexical_symbol, self.__lexical_definition[lexical_symbol].get('number', None)))
        nfa.construct()
        self.__lexical_dfa: LexicalDFA = nfa.transform_to_dfa()
        self.__lexical_dfa.minimize()
        for state, lexical_symbol in self.__lexical_dfa.lexical_symbol_mapping().items():
            if lexical_symbol in non_greedy_symbol_set:
                self.__non_greedy_state_set.add(state)

    def generate_compact_move_table(self) -> None:
        logger.info('[Lexer Generator] Generate Compact Move Table.')
        self.__compact_move_table: Dict[int, List[list]] = {}
        for from_state, move_table in self.__lexical_dfa.move_table().items():
            reverse_mapping: Dict[int, Set[str]] = {}
            for character, to_state in move_table.items():
                reverse_mapping.setdefault(to_state, set())
                reverse_mapping[to_state].add(character)
            self.__compact_move_table.setdefault(from_state, [])
            for to_state, character_set in reverse_mapping.items():
                range_list: List[Tuple[str, str]] = []
                scattered_character_set: Set[str] = set()
                scan_head: Optional[str] = None
                scan: Optional[str] = None
                reverse: bool = False
                if configure.boson_lexical_wildcard in character_set:
                    if len(self.__lexical_dfa.character_set()) < 1.5 * len(character_set):
                        reverse: bool = True
                        character_set = self.__lexical_dfa.character_set() - character_set
                for character in sorted(character_set - {configure.boson_lexical_wildcard}) + [configure.boson_lexical_reserved_character]:
                    if scan_head is None:
                        scan_head: str = character
                        scan: str = character
                    else:
                        if character == configure.boson_lexical_reserved_character or ord(character) - ord(scan) != 1:
                            if ord(scan) - ord(scan_head) > 1:
                                range_list.append((scan_head, scan))
                            else:
                                scattered_character_set.add(scan_head)
                                scattered_character_set.add(scan)
                            scan_head: str = character
                        scan: str = character
                has_wildcard: bool = configure.boson_lexical_wildcard in character_set
                attribute: int = 0b00
                if reverse and not has_wildcard:
                    attribute: int = 0b10
                elif not reverse and has_wildcard:
                    attribute: int = 0b01
                self.__compact_move_table[from_state].append([attribute, scattered_character_set, range_list, to_state])
