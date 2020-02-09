import boson.bs_configure as configure


class DFA:
    def __init__(self):
        self.__move_table: dict = {}
        self.__start_state: int = configure.boson_lexicon_default_state
        self.__end_state_set: set = set()
        self.__state_set: set = set()

    def set_start_state(self, state: int):
        self.__start_state = state

    def add_end_state(self, state: int):
        self.__end_state_set.add(state)

    def add_move(self, from_state: int, character: (str, bool), to_state: int):
        self.__state_set.add(from_state)
        self.__state_set.add(to_state)
        self.__move_table.setdefault(from_state, {})
        self.__move_table[from_state][character] = to_state

    def move(self, state: int, character: (str, bool)) -> int:
        return self.__move_table.get(state, {}).get(character, None)

    def alphabet(self) -> set:
        alphabet = set()
        for _, move_table in self.__move_table.items():
            alphabet |= set(move_table)
        return alphabet - {configure.boson_lexicon_epsilon_transition}

    def minimize(self):
        alphabet = self.alphabet()
        group_number = 0
        state_group_number = {}
        state_group_wait_list = [set(self.__state_set - self.__end_state_set), set(self.__end_state_set)]
        for state_group in state_group_wait_list:
            for state in state_group:
                state_group_number[state] = group_number
            group_number += 1
        while len(state_group_wait_list) > 0:
            state_group = state_group_wait_list.pop()
            if len(state_group) > 1:
                merge = True
                for character in alphabet:
                    split_group = {}
                    for state in state_group:
                        move_state = self.move(state, character)
                        move_group_number = state_group_number.get(move_state, -1)
                        split_group.setdefault(move_group_number, set())
                        split_group[move_group_number].add(state)
                    if len(split_group) > 1:
                        for _, group in split_group.items():
                            for state in group:
                                state_group_number[state] = group_number
                            group_number += 1
                            state_group_wait_list.append(group)
                        merge = False
                        break
                if merge:
                    base_state = state_group.pop()
                    base_state_move_table = self.__move_table.get(base_state, {})
                    if self.__start_state in state_group:
                        self.__start_state = base_state
                    if len(self.__end_state_set & state_group) > 0:
                        self.__end_state_set -= state_group
                        self.__end_state_set.add(base_state)
                    for remove_state in state_group:
                        base_state_move_table.update(self.__move_table.get(remove_state, {}))
                        del self.__move_table[remove_state]
                    self.__move_table[base_state] = base_state_move_table
                    for from_state, move_table in self.__move_table.items():
                        for character, to_state in move_table.items():
                            if to_state in state_group:
                                move_table[character] = base_state
                        self.__move_table[from_state] = move_table


class NFA:
    def __init__(self):
        self.__move_table: dict = {}
        self.__start_state: int = configure.boson_lexicon_default_start_state
        self.__end_state_set: set = set()
        self.__state_set: set = set()

    def set_start_state(self, state: int):
        self.__start_state = state

    def add_end_state(self, state: int):
        self.__end_state_set.add(state)

    def add_move(self, from_state: int, character: (str, bool), to_state: int):
        self.__state_set.add(from_state)
        self.__state_set.add(to_state)
        self.__move_table.setdefault(from_state, {})
        self.__move_table[from_state].setdefault(character, set())
        self.__move_table[from_state][character].add(to_state)

    def state_set(self):
        return self.__state_set

    def start_state(self):
        return self.__start_state

    def end_state_set(self):
        return self.__end_state_set

    def move_table(self):
        return self.__move_table

    def alphabet(self) -> set:
        alphabet = set()
        for _, move_table in self.move_table().items():
            alphabet |= set(move_table)
        return alphabet - {configure.boson_lexicon_epsilon_transition}

    def epsilon_closure(self, state: (set, frozenset, int)) -> set:
        if isinstance(state, int):
            wait_set = {state}
        else:
            wait_set = set(state)
        closure = set()
        while len(wait_set) > 0:
            check_state = wait_set.pop()
            closure.add(check_state)
            wait_set |= self.move_table().get(check_state, {}).get(configure.boson_lexicon_epsilon_transition, set()) - closure
        return closure

    def move_closure(self, state_set: (set, frozenset), character: (str, bool)) -> set:
        closure = set()
        for state in state_set:
            closure |= self.move_table().get(state, {}).get(character, set())
        return closure

    def transform_to_dfa(self) -> DFA:
        dfa_state_set = set()
        dfa_state_wait_list = []
        dfa_state_map = {}
        dfa_state_number = configure.boson_lexicon_default_state
        dfa_entity = DFA()
        alphabet = self.alphabet()
        dfa_start = frozenset(self.epsilon_closure(self.start_state()))
        dfa_state_set.add(dfa_start)
        dfa_state_map[dfa_start] = dfa_state_number
        dfa_entity.set_start_state(dfa_state_number)
        dfa_state_number += 1
        dfa_state_wait_list.append(dfa_start)
        while len(dfa_state_wait_list) > 0:
            dfa_state = dfa_state_wait_list.pop()
            for character in alphabet:
                new_dfa_state = frozenset(self.epsilon_closure(self.move_closure(dfa_state, character)))
                if len(new_dfa_state) == 0:
                    continue
                if new_dfa_state not in dfa_state_set:
                    dfa_state_set.add(new_dfa_state)
                    dfa_state_map[new_dfa_state] = dfa_state_number
                    dfa_state_number += 1
                    dfa_state_wait_list.append(new_dfa_state)
                from_state = dfa_state_map[dfa_state]
                to_state = dfa_state_map[new_dfa_state]
                dfa_entity.add_move(from_state, character, to_state)
                if len(self.end_state_set() & new_dfa_state) > 0:
                    dfa_entity.add_end_state(to_state)
        return dfa_entity

    def next_state(self):
        return max(self.state_set()) + 1 if len(self.state_set()) > 0 else configure.boson_lexicon_default_state

    def update(self, input_nfa_list: list) -> tuple:
        start_state_mapping = {}
        end_state_mapping = {}
        global_state_number = self.next_state()
        for index, input_nfa in enumerate(input_nfa_list):
            nfa_move_table = input_nfa.move_table()
            temp_state_mapping = {}
            for from_state, move_table in nfa_move_table.items():
                is_start_state = True if from_state == input_nfa.start_state() else False
                if from_state in temp_state_mapping:
                    from_state = temp_state_mapping[from_state]
                else:
                    temp_state_mapping[from_state] = global_state_number
                    from_state = global_state_number
                    global_state_number += 1
                if is_start_state:
                    start_state_mapping[index] = from_state
                for character, to_state_set in move_table.items():
                    for to_state in to_state_set:
                        is_end_state = True if to_state in input_nfa.end_state_set() else False
                        if to_state in temp_state_mapping:
                            to_state = temp_state_mapping[to_state]
                        else:
                            temp_state_mapping[to_state] = global_state_number
                            to_state = global_state_number
                            global_state_number += 1
                        if is_end_state:
                            end_state_mapping.setdefault(index, set())
                            end_state_mapping[index].add(to_state)
                        self.add_move(from_state, character, to_state)
        return start_state_mapping, end_state_mapping

    def create_nfa_character(self, character: (str, bool)):
        self.add_move(configure.boson_lexicon_default_start_state, character, configure.boson_lexicon_default_end_state)
        self.set_start_state(configure.boson_lexicon_default_start_state)
        self.add_end_state(configure.boson_lexicon_default_end_state)

    def create_nfa_link(self, input_nfa_list: list):
        start_state_mapping, end_state_mapping = self.update(input_nfa_list)
        for index in range(len(input_nfa_list)):
            if index == 0:
                self.set_start_state(start_state_mapping[index])
            if index == len(input_nfa_list) - 1:
                for state in end_state_mapping[index]:
                    self.add_end_state(state)
            if index > 0:
                start_state = start_state_mapping[index]
                for previous_end_state in end_state_mapping[index - 1]:
                    self.add_move(previous_end_state, configure.boson_lexicon_epsilon_transition, start_state)

    def create_nfa_or(self, input_nfa_list: list):
        start_state_mapping, end_state_mapping = self.update(input_nfa_list)
        start_state = self.next_state()
        self.set_start_state(start_state)
        for state in [state for _, state in start_state_mapping.items()]:
            self.add_move(start_state, configure.boson_lexicon_epsilon_transition, state)
        end_state = self.next_state()
        self.add_end_state(end_state)
        for state_set in [state_set for _, state_set in end_state_mapping.items()]:
            for state in state_set:
                self.add_move(state, configure.boson_lexicon_epsilon_transition, end_state)

    def create_nfa_kleene_closure(self, input_nfa):
        start_state_mapping, end_state_mapping = self.update([input_nfa])
        end_state = self.next_state()
        self.add_end_state(end_state)
        for state in end_state_mapping[0]:
            self.add_move(state, configure.boson_lexicon_epsilon_transition, start_state_mapping[0])
            self.add_move(state, configure.boson_lexicon_epsilon_transition, end_state)
        start_state = self.next_state()
        self.set_start_state(start_state)
        self.add_move(start_state, configure.boson_lexicon_epsilon_transition, start_state_mapping[0])
        self.add_move(start_state, configure.boson_lexicon_epsilon_transition, end_state)

    def create_nfa_plus_closure(self, input_nfa):
        start_state_mapping, end_state_mapping = self.update([input_nfa])
        end_state = self.next_state()
        self.add_end_state(end_state)
        for state in end_state_mapping[0]:
            self.add_move(state, configure.boson_lexicon_epsilon_transition, start_state_mapping[0])
            self.add_move(state, configure.boson_lexicon_epsilon_transition, end_state)
        start_state = self.next_state()
        self.set_start_state(start_state)
        self.add_move(start_state, configure.boson_lexicon_epsilon_transition, start_state_mapping[0])

    def create_nfa_repeat(self, input_nfa, count: int):
        self.create_nfa_link([input_nfa] * count)


def bs_create_nfa_character(character: (str, bool)) -> NFA:
    nfa = NFA()
    nfa.create_nfa_character(character)
    return nfa


def bs_create_nfa_or(input_list: list):
    nfa = NFA()
    nfa.create_nfa_or(input_list)
    return nfa


def bs_create_nfa_link(input_list: list):
    nfa = NFA()
    nfa.create_nfa_link(input_list)
    return nfa


def bs_create_nfa_kleene_closure(input_nfa: NFA):
    nfa = NFA()
    nfa.create_nfa_kleene_closure(input_nfa)
    return nfa


def bs_create_nfa_plus_closure(input_nfa: NFA):
    nfa = NFA()
    nfa.create_nfa_plus_closure(input_nfa)
    return nfa


def bs_create_nfa_repeat(input_nfa: NFA, count: int):
    nfa = NFA()
    nfa.create_nfa_repeat(input_nfa, count)
    return nfa
