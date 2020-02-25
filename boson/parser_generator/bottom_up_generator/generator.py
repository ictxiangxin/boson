from abc import abstractmethod
from boson.parser_generator import ParserGenerator
import boson.configure as configure


class BottomUpParserGenerator(ParserGenerator):
    def __init__(self, sentence_set: set):
        super().__init__(sentence_set)
        self._non_terminal_closure: dict = {}
        self._state_list: list = []
        self._state_move_table: dict = {}

    def __generate_non_terminal_closure(self, non_terminal: str) -> set:
        non_terminal_closure = set()
        visited_non_terminal_set = set()
        non_terminal_list = [non_terminal]
        while len(non_terminal_list) > 0:
            non_terminal = non_terminal_list.pop()
            visited_non_terminal_set.add(non_terminal)
            for sentence in self._sentence_set:
                if non_terminal == sentence[0]:
                    non_terminal_closure.add(sentence)
                    next_symbol = sentence[1]
                    if next_symbol in self._non_terminal_set and next_symbol not in visited_non_terminal_set:
                        non_terminal_list.append(next_symbol)
        return non_terminal_closure

    def state_list(self):
        return self._state_list

    def state_move_table(self):
        return self._state_move_table

    def initialize(self):
        super().initialize()
        self._non_terminal_closure = {}
        for non_terminal in self._non_terminal_set:
            self._non_terminal_closure[non_terminal] = self.__generate_non_terminal_closure(non_terminal)

    def generate_parser_dfa(self):
        self._state_list = [frozenset(self.initialize_start_state())]
        self._state_move_table = {}
        scan_index = 0
        while True:
            move_sentence_mapper = {}
            for flag_sentence in self._state_list[scan_index]:
                (sentence, _), flag = flag_sentence
                if flag < len(sentence):
                    move_symbol = sentence[flag]
                    move_sentence_mapper.setdefault(move_symbol, set())
                    move_sentence_mapper[move_symbol].add(flag_sentence)
            for move_symbol, flag_sentence_set in move_sentence_mapper.items():
                new_state = set()
                for (sentence, look_ahead), flag in flag_sentence_set:
                    flag += 1
                    new_state.add(((sentence, look_ahead), flag))
                    if flag < len(sentence):
                        if sentence[flag] in self._non_terminal_set:
                            closure_flag_sentence_set = set()
                            for temp_sentence in self._non_terminal_closure[sentence[flag]]:
                                temp_flag = 2 if temp_sentence[-1] == configure.boson_null_symbol else 1
                                temp_look_ahead = self.sentence_look_ahead_set(temp_sentence)
                                closure_flag_sentence_set.add(((temp_sentence, temp_look_ahead), temp_flag))
                            new_state |= closure_flag_sentence_set
                    new_state = self.state_post_processing(new_state)
                hashable_new_state = frozenset(new_state)
                self._state_move_table.setdefault(scan_index, {})
                if hashable_new_state in self._state_list:
                    old_index = self._state_list.index(hashable_new_state)
                    self._state_move_table[scan_index][move_symbol] = old_index
                else:
                    self._state_list.append(hashable_new_state)
                    self._state_move_table[scan_index][move_symbol] = len(self._state_list) - 1
            scan_index += 1
            if scan_index == len(self._state_list):
                break

    @abstractmethod
    def initialize_start_state(self):
        raise AttributeError('Bottom Up Grammar Parser must implement "initialize_start_state" Method.')

    @abstractmethod
    def sentence_look_ahead_set(self, sentence: tuple) -> (frozenset, None):
        raise AttributeError('Bottom Up Grammar Parser must implement "sentence_look_ahead_set" Method.')

    @abstractmethod
    def state_post_processing(self, state: set) -> set:
        raise AttributeError('Bottom Up Grammar Parser must implement "state_post_processing" Method.')
