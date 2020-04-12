import boson.configure as configure


class LexicalDFA:
    def __init__(self):
        self.__move_table: dict = {}
        self.__start_state: int = configure.boson_lexical_default_state
        self.__end_state_set: set = set()
        self.__state_set: set = set()
        self.__lexical_symbol_mapping: dict = {}
        self.__lexical_symbol_number_mapping: dict = {}
        self.__character_set: set = set()

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

    def add_lexical_symbol(self, state: int, lexical_symbol_tuple: tuple) -> None:
        symbol, number = lexical_symbol_tuple
        if state in self.__lexical_symbol_number_mapping:
            if self.__lexical_symbol_number_mapping[state] < number:
                return
        self.__lexical_symbol_number_mapping[state] = number
        self.__lexical_symbol_mapping[state] = symbol

    def set_character_set(self, character_set: set) -> None:
        self.__character_set = set(character_set)

    def move_table(self) -> dict:
        return self.__move_table

    def character_set(self) -> set:
        return self.__character_set

    def start_state(self) -> int:
        return self.__start_state

    def end_state_set(self) -> set:
        return self.__end_state_set

    def lexical_symbol_mapping(self) -> dict:
        return self.__lexical_symbol_mapping

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
        self.__start_state = new_state_number_mapping.get(self.__start_state, configure.boson_lexical_default_start_state)
        self.__end_state_set = new_end_state_set
        self.__lexical_symbol_mapping = new_lexical_symbol_mapping
