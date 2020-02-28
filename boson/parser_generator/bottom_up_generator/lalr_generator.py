from boson.parser_generator.bottom_up_generator import BottomUpCanonicalParserGenerator
import boson.configure as configure


class LALRParserGenerator(BottomUpCanonicalParserGenerator):
    def __init__(self, sentence_set: set):
        super().__init__(sentence_set)

    def _non_terminal_look_ahead_set(self, sentence: tuple, flag: int, look_ahead_set: (set, frozenset)) -> (frozenset, None):
        first_set = self._sentence_first_set(sentence[flag + 1:])
        if configure.boson_null_symbol in first_set:
            first_set.remove(configure.boson_null_symbol)
            first_set |= look_ahead_set
        return frozenset(first_set)

    def _end_processing(self) -> None:
        normal_sentence_number_mapping = {}
        current_normal_sentence_number = 0
        dfa_state_core_number_mapping = {}
        current_dfa_state_core_number = 0
        dfa_state_core_mapping = {}
        self._dfa_state_reduce_mapping = {}
        for dfa_state, dfa_state_number in self._dfa_state_number_mapping.items():
            dfa_state_reduce = {}
            dfa_state_core = set()
            for nfa_state_number in dfa_state:
                sentence, flag, look_ahead_set = self._nfa_state_number_inverted_mapping[nfa_state_number]
                normal_sentence = (sentence, flag)
                if normal_sentence in normal_sentence_number_mapping:
                    normal_sentence_number = normal_sentence_number_mapping[normal_sentence]
                else:
                    normal_sentence_number = current_normal_sentence_number
                    normal_sentence_number_mapping[normal_sentence] = current_normal_sentence_number
                    current_normal_sentence_number += 1
                dfa_state_core.add(normal_sentence_number)
                if flag == len(sentence):
                    terminal_index = self._sentence_index_mapping[sentence]
                    dfa_state_reduce.setdefault(terminal_index, set())
                    dfa_state_reduce[terminal_index] |= look_ahead_set
            dfa_state_core = frozenset(dfa_state_core)
            if dfa_state_core in dfa_state_core_number_mapping:
                dfa_state_core_number = dfa_state_core_number_mapping[dfa_state_core]
            else:
                dfa_state_core_number = current_dfa_state_core_number
                dfa_state_core_number_mapping[dfa_state_core] = current_dfa_state_core_number
                current_dfa_state_core_number += 1
            dfa_state_core_mapping[dfa_state_number] = dfa_state_core_number
            if dfa_state_core_number in self._dfa_state_reduce_mapping:
                for sentence_index, look_ahead_set in self._dfa_state_reduce_mapping[dfa_state_core_number].items():
                    look_ahead_set |= dfa_state_reduce[sentence_index]
            else:
                self._dfa_state_reduce_mapping[dfa_state_core_number] = dfa_state_reduce
        new_dfa_move_table = {}
        for state_number, state_move_table in self._dfa_move_table.items():
            new_state_move_table = {}
            for symbol, next_state in state_move_table.items():
                new_state_move_table[symbol] = dfa_state_core_mapping[next_state]
            new_dfa_move_table[dfa_state_core_mapping[state_number]] = new_state_move_table
        self._dfa_move_table = new_dfa_move_table
