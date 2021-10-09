from typing import Dict

from boson.boson_script.sentence_attribute import SentenceAttribute
from boson.parser_generator.bottom_up_generator import BottomUpCanonicalParserGenerator


class SLRParserGenerator(BottomUpCanonicalParserGenerator):
    def __init__(self, sentence_set: set, sentence_attribute_mapping: Dict[tuple, SentenceAttribute]):
        super().__init__(sentence_set, sentence_attribute_mapping)

    def initialize(self) -> None:
        super().initialize()
        self._generate_non_terminal_follow_set()

    def _non_terminal_look_ahead_set(self, sentence: tuple, flag: int, look_ahead_set: (set, frozenset)) -> (frozenset, None):
        return None

    def _end_processing(self) -> None:
        self._dfa_state_reduce_mapping = {}
        for dfa_state, dfa_state_number in self._dfa_state_number_mapping.items():
            dfa_state_reduce = {}
            for nfa_state_number in dfa_state:
                sentence, flag, _ = self._nfa_state_number_inverted_mapping[nfa_state_number]
                if flag == len(sentence):
                    sentence_attribute = self._sentence_attribute_mapping[sentence]
                    dfa_state_reduce[sentence_attribute.sentence_index] = self._follow_set_mapping[sentence[0]]
            self._dfa_state_reduce_mapping[dfa_state_number] = dfa_state_reduce
