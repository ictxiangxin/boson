from typing import Optional, Dict, Tuple, Set, FrozenSet

import boson.configure as configure
from boson.boson_script.sentence_attribute import SentenceAttribute
from boson.parser_generator.bottom_up_generator import BottomUpCanonicalParserGenerator


class LALRParserGenerator(BottomUpCanonicalParserGenerator):
    def __init__(self, sentence_set: Set[Tuple[str, ...]], sentence_attribute_mapping: Dict[Tuple[str, ...], SentenceAttribute]):
        super().__init__(sentence_set, sentence_attribute_mapping)

    def _non_terminal_look_ahead_set(self, sentence: Tuple[str, ...], flag: int, look_ahead_set: Set[str] | FrozenSet[str]) -> Optional[FrozenSet[str]]:
        if sentence[0] == configure.boson_augmented_start:
            return frozenset(look_ahead_set)
        else:
            return None

    def _end_processing(self) -> None:
        null_right_sentence_dfa_nfa_set: Set[Tuple[int, int]] = set()
        dfa_state_channel_look_ahead_mapping: Dict[int, Dict[str]] = {}
        dfa_state_nfa_state_look_ahead_mapping: Dict[int, Dict[int, Set[str]]] = {}
        channel_look_ahead_count: int = 0
        nfa_state_look_ahead_count: int = 0
        continue_loop: bool = True
        for dfa_state, dfa_state_number in self._dfa_state_number_mapping.items():
            dfa_state_nfa_state_look_ahead_mapping.setdefault(dfa_state_number, {})
            dfa_state_channel_look_ahead_mapping.setdefault(dfa_state_number, {})
            channel_look_ahead_set_mapping = dfa_state_channel_look_ahead_mapping[dfa_state_number]
            for nfa_state_number in dfa_state:
                sentence, flag, look_ahead_set = self._nfa_state_number_inverted_mapping[nfa_state_number]
                flag_symbol: Optional[str] = sentence[flag] if flag < len(sentence) else None
                if flag_symbol in self._non_terminal_set:
                    if flag > 0:
                        first_set = self._sentence_first_set(sentence[flag + 1:])
                        if configure.boson_null_symbol in first_set:
                            first_set.remove(configure.boson_null_symbol)
                            null_right_sentence_dfa_nfa_set.add((dfa_state_number, nfa_state_number))
                        if look_ahead_set is not None:
                            first_set |= look_ahead_set
                        channel_look_ahead_set = first_set
                    else:
                        channel_look_ahead_set = set() if look_ahead_set is None else look_ahead_set
                    channel_look_ahead_set_mapping.setdefault(flag_symbol, set())
                    channel_look_ahead_set_mapping[flag_symbol] |= channel_look_ahead_set
        while continue_loop:
            continue_loop: bool = False
            for dfa_state, dfa_state_number in self._dfa_state_number_mapping.items():
                nfa_state_number_look_ahead_mapping: Dict[int, Set[str]] = dfa_state_nfa_state_look_ahead_mapping[dfa_state_number]
                channel_look_ahead_set_mapping: Dict[str] = dfa_state_channel_look_ahead_mapping[dfa_state_number]
                for nfa_state_number in dfa_state:
                    sentence, flag, _ = self._nfa_state_number_inverted_mapping[nfa_state_number]
                    if flag > 0:
                        nfa_state_number_look_ahead_mapping.setdefault(nfa_state_number, set())
                        nfa_state_number_look_ahead_mapping[nfa_state_number] |= channel_look_ahead_set_mapping.get(sentence[0], set())
                for nfa_state_number in dfa_state:
                    sentence, flag, look_ahead_set = self._nfa_state_number_inverted_mapping[nfa_state_number]
                    if 0 < flag < len(sentence) and sentence[flag] in self._non_terminal_set:
                        if flag == len(sentence) - 1 or (dfa_state_number, nfa_state_number) in null_right_sentence_dfa_nfa_set:
                            channel_look_ahead_set_mapping[sentence[flag]] |= nfa_state_number_look_ahead_mapping[nfa_state_number]
            for dfa_state, dfa_state_number in self._dfa_state_number_mapping.items():
                for nfa_state_number in dfa_state:
                    sentence, flag, _ = self._nfa_state_number_inverted_mapping[nfa_state_number]
                    flag_symbol: Optional[str] = sentence[flag] if flag < len(sentence) else None
                    if flag_symbol and flag > 0:
                        nfa_state_number_look_ahead_mapping: Dict[int, Set[str]] = dfa_state_nfa_state_look_ahead_mapping[self._dfa_move_table[dfa_state_number][flag_symbol]]
                        nfa_state_number_look_ahead_mapping[self._nfa_move_table[nfa_state_number][2]] |= dfa_state_nfa_state_look_ahead_mapping[dfa_state_number][nfa_state_number]
            current_channel_look_ahead_count: int = 0
            for _, dfa_state_data in dfa_state_channel_look_ahead_mapping.items():
                current_channel_look_ahead_count += sum([len(look_ahead_set) for _, look_ahead_set in dfa_state_data.items()])
            if current_channel_look_ahead_count > channel_look_ahead_count:
                channel_look_ahead_count: int = current_channel_look_ahead_count
                continue_loop: bool = True
                continue
            current_nfa_state_look_ahead_count: int = 0
            for _, dfa_state_data in dfa_state_nfa_state_look_ahead_mapping.items():
                current_nfa_state_look_ahead_count += sum([len(look_ahead_set) for _, look_ahead_set in dfa_state_data.items()])
            if current_nfa_state_look_ahead_count > nfa_state_look_ahead_count:
                nfa_state_look_ahead_count: int = current_nfa_state_look_ahead_count
                continue_loop: bool = True
                continue
        self._dfa_state_reduce_mapping: Dict[int, Dict[int, Set[str]]] = {}
        for dfa_state, dfa_state_number in self._dfa_state_number_mapping.items():
            dfa_state_reduce: Dict[int, Set[str]] = {}
            for nfa_state_number in dfa_state:
                sentence, flag, _ = self._nfa_state_number_inverted_mapping[nfa_state_number]
                if flag == len(sentence):
                    sentence_attribute: SentenceAttribute = self._sentence_attribute_mapping[sentence]
                    dfa_state_reduce[sentence_attribute.sentence_index] = dfa_state_nfa_state_look_ahead_mapping[dfa_state_number][nfa_state_number]
            self._dfa_state_reduce_mapping[dfa_state_number] = dfa_state_reduce
