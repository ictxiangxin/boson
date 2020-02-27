from abc import abstractmethod
from boson.parser_generator.bottom_up_generator import BottomUpParserGenerator
import boson.configure as configure


class BottomUpCanonicalParserGenerator(BottomUpParserGenerator):
    def __init__(self, sentence_set: set):
        super().__init__(sentence_set)
        self._action_table: list = []
        self._sparse_action_table: dict = {}
        self._goto_table: list = []
        self._sparse_goto_table: dict = {}
        self._conflict_list: list = []

    def action_table(self):
        return self._action_table

    def sparse_action_table(self):
        return self._sparse_action_table

    def goto_table(self):
        return self._goto_table

    def sparse_goto_table(self):
        return self._sparse_goto_table

    def conflict_list(self):
        return self._conflict_list

    def initialize(self):
        super().initialize()
        self._generate_non_terminal_first_set()

    def generate_parse_table(self):
        conflict_resolver_enable = configure.boson_option['conflict_resolver'] == 'yes'
        self._action_table = [[configure.boson_table_sign_error] * (len(self._terminal_index_mapping) + 1) for _ in range(len(self._dfa_state_number_mapping))]
        self._goto_table = [[configure.boson_invalid_goto] * len(self._non_terminal_index_mapping) for _ in range(len(self._dfa_state_number_mapping))]
        self._conflict_list = []
        for state_number, state_move_table in self._dfa_move_table.items():
            for symbol, next_state in state_move_table.items():
                if symbol in self._terminal_index_mapping:
                    self._action_table[state_number][self._terminal_index_mapping[symbol]] = '{}{}'.format(configure.boson_table_sign_shift, next_state)
                else:
                    self._goto_table[state_number][self._non_terminal_index_mapping[symbol]] = next_state
        for state_number, reduce_sentence_list in self._dfa_state_reduce_mapping.items():
            for reduce_number, terminal_set in reduce_sentence_list:
                for terminal in terminal_set:
                    terminal_index = self._terminal_index_mapping[terminal]
                    if self._action_table[state_number][terminal_index] != configure.boson_table_sign_error:
                        old_action = self._action_table[state_number][terminal_index]
                        old_sign = old_action[0]
                        if old_sign in {configure.boson_table_sign_reduce, configure.boson_table_sign_accept}:
                            if conflict_resolver_enable:
                                old_reduce_number = int(old_action[1:])
                                old_shorter = len(self._sentence_list[old_reduce_number]) < len(self._sentence_list[reduce_number])
                                longer = configure.boson_option['reduce_reduce_conflict_resolver'] == 'long'
                                if not (old_shorter ^ longer):
                                    self._action_table[state_number][terminal_index] = '{}{}'.format(configure.boson_table_sign_reduce, reduce_number)
                            else:
                                self._conflict_list.append((state_number, configure.boson_conflict_reduce_reduce, terminal))
                        elif old_sign == configure.boson_table_sign_shift:
                            if conflict_resolver_enable:
                                if configure.boson_option['shift_reduce_conflict_resolver'] == 'reduce':
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

    def parse_table_sparsification(self):
        self._sparse_action_table = {}
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
    def initialize_start_state(self):
        raise AttributeError('Bottom Up Canonical Grammar Parser must implement "initialize_start_state" Method.')

    @abstractmethod
    def sentence_look_ahead_set(self, sentence: tuple) -> (frozenset, None):
        raise AttributeError('Bottom Up Canonical Grammar Parser must implement "sentence_look_ahead_set" Method.')

    @abstractmethod
    def state_post_processing(self, state: set) -> set:
        raise AttributeError('Bottom Up Canonical Grammar Parser must implement "state_post_processing" Method.')

    @abstractmethod
    def end_processing(self) -> None:
        raise AttributeError('Bottom Up Canonical Grammar Parser must implement "end_processing" Method.')
