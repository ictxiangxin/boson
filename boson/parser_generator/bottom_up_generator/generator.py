from abc import abstractmethod
from boson.parser_generator import ParserGenerator
import boson.configure as configure


class BottomUpParserGenerator(ParserGenerator):
    def __init__(self, sentence_set: set):
        super().__init__(sentence_set)
        self._non_terminal_reduction_mapping: dict = {}
        self._nfa_state_number_inverted_mapping: dict = {}
        self._dfa_state_reduce_mapping: dict = {}
        self._dfa_state_number_mapping: dict = {}
        self._dfa_move_table: dict = {}

    def state_reduce_mapping(self):
        return self._dfa_state_reduce_mapping

    def dfa_move_table(self):
        return self._dfa_move_table

    def initialize(self):
        super().initialize()
        self._non_terminal_reduction_mapping = {}
        for sentence in self._sentence_list:
            self._non_terminal_reduction_mapping.setdefault(sentence[0], [])
            self._non_terminal_reduction_mapping[sentence[0]].append(sentence)

    def generate_parser_dfa(self):
        start_nfa_state = ((configure.boson_augmented_start,), 0, None)
        nfa_move_table = {}
        nfa_state_number_mapping = {start_nfa_state: 0}
        self._nfa_state_number_inverted_mapping = {0: start_nfa_state}
        nfa_state_number = 1
        non_terminal_nfa_state_number_set = {0}
        visited_non_terminal_set = set()
        nfa_state_stack = [start_nfa_state]
        while nfa_state_stack:
            state = nfa_state_stack.pop()
            sentence, flag, look_ahead = state
            if flag == 0:
                if sentence not in visited_non_terminal_set:
                    epsilon_move_set = set()
                    for reduction_sentence in self._non_terminal_reduction_mapping[sentence[0]]:
                        init_flag = 2 if reduction_sentence[-1] == configure.boson_null_symbol else 1
                        new_state = (reduction_sentence, init_flag, None)
                        nfa_state_number_mapping[new_state] = nfa_state_number
                        self._nfa_state_number_inverted_mapping[nfa_state_number] = new_state
                        nfa_state_stack.append(new_state)
                        epsilon_move_set.add(nfa_state_number)
                        nfa_state_number += 1
                    visited_non_terminal_set.add(sentence)
                    nfa_move_table[nfa_state_number_mapping[state]] = epsilon_move_set
            else:
                if flag < len(sentence):
                    symbol = sentence[flag]
                    new_state = (sentence, flag + 1, look_ahead)
                    nfa_state_number_mapping[new_state] = nfa_state_number
                    self._nfa_state_number_inverted_mapping[nfa_state_number] = new_state
                    nfa_state_stack.append(new_state)
                    move_state_number = nfa_state_number
                    nfa_state_number += 1
                    if symbol in self._non_terminal_set:
                        non_terminal_state = ((symbol,), 0, None)
                        if non_terminal_state in nfa_state_number_mapping:
                            non_terminal_nfa_state_number = nfa_state_number_mapping[non_terminal_state]
                        else:
                            nfa_state_number_mapping[non_terminal_state] = nfa_state_number
                            self._nfa_state_number_inverted_mapping[nfa_state_number] = non_terminal_state
                            nfa_state_stack.append(non_terminal_state)
                            non_terminal_nfa_state_number = nfa_state_number
                            non_terminal_nfa_state_number_set.add(non_terminal_nfa_state_number)
                            nfa_state_number += 1
                    else:
                        non_terminal_nfa_state_number = None
                    nfa_move_table[nfa_state_number_mapping[state]] = (non_terminal_nfa_state_number, symbol, move_state_number)
        state_epsilon_closure_mapping = {}
        for state, state_move_table in nfa_move_table.items():
            if isinstance(state_move_table, set):
                state_epsilon_closure_mapping[state] = set(state_move_table)
            else:
                if state_move_table[0] is not None:
                    state_epsilon_closure_mapping[state] = {state_move_table[0]}
        available_state_set = set(state_epsilon_closure_mapping)
        variable_state_set = set(state_epsilon_closure_mapping)
        continue_loop = True
        while continue_loop:
            continue_loop = False
            for state, epsilon_closure in state_epsilon_closure_mapping.items():
                if state in variable_state_set:
                    update_state_set = available_state_set & epsilon_closure
                    if update_state_set:
                        old_closure_size = len(epsilon_closure)
                        update_closure = set(epsilon_closure)
                        for update_state in update_state_set:
                            update_closure |= state_epsilon_closure_mapping[update_state]
                        if old_closure_size < len(update_closure):
                            state_epsilon_closure_mapping[state] = update_closure
                            continue_loop = True
                    else:
                        variable_state_set.remove(state)
        dfa_state_number = 0
        dfa_start_state = frozenset(state_epsilon_closure_mapping[0] | {0})
        dfa_state_wait_list = [dfa_start_state]
        self._dfa_state_number_mapping = {dfa_start_state: dfa_state_number}
        self._dfa_move_table = {}
        while dfa_state_wait_list:
            dfa_state = dfa_state_wait_list.pop()
            dfa_from_state_number = self._dfa_state_number_mapping[dfa_state]
            move_closure_mapping = {}
            for nfa_state_number in dfa_state:
                if nfa_state_number in nfa_move_table:
                    state_move_table = nfa_move_table[nfa_state_number]
                    if isinstance(state_move_table, tuple):
                        move_closure_mapping.setdefault(state_move_table[1], set())
                        move_closure_mapping[state_move_table[1]].add(state_move_table[2])
            for symbol, move_closure in move_closure_mapping.items():
                move_closure_epsilon_closure = set()
                for nfa_state_number in move_closure:
                    move_closure_epsilon_closure |= state_epsilon_closure_mapping.get(nfa_state_number, set())
                new_dfa_state = frozenset(move_closure | move_closure_epsilon_closure)
                if new_dfa_state in self._dfa_state_number_mapping:
                    dfa_to_state_number = self._dfa_state_number_mapping[new_dfa_state]
                else:
                    dfa_to_state_number = dfa_state_number
                    self._dfa_state_number_mapping[new_dfa_state] = dfa_state_number
                    dfa_state_number += 1
                    dfa_state_wait_list.append(new_dfa_state)
                self._dfa_move_table.setdefault(dfa_from_state_number, {})
                self._dfa_move_table[dfa_from_state_number][symbol] = dfa_to_state_number
        self.end_processing()

    @abstractmethod
    def initialize_start_state(self):
        raise AttributeError('Bottom Up Grammar Parser must implement "initialize_start_state" Method.')

    @abstractmethod
    def sentence_look_ahead_set(self, sentence: tuple) -> (frozenset, None):
        raise AttributeError('Bottom Up Grammar Parser must implement "sentence_look_ahead_set" Method.')

    @abstractmethod
    def state_pre_processing(self, state: frozenset) -> frozenset:
        raise AttributeError('Bottom Up Grammar Parser must implement "state_pre_processing" Method.')

    @abstractmethod
    def state_post_processing(self, state: set) -> set:
        raise AttributeError('Bottom Up Grammar Parser must implement "state_post_processing" Method.')

    @abstractmethod
    def end_processing(self) -> None:
        raise AttributeError('Bottom Up Grammar Parser must implement "end_processing" Method.')
