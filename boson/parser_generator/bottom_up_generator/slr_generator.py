from boson.parser_generator.bottom_up_generator import BottomUpCanonicalParserGenerator


class SLRParserGenerator(BottomUpCanonicalParserGenerator):
    def __init__(self, sentence_set: set):
        super().__init__(sentence_set)

    def initialize(self):
        super().initialize()
        self._generate_non_terminal_follow_set()

    def _non_terminal_look_ahead_set(self, sentence: tuple, flag: int, look_ahead_set: (set, frozenset)) -> (frozenset, None):
        return None

    def _end_processing(self) -> None:
        self._dfa_state_reduce_mapping = {}
        for dfa_state, dfa_state_number in self._dfa_state_number_mapping.items():
            dfa_state_reduce = []
            for nfa_state_number in dfa_state:
                sentence, flag, _ = self._nfa_state_number_inverted_mapping[nfa_state_number]
                if flag == len(sentence):
                    dfa_state_reduce.append((self._sentence_index_mapping[sentence], self._follow_set_mapping[sentence[0]]))
            self._dfa_state_reduce_mapping[dfa_state_number] = dfa_state_reduce
