from abc import abstractmethod
from typing import Optional, List, Dict, Tuple, Set, FrozenSet

import boson.configure as configure
from boson.boson_script.sentence_attribute import SentenceAttribute
from boson.option import option as boson_option
from boson.parser_generator.bottom_up_generator import BottomUpParserGenerator
from boson.system.logger import logger


class BottomUpCanonicalParserGenerator(BottomUpParserGenerator):
    def __init__(self, sentence_set: Set[Tuple[str, ...]], sentence_attribute_mapping: Dict[tuple, SentenceAttribute]):
        super().__init__(sentence_set, sentence_attribute_mapping)
        self._action_table: List[List[str]] = []
        self._sparse_action_table: Dict[int, Dict[int, str]] = {}
        self._goto_table: List[List[int]] = []
        self._sparse_goto_table: Dict[int, Dict[int, int]] = {}
        self._conflict_list: List[Tuple[int, int, str]] = []

    def action_table(self) -> List[List[str]]:
        return self._action_table

    def sparse_action_table(self) -> Dict[int, Dict[int, str]]:
        return self._sparse_action_table

    def goto_table(self) -> List[List[int]]:
        return self._goto_table

    def sparse_goto_table(self) -> Dict[int, Dict[int, int]]:
        return self._sparse_goto_table

    def conflict_list(self) -> List[Tuple[int, int, str]]:
        return self._conflict_list

    def initialize(self) -> None:
        super().initialize()
        self._generate_non_terminal_first_set()

    def generate_parse_table(self) -> None:
        logger.info('[Bottom-Up Canonical Parser Generator] Generate Parse Table.')
        conflict_resolver_enable: bool = boson_option['parser']['conflict_resolver']['enable'] == 'True'
        self._action_table: List[List[str]] = [[configure.boson_table_sign_error] * (len(self._terminal_index_mapping) + 1) for _ in range(len(self._dfa_state_number_mapping))]
        self._goto_table: List[List[int]] = [[configure.boson_invalid_goto] * len(self._non_terminal_index_mapping) for _ in range(len(self._dfa_state_number_mapping))]
        self._conflict_list: List[Tuple[int, int, str]] = []
        for state_number, state_move_table in self._dfa_move_table.items():
            for symbol, next_state in state_move_table.items():
                if symbol in self._terminal_index_mapping:
                    self._action_table[state_number][self._terminal_index_mapping[symbol]] = '{}{}'.format(configure.boson_table_sign_shift, next_state)
                else:
                    self._goto_table[state_number][self._non_terminal_index_mapping[symbol]] = next_state
        for state_number, reduce_terminal_set_mapping in self._dfa_state_reduce_mapping.items():
            for reduce_number, terminal_set in reduce_terminal_set_mapping.items():
                for terminal in terminal_set:
                    terminal_index: int = self._terminal_index_mapping[terminal]
                    if self._action_table[state_number][terminal_index] != configure.boson_table_sign_error:
                        old_action: str = self._action_table[state_number][terminal_index]
                        old_sign: str = old_action[0]
                        if old_sign in {configure.boson_table_sign_reduce, configure.boson_table_sign_accept}:
                            old_reduce_number: int = int(old_action[1:])
                            if old_reduce_number == reduce_number:
                                continue
                            if conflict_resolver_enable:
                                if boson_option['parser']['conflict_resolver']['reduce_reduce'] == 'order':
                                    sentence_attribute: SentenceAttribute = self._sentence_attribute_mapping[self._index_sentence_mapping[reduce_number]]
                                    old_sentence_attribute: SentenceAttribute = self._sentence_attribute_mapping[self._index_sentence_mapping[old_reduce_number]]
                                    if sentence_attribute.order < old_sentence_attribute.order:
                                        self._action_table[state_number][terminal_index] = '{}{}'.format(configure.boson_table_sign_reduce, reduce_number)
                                else:
                                    old_shorter: bool = len(self._index_sentence_mapping[old_reduce_number]) < len(self._index_sentence_mapping[reduce_number])
                                    longer: bool = boson_option['parser']['conflict_resolver']['reduce_reduce'] == 'long'
                                    if not (old_shorter ^ longer):
                                        self._action_table[state_number][terminal_index] = '{}{}'.format(configure.boson_table_sign_reduce, reduce_number)
                            else:
                                self._conflict_list.append((state_number, configure.boson_conflict_reduce_reduce, terminal))
                        elif old_sign == configure.boson_table_sign_shift:
                            if conflict_resolver_enable:
                                if boson_option['parser']['conflict_resolver']['reduce_reduce'] == 'order':
                                    reduce_sentence: Tuple[str, ...] = self._index_sentence_mapping[reduce_number]
                                    nfa_state_number_set: FrozenSet[int] = self._dfa_state_number_inverted_mapping[state_number]
                                    for nfa_state_number in nfa_state_number_set:
                                        nfa_sentence, nfa_flag, _ = self._nfa_state_number_inverted_mapping[nfa_state_number]
                                        if nfa_flag < len(nfa_sentence) and nfa_sentence[nfa_flag] == terminal:
                                            reduce_sentence_attribute = self._sentence_attribute_mapping[reduce_sentence]
                                            nfa_sentence_attribute = self._sentence_attribute_mapping[nfa_sentence]
                                            if reduce_sentence_attribute.order < nfa_sentence_attribute.order:
                                                self._action_table[state_number][terminal_index] = '{}{}'.format(configure.boson_table_sign_reduce, reduce_number)
                                                break
                                elif boson_option['parser']['conflict_resolver']['shift_reduce'] == 'reduce':
                                    self._action_table[state_number][terminal_index] = '{}{}'.format(configure.boson_table_sign_reduce, reduce_number)
                            else:
                                self._conflict_list.append((state_number, configure.boson_conflict_shift_reduce, terminal))
                        else:
                            raise ValueError('[Bottom-Up Canonical Parser Generator] Invalid Action: {}'.format(old_action))
                        if not conflict_resolver_enable:
                            self._action_table[state_number][terminal_index] += '/{}{}'.format(configure.boson_table_sign_reduce, reduce_number)
                    else:
                        if reduce_number == 0:
                            self._action_table[state_number][terminal_index] = configure.boson_table_sign_accept
                        else:
                            self._action_table[state_number][terminal_index] = '{}{}'.format(configure.boson_table_sign_reduce, reduce_number)

    def parse_table_sparsification(self) -> None:
        logger.info('[Bottom-Up Canonical Parser Generator] Parse Table Sparsification.')
        self._sparse_action_table: Dict[int, Dict[int, str]] = {}
        for state, state_action_table in enumerate(self._action_table):
            sparse_state_action_table = {}
            for terminal_index, action in enumerate(state_action_table):
                if action != configure.boson_table_sign_error:
                    sparse_state_action_table[terminal_index] = action
            if sparse_state_action_table:
                self._sparse_action_table[state] = sparse_state_action_table
        self._sparse_goto_table = {}
        for state, state_goto_table in enumerate(self._goto_table):
            sparse_state_goto_table = {}
            for non_terminal_index, goto_state in enumerate(state_goto_table):
                if goto_state != configure.boson_invalid_goto:
                    sparse_state_goto_table[non_terminal_index] = goto_state
            if sparse_state_goto_table:
                self._sparse_goto_table[state] = sparse_state_goto_table

    @abstractmethod
    def _non_terminal_look_ahead_set(self, sentence: Tuple[str, ...], flag: int, look_ahead_set: Set[str] | FrozenSet[str]) -> Optional[FrozenSet[str]]:
        pass

    @abstractmethod
    def _end_processing(self) -> None:
        pass
