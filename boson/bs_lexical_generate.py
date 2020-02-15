import boson.bs_configure as configure


class LexicalDFA:
    def __init__(self):
        self.__move_table: dict = {}
        self.__start_state: int = configure.boson_lexical_default_state
        self.__end_state_set: set = set()
        self.__state_set: set = set()
        self.__lexical_symbol_mapping: dict = {}
        self.__character_set: set = set()
        self.__compact_move_table: dict = {}

    def __alphabet(self, state_group: set) -> set:
        alphabet = set()
        for state in state_group:
            if state in self.__move_table:
                alphabet |= set(self.__move_table[state])
        return alphabet - {configure.boson_lexical_epsilon_transition}

    def __move(self, state: int, character: str) -> int:
        return self.__move_table.get(state, {}).get(character, None)

    def set_start_state(self, state: int) -> None:
        self.__start_state = state

    def add_end_state(self, state: int) -> None:
        self.__end_state_set.add(state)

    def add_move(self, from_state: int, character: str, to_state: int) -> None:
        self.__state_set.add(from_state)
        self.__state_set.add(to_state)
        self.__move_table.setdefault(from_state, {})
        self.__move_table[from_state][character] = to_state

    def add_lexical_symbol(self, state: int, lexical_symbol: str) -> None:
        self.__lexical_symbol_mapping[state] = lexical_symbol

    def set_character_set(self, character_set: set) -> None:
        self.__character_set = set(character_set)

    def move_table(self) -> dict:
        return self.__move_table

    def compact_move_table(self) -> dict:
        return self.__compact_move_table

    def character_set(self) -> set:
        return self.__character_set

    def start_state(self) -> int:
        return self.__start_state

    def end_state_set(self) -> set:
        return self.__end_state_set

    def lexical_symbol_mapping(self) -> dict:
        return self.__lexical_symbol_mapping

    def simplify(self) -> None:
        self.__compact_move_table = {}
        for from_state, move_table in self.__move_table.items():
            reverse_mapping = {}
            for character, to_state in move_table.items():
                reverse_mapping.setdefault(to_state, set())
                reverse_mapping[to_state].add(character)
            self.__compact_move_table.setdefault(from_state, [])
            for to_state, character_set in reverse_mapping.items():
                range_list = []
                scattered_character_set = set()
                scan_head = None
                scan = None
                reverse = False
                if configure.boson_lexical_wildcard in character_set:
                    if len(self.__character_set) < 1.5 * len(character_set):
                        reverse = True
                        character_set = self.__character_set - character_set
                for character in sorted(character_set - {configure.boson_lexical_wildcard}) + [chr(0xffff)]:
                    if scan_head is None:
                        scan_head = character
                        scan = character
                    else:
                        if ord(character) - ord(scan) != 1:
                            if ord(scan) - ord(scan_head) > 1:
                                range_list.append((scan_head, scan))
                            else:
                                scattered_character_set.add(scan_head)
                                scattered_character_set.add(scan)
                            scan_head = character
                            scan = character
                        else:
                            scan = character
                has_wildcard = configure.boson_lexical_wildcard in character_set
                attribute = 0b00
                if reverse and not has_wildcard:
                    attribute = 0b10
                elif not reverse and has_wildcard:
                    attribute = 0b01
                self.__compact_move_table[from_state].append([attribute, scattered_character_set, range_list, to_state])

    def minimize(self) -> None:
        group_number = 0
        state_group_number = {}
        state_group_wait_list = [set(self.__state_set - self.__end_state_set), set(self.__end_state_set)]
        state_group_checked_list = []
        for state_group in state_group_wait_list:
            for state in state_group:
                state_group_number[state] = group_number
            group_number += 1
        group_changed = True
        while group_changed:
            group_changed = False
            while len(state_group_wait_list) > 0:
                state_group = state_group_wait_list.pop()
                if len(state_group) > 1:
                    check_pass = True
                    group_changed = False
                    for character in self.__alphabet(state_group) | {None}:
                        split_group = {}
                        for state in state_group:
                            move_state = self.__move(state, character)
                            move_group_number = state_group_number.get(move_state, -1)
                            if state in self.__lexical_symbol_mapping:
                                move_group_number = (move_group_number, self.__lexical_symbol_mapping[state])
                            split_group.setdefault(move_group_number, set())
                            split_group[move_group_number].add(state)
                        if len(split_group) > 1:
                            for _, group in split_group.items():
                                for state in group:
                                    state_group_number[state] = group_number
                                group_number += 1
                                state_group_wait_list.append(group)
                            group_changed = True
                            check_pass = False
                            break
                    if check_pass:
                        state_group_checked_list.append(state_group)
            if group_changed:
                state_group_wait_list = state_group_checked_list
                state_group_checked_list = []
        for merge_group in state_group_checked_list:
            base_state = merge_group.pop()
            base_state_move_table = self.__move_table.get(base_state, {})
            if self.__start_state in merge_group:
                self.__start_state = base_state
            if len(self.__end_state_set & merge_group) > 0:
                self.__end_state_set -= merge_group
                self.__end_state_set.add(base_state)
            for remove_state in merge_group:
                self.__state_set.remove(remove_state)
                if remove_state in self.__lexical_symbol_mapping:
                    del self.__lexical_symbol_mapping[remove_state]
                base_state_move_table.update(self.__move_table.get(remove_state, {}))
                if remove_state in self.__move_table:
                    del self.__move_table[remove_state]
            if len(base_state_move_table) > 0:
                self.__move_table[base_state] = base_state_move_table
            for from_state, move_table in self.__move_table.items():
                for character, to_state in move_table.items():
                    if to_state in merge_group:
                        move_table[character] = base_state
                self.__move_table[from_state] = move_table
        new_state_number_mapping = {}
        new_number = 0
        for state in self.__state_set:
            new_state_number_mapping[state] = new_number
            new_number += 1
        new_move_table = {}
        for from_state, move_table in self.__move_table.items():
            state_move_table = {}
            for symbol, to_state in move_table.items():
                state_move_table[symbol] = new_state_number_mapping[to_state]
            new_move_table[new_state_number_mapping[from_state]] = state_move_table
        new_end_state_set = set()
        for state in self.__end_state_set:
            new_end_state_set.add(new_state_number_mapping[state])
        new_lexical_symbol_mapping = {}
        for state, lexical_symbol in self.__lexical_symbol_mapping.items():
            new_lexical_symbol_mapping[new_state_number_mapping[state]] = lexical_symbol
        self.__move_table = new_move_table
        self.__state_set = set(range(new_number))
        self.__start_state = new_state_number_mapping[self.__start_state]
        self.__end_state_set = new_end_state_set
        self.__lexical_symbol_mapping = new_lexical_symbol_mapping


class LexicalNFA:
    def __init__(self):
        self.__move_table: dict = {}
        self.__start_state: int = configure.boson_lexical_default_start_state
        self.__end_state_set: set = set()
        self.__state_set: set = set()
        self.__character_set: set = set()
        self.__lexical_symbol_mapping: dict = {}
        self.__reverse_delay_construct: bool = False
        self.__reverse_character_set: set = set()
        self.__delay_construct_reverse_set_list: list = []
        self.__delay_construct_base_state_list: list = []

    def __alphabet(self, dfa_state: frozenset) -> set:
        alphabet = set()
        for state in dfa_state:
            if state in self.__move_table:
                alphabet |= set(self.__move_table[state])
        return alphabet - {configure.boson_lexical_epsilon_transition}

    def set_start_state(self, state: int) -> None:
        self.__start_state = state

    def add_end_state(self, state: int) -> None:
        self.__end_state_set.add(state)

    def add_move(self, from_state: int, character: str, to_state: int) -> None:
        self.__state_set.add(from_state)
        self.__state_set.add(to_state)
        self.__character_set.add(character)
        self.__move_table.setdefault(from_state, {})
        self.__move_table[from_state].setdefault(character, set())
        self.__move_table[from_state][character].add(to_state)

    def construct(self, full_character_set: set = None) -> None:
        if full_character_set is None:
            full_character_set = self.character_set()
        if self.__reverse_delay_construct:
            for pass_character in full_character_set - self.reverse_character_set():
                self.add_move(configure.boson_lexical_default_start_state, pass_character, configure.boson_lexical_default_end_state)
            self.__reverse_delay_construct = False
        for reverse_character_set, delay_base_state in self.delay_construct_list():
            for pass_character in full_character_set - reverse_character_set:
                self.add_move(delay_base_state[0], pass_character, delay_base_state[1])

    def reverse_delay_construct(self) -> bool:
        return self.__reverse_delay_construct

    def reverse_character_set(self) -> set:
        return self.__reverse_character_set

    def delay_construct_list(self) -> zip:
        return zip(self.__delay_construct_reverse_set_list, self.__delay_construct_base_state_list)

    def character_set(self) -> set:
        return self.__character_set - {configure.boson_lexical_epsilon_transition, configure.boson_lexical_wildcard}

    def state_set(self) -> set:
        return self.__state_set

    def start_state(self) -> int:
        return self.__start_state

    def end_state_set(self) -> set:
        return self.__end_state_set

    def move_table(self) -> dict:
        return self.__move_table

    def epsilon_closure(self, state: (set, frozenset, int)) -> set:
        if isinstance(state, int):
            wait_set = {state}
        else:
            wait_set = set(state)
        closure = set()
        while len(wait_set) > 0:
            check_state = wait_set.pop()
            closure.add(check_state)
            wait_set |= self.move_table().get(check_state, {}).get(configure.boson_lexical_epsilon_transition, set()) - closure
        return closure

    def move_closure(self, state_set: (set, frozenset), character: str) -> set:
        closure = set()
        for state in state_set:
            closure |= self.move_table().get(state, {}).get(character, set())
        return closure

    def transform_to_dfa(self) -> LexicalDFA:
        dfa_state_set = set()
        dfa_state_wait_list = []
        dfa_state_map = {}
        dfa_state_number = configure.boson_lexical_default_state
        dfa_entity = LexicalDFA()
        dfa_start = frozenset(self.epsilon_closure(self.start_state()))
        dfa_state_set.add(dfa_start)
        dfa_state_map[dfa_start] = dfa_state_number
        dfa_entity.set_start_state(dfa_state_number)
        if len(self.end_state_set() & dfa_start) > 0:
            dfa_entity.add_end_state(dfa_state_number)
        dfa_state_number += 1
        dfa_state_wait_list.append(dfa_start)
        lexical_end_state_set = set(self.__lexical_symbol_mapping)
        while len(dfa_state_wait_list) > 0:
            dfa_state = dfa_state_wait_list.pop()
            for character in self.__alphabet(dfa_state):
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
                for lexical_state in lexical_end_state_set & new_dfa_state:
                    dfa_entity.add_lexical_symbol(to_state, self.__lexical_symbol_mapping[lexical_state])
        dfa_entity.set_character_set(self.character_set())
        return dfa_entity

    def next_state(self) -> int:
        return max(self.state_set()) + 1 if len(self.state_set()) > 0 else configure.boson_lexical_default_state

    def update(self, input_nfa_list: list) -> tuple:
        start_state_mapping = {}
        end_state_mapping = {}
        global_state_number = self.next_state()
        for index, input_nfa in enumerate(input_nfa_list):
            if input_nfa.reverse_delay_construct():
                self.__delay_construct_reverse_set_list.append(input_nfa.reverse_character_set())
            temp_state_mapping = {}
            end_state_mapping.setdefault(index, set())
            for from_state, move_table in input_nfa.move_table().items():
                is_start_state = True if from_state == input_nfa.start_state() else False
                is_end_state = True if from_state in input_nfa.end_state_set() else False
                if from_state in temp_state_mapping:
                    from_state = temp_state_mapping[from_state]
                else:
                    temp_state_mapping[from_state] = global_state_number
                    from_state = global_state_number
                    global_state_number += 1
                if is_start_state:
                    start_state_mapping[index] = from_state
                if is_end_state:
                    end_state_mapping[index].add(from_state)
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
                            end_state_mapping[index].add(to_state)
                        self.add_move(from_state, character, to_state)
            if input_nfa.reverse_delay_construct():
                self.__delay_construct_base_state_list.append((start_state_mapping[index], set(end_state_mapping[index]).pop()))
            for reverse_character_set, delay_base_state in input_nfa.delay_construct_list():
                self.__delay_construct_reverse_set_list.append(reverse_character_set)
                self.__delay_construct_base_state_list.append((temp_state_mapping[delay_base_state[0]], temp_state_mapping[delay_base_state[1]]))
            self.__character_set |= input_nfa.character_set()
        return start_state_mapping, end_state_mapping

    def add_lexical_symbol(self, lexical_nfa, lexical_symbol: str) -> None:
        default_start_state = configure.boson_lexical_default_start_state
        if len(self.__state_set) == 0:
            self.__state_set.add(default_start_state)
        start_state_mapping, end_state_mapping = self.update([lexical_nfa])
        self.add_move(default_start_state, configure.boson_lexical_epsilon_transition, start_state_mapping[0])
        for state in end_state_mapping[0]:
            self.__lexical_symbol_mapping[state] = lexical_symbol
            self.add_end_state(state)

    def create_nfa_reverse_delay_construct(self, reverse_character_set: set) -> None:
        self.__reverse_delay_construct = True
        self.__reverse_character_set = set(reverse_character_set)
        self.__character_set |= reverse_character_set
        self.add_move(configure.boson_lexical_default_start_state, configure.boson_lexical_wildcard, configure.boson_lexical_default_end_state)
        self.set_start_state(configure.boson_lexical_default_start_state)
        self.add_end_state(configure.boson_lexical_default_end_state)

    def create_nfa_character(self, character: str) -> None:
        self.add_move(configure.boson_lexical_default_start_state, character, configure.boson_lexical_default_end_state)
        self.set_start_state(configure.boson_lexical_default_start_state)
        self.add_end_state(configure.boson_lexical_default_end_state)

    def create_nfa_link(self, input_nfa_list: list) -> None:
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
                    self.add_move(previous_end_state, configure.boson_lexical_epsilon_transition, start_state)

    def create_nfa_or(self, input_nfa_list: list) -> None:
        start_state_mapping, end_state_mapping = self.update(input_nfa_list)
        start_state = self.next_state()
        self.set_start_state(start_state)
        for _, state in start_state_mapping.items():
            self.add_move(start_state, configure.boson_lexical_epsilon_transition, state)
        end_state = self.next_state()
        self.add_end_state(end_state)
        for _, end_state_set in end_state_mapping.items():
            for state in end_state_set:
                self.add_move(state, configure.boson_lexical_epsilon_transition, end_state)

    def create_nfa_kleene_closure(self, input_nfa) -> None:
        start_state_mapping, end_state_mapping = self.update([input_nfa])
        end_state = self.next_state()
        self.add_end_state(end_state)
        for state in end_state_mapping[0]:
            self.add_move(state, configure.boson_lexical_epsilon_transition, start_state_mapping[0])
            self.add_move(state, configure.boson_lexical_epsilon_transition, end_state)
        start_state = self.next_state()
        self.set_start_state(start_state)
        self.add_move(start_state, configure.boson_lexical_epsilon_transition, start_state_mapping[0])
        self.add_move(start_state, configure.boson_lexical_epsilon_transition, end_state)

    def create_nfa_plus_closure(self, input_nfa) -> None:
        start_state_mapping, end_state_mapping = self.update([input_nfa])
        end_state = self.next_state()
        self.add_end_state(end_state)
        for state in end_state_mapping[0]:
            self.add_move(state, configure.boson_lexical_epsilon_transition, start_state_mapping[0])
            self.add_move(state, configure.boson_lexical_epsilon_transition, end_state)
        start_state = self.next_state()
        self.set_start_state(start_state)
        self.add_move(start_state, configure.boson_lexical_epsilon_transition, start_state_mapping[0])

    def create_nfa_count_range(self, input_nfa, min_count: int, max_count: int) -> None:
        input_nfa_list = [input_nfa] * max_count
        start_state_mapping, end_state_mapping = self.update(input_nfa_list)
        for index in range(len(input_nfa_list)):
            if index == 0:
                self.set_start_state(start_state_mapping[index])
                if min_count == 0:
                    self.add_end_state(start_state_mapping[index])
            if index == len(input_nfa_list) - 1:
                for state in end_state_mapping[index]:
                    self.add_end_state(state)
            if index > 0:
                start_state = start_state_mapping[index]
                for previous_end_state in end_state_mapping[index - 1]:
                    self.add_move(previous_end_state, configure.boson_lexical_epsilon_transition, start_state)
            if index >= min_count - 1:
                for end_state in end_state_mapping[index]:
                    self.add_end_state(end_state)


def bs_create_nfa_character(character: str) -> LexicalNFA:
    nfa = LexicalNFA()
    nfa.create_nfa_character(character)
    return nfa


def bs_create_nfa_or(input_list: list) -> LexicalNFA:
    nfa = LexicalNFA()
    nfa.create_nfa_or(input_list)
    return nfa


def bs_create_nfa_link(input_list: list) -> LexicalNFA:
    nfa = LexicalNFA()
    nfa.create_nfa_link(input_list)
    return nfa


def bs_create_nfa_kleene_closure(input_nfa: LexicalNFA) -> LexicalNFA:
    nfa = LexicalNFA()
    nfa.create_nfa_kleene_closure(input_nfa)
    return nfa


def bs_create_nfa_plus_closure(input_nfa: LexicalNFA) -> LexicalNFA:
    nfa = LexicalNFA()
    nfa.create_nfa_plus_closure(input_nfa)
    return nfa


def bs_create_nfa_count_range(input_nfa: LexicalNFA, min_count: int, max_count: int) -> LexicalNFA:
    nfa = LexicalNFA()
    nfa.create_nfa_count_range(input_nfa, min_count, max_count)
    return nfa


def bs_create_nfa_reverse_delay_construct(reverse_character_set: set) -> LexicalNFA:
    nfa = LexicalNFA()
    nfa.create_nfa_reverse_delay_construct(reverse_character_set)
    return nfa
