from typing import Optional, List, Dict, Tuple, Set

import boson.configure as configure


class LexicalDFA:
    def __init__(self):
        self.__move_table: Dict[int, Dict[str, int]] = {}
        self.__start_state: int = configure.boson_lexical_default_state
        self.__end_state_set: Set[int] = set()
        self.__state_set: Set[int] = set()
        self.__lexical_symbol_mapping: Dict[int, str] = {}
        self.__lexical_symbol_number_mapping: Dict[int, int] = {}
        self.__character_set: Set[str] = set()

    def __alphabet(self, state_group: Set[int]) -> Set[Optional[str]]:
        alphabet: Set[Optional[str]] = set()
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

    def add_lexical_symbol(self, state: int, lexical_symbol_tuple: Tuple[str, Optional[int]]) -> None:
        symbol, number = lexical_symbol_tuple
        if number is not None and state in self.__lexical_symbol_number_mapping:
            old_number: int = self.__lexical_symbol_number_mapping[state]
            if old_number is None or old_number < number:
                return
        self.__lexical_symbol_number_mapping[state] = number
        self.__lexical_symbol_mapping[state] = symbol

    def set_character_set(self, character_set: Set[str]) -> None:
        self.__character_set: Set[str] = set(character_set)

    def move_table(self) -> Dict[int, Dict[str, int]]:
        return self.__move_table

    def character_set(self) -> Set[str]:
        return self.__character_set

    def start_state(self) -> int:
        return self.__start_state

    def end_state_set(self) -> Set[int]:
        return self.__end_state_set

    def lexical_symbol_mapping(self) -> Dict[int, str]:
        return self.__lexical_symbol_mapping

    def minimize(self) -> None:
        group_number: int = 0
        state_group_number: Dict[int, int] = {}
        state_group_wait_list: List[Set[int]] = [set(self.__state_set - self.__end_state_set), set(self.__end_state_set)]
        state_group_checked_list: List[Set[int]] = []
        for state_group in state_group_wait_list:
            for state in state_group:
                state_group_number[state] = group_number
            group_number += 1
        group_changed: bool = True
        while group_changed:
            group_changed: bool = False
            while len(state_group_wait_list) > 0:
                state_group: Set[int] = state_group_wait_list.pop()
                if len(state_group) > 1:
                    check_pass: bool = True
                    group_changed: bool = False
                    for character in self.__alphabet(state_group) | {None}:
                        split_group: Dict[int | Tuple[int, str], Set[int]] = {}
                        for state in state_group:
                            move_state: int = self.__move(state, character)
                            move_group_number: int = state_group_number.get(move_state, -1)
                            if state in self.__lexical_symbol_mapping:
                                move_group_number: Tuple[int, str] = (move_group_number, self.__lexical_symbol_mapping[state])
                            split_group.setdefault(move_group_number, set())
                            split_group[move_group_number].add(state)
                        if len(split_group) > 1:
                            for _, group in split_group.items():
                                for state in group:
                                    state_group_number[state] = group_number
                                group_number += 1
                                state_group_wait_list.append(group)
                            group_changed: bool = True
                            check_pass: bool = False
                            break
                    if check_pass:
                        state_group_checked_list.append(state_group)
            if group_changed:
                state_group_wait_list: List[Set[int]] = state_group_checked_list
                state_group_checked_list: List[Set[int]] = []
        for merge_group in state_group_checked_list:
            base_state: int = merge_group.pop()
            base_state_move_table: Dict[str, int] = self.__move_table.get(base_state, {})
            if self.__start_state in merge_group:
                self.__start_state: int = base_state
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
        new_state_number_mapping: Dict[int, int] = {}
        new_number: int = 0
        for state in self.__state_set:
            new_state_number_mapping[state] = new_number
            new_number += 1
        new_move_table: Dict[int, Dict[str, int]] = {}
        for from_state, move_table in self.__move_table.items():
            state_move_table: Dict[str, int] = {}
            for symbol, to_state in move_table.items():
                state_move_table[symbol] = new_state_number_mapping[to_state]
            new_move_table[new_state_number_mapping[from_state]] = state_move_table
        new_end_state_set: Set[int] = set()
        for state in self.__end_state_set:
            new_end_state_set.add(new_state_number_mapping[state])
        new_lexical_symbol_mapping: Dict[int, str] = {}
        for state, lexical_symbol in self.__lexical_symbol_mapping.items():
            new_lexical_symbol_mapping[new_state_number_mapping[state]] = lexical_symbol
        self.__move_table: Dict[int, Dict[str, int]] = new_move_table
        self.__state_set: Set[int] = set(range(new_number))
        self.__start_state: int = new_state_number_mapping.get(self.__start_state, configure.boson_lexical_default_start_state)
        self.__end_state_set: Set[int] = new_end_state_set
        self.__lexical_symbol_mapping: Dict[int, str] = new_lexical_symbol_mapping
