from typing import Dict

import boson.configure as configure
from boson.boson_script.sentence_attribute import SentenceAttribute
from boson.parser_generator.bottom_up_generator import BottomUpCanonicalParserGenerator


class LRParserGenerator(BottomUpCanonicalParserGenerator):
    def __init__(self, sentence_set: set, sentence_attribute_mapping: Dict[tuple, SentenceAttribute]):
        super().__init__(sentence_set, sentence_attribute_mapping)

    def _non_terminal_look_ahead_set(self, sentence: tuple, flag: int, look_ahead_set: (set, frozenset)) -> (frozenset, None):
        first_set = self._sentence_first_set(sentence[flag + 1:])
        if configure.boson_null_symbol in first_set:
            first_set.remove(configure.boson_null_symbol)
            first_set |= look_ahead_set
        return frozenset(first_set)

    def _end_processing(self) -> None:
        self._dfa_state_reduce_mapping = {}
        for dfa_state, dfa_state_number in self._dfa_state_number_mapping.items():
            dfa_state_reduce = {}
            for nfa_state_number in dfa_state:
                sentence, flag, look_ahead_set = self._nfa_state_number_inverted_mapping[nfa_state_number]
                if flag == len(sentence):
                    sentence_attribute = self._sentence_attribute_mapping[sentence]
                    dfa_state_reduce.setdefault(sentence_attribute.sentence_index, set())
                    dfa_state_reduce[sentence_attribute.sentence_index] |= look_ahead_set
            self._dfa_state_reduce_mapping[dfa_state_number] = dfa_state_reduce
