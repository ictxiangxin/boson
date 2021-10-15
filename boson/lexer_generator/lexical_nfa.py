from typing import Optional, List, Dict, Tuple, Set, FrozenSet

import boson.configure as configure
from boson.lexer_generator.lexical_dfa import LexicalDFA
from boson.system.logger import logger


class LexicalNFA:
    def __init__(self):
        self.__move_table: Dict[int, Dict[str, Set[int]]] = {}
        self.__start_state: int = configure.boson_lexical_default_start_state
        self.__end_state_set: Set[int] = set()
        self.__state_set: Set[int] = set()
        self.__character_set: Set[str] = set()
        self.__state_epsilon_closure_mapping: Dict[int, Set[int]] = {}
        self.__lexical_symbol_mapping: Dict[int, Tuple[str, Optional[int]]] = {}
        self.__reverse_delay_construct: bool = False
        self.__reverse_character_set: Set[str] = set()
        self.__delay_construct_reverse_set_list: List[Set[str]] = []
        self.__delay_construct_base_state_list: List[Tuple[int, int]] = []

    def __generate_state_epsilon_closure_mapping(self) -> None:
        self.__state_epsilon_closure_mapping: Dict[int, Set[int]] = {}
        for state, state_move_table in self.__move_table.items():
            epsilon_transition_set: Optional[Set[int]] = state_move_table.get(configure.boson_lexical_epsilon_transition, None)
            if epsilon_transition_set:
                self.__state_epsilon_closure_mapping[state] = set(epsilon_transition_set)
        available_state_set: Set[int] = set(self.__state_epsilon_closure_mapping)
        variable_state_set: Set[int] = set(self.__state_epsilon_closure_mapping)
        continue_loop: bool = True
        while continue_loop:
            continue_loop: bool = False
            for state, epsilon_closure in self.__state_epsilon_closure_mapping.items():
                if state in variable_state_set:
                    update_state_set: Set[int] = available_state_set & epsilon_closure
                    if update_state_set:
                        update_closure: Set[int] = set(epsilon_closure)
                        for update_state in update_state_set:
                            update_closure |= self.__state_epsilon_closure_mapping[update_state]
                        if len(epsilon_closure) < len(update_closure):
                            self.__state_epsilon_closure_mapping[state] = update_closure
                            continue_loop: bool = True
                    else:
                        variable_state_set.remove(state)

    def set_start_state(self, state: int) -> None:
        self.__start_state: int = state

    def add_end_state(self, state: int) -> None:
        self.__end_state_set.add(state)

    def add_move(self, from_state: int, character: str, to_state: int) -> None:
        self.__state_set.add(from_state)
        self.__state_set.add(to_state)
        self.__character_set.add(character)
        self.__move_table.setdefault(from_state, {})
        self.__move_table[from_state].setdefault(character, set())
        self.__move_table[from_state][character].add(to_state)

    def construct(self, full_character_set: Optional[Set[str]] = None) -> None:
        logger.info('[Lexical NFA] Construct Lexer NFA.')
        if full_character_set is None:
            full_character_set: Set[str] = self.character_set()
        if self.__reverse_delay_construct:
            for pass_character in full_character_set - self.reverse_character_set():
                self.add_move(configure.boson_lexical_default_start_state, pass_character, configure.boson_lexical_default_end_state)
            self.__reverse_delay_construct: bool = False
        for reverse_character_set, delay_base_state in self.delay_construct_list():
            for pass_character in full_character_set - reverse_character_set:
                self.add_move(delay_base_state[0], pass_character, delay_base_state[1])

    def reverse_delay_construct(self) -> bool:
        return self.__reverse_delay_construct

    def reverse_character_set(self) -> Set[str]:
        return self.__reverse_character_set

    def delay_construct_list(self) -> zip:
        return zip(self.__delay_construct_reverse_set_list, self.__delay_construct_base_state_list)

    def character_set(self) -> Set[str]:
        return self.__character_set - {configure.boson_lexical_epsilon_transition, configure.boson_lexical_wildcard}

    def state_set(self) -> Set[int]:
        return self.__state_set

    def start_state(self) -> int:
        return self.__start_state

    def end_state_set(self) -> Set[int]:
        return self.__end_state_set

    def move_table(self) -> Dict[int, Dict[str, Set[int]]]:
        return self.__move_table

    def transform_to_dfa(self) -> LexicalDFA:
        logger.info('[Lexical NFA] Transform Lexer NFA to DFA.')
        self.__generate_state_epsilon_closure_mapping()
        dfa_state_number: int = configure.boson_lexical_default_state
        dfa_entity: LexicalDFA = LexicalDFA()
        dfa_start_state: FrozenSet[int] = frozenset(self.__state_epsilon_closure_mapping.get(self.__start_state, set()) | {self.__start_state})
        dfa_state_number_mapping: Dict[FrozenSet[int], int] = {dfa_start_state: dfa_state_number}
        dfa_entity.set_start_state(dfa_state_number)
        if self.end_state_set() & dfa_start_state:
            dfa_entity.add_end_state(dfa_state_number)
        dfa_state_number += 1
        lexical_end_state_set: Set[int] = set(self.__lexical_symbol_mapping)
        dfa_state_wait_list: List[FrozenSet[int]] = [dfa_start_state]
        while dfa_state_wait_list:
            dfa_state: FrozenSet[int] = dfa_state_wait_list.pop()
            from_state_number: int = dfa_state_number_mapping[dfa_state]
            move_closure_mapping: Dict[str, Set[int]] = {}
            for nfa_state in dfa_state:
                for character, next_state_set in self.__move_table.get(nfa_state, {}).items():
                    if character != configure.boson_lexical_epsilon_transition:
                        move_closure_mapping.setdefault(character, set())
                        move_closure_mapping[character] |= next_state_set
            for character, move_closure in move_closure_mapping.items():
                move_closure_epsilon_closure: Set[int] = set()
                for nfa_state in move_closure:
                    move_closure_epsilon_closure |= self.__state_epsilon_closure_mapping.get(nfa_state, set())
                new_dfa_state = frozenset(move_closure | move_closure_epsilon_closure)
                if new_dfa_state in dfa_state_number_mapping:
                    to_state_number: int = dfa_state_number_mapping[new_dfa_state]
                else:
                    to_state_number: int = dfa_state_number
                    dfa_state_number_mapping[new_dfa_state] = dfa_state_number
                    dfa_state_number += 1
                    dfa_state_wait_list.append(new_dfa_state)
                dfa_entity.add_move(from_state_number, character, to_state_number)
                if len(self.end_state_set() & new_dfa_state) > 0:
                    dfa_entity.add_end_state(to_state_number)
                for lexical_state in lexical_end_state_set & new_dfa_state:
                    dfa_entity.add_lexical_symbol(to_state_number, self.__lexical_symbol_mapping[lexical_state])
        dfa_entity.set_character_set(self.character_set())
        return dfa_entity

    def next_state(self) -> int:
        return max(self.state_set()) + 1 if len(self.state_set()) > 0 else configure.boson_lexical_default_state

    def update(self, input_nfa_list: list) -> Tuple[Dict[int, int], Dict[int, Set[int]]]:
        start_state_mapping: Dict[int, int] = {}
        end_state_mapping: Dict[int, Set[int]] = {}
        global_state_number: int = self.next_state()
        for index, input_nfa in enumerate(input_nfa_list):
            if input_nfa.reverse_delay_construct():
                self.__delay_construct_reverse_set_list.append(input_nfa.reverse_character_set())
            temp_state_mapping: Dict[int, int] = {}
            end_state_mapping.setdefault(index, set())
            for from_state, move_table in input_nfa.move_table().items():
                is_start_state: bool = from_state == input_nfa.start_state()
                is_end_state: bool = from_state in input_nfa.end_state_set()
                if from_state in temp_state_mapping:
                    from_state: int = temp_state_mapping[from_state]
                else:
                    temp_state_mapping[from_state] = global_state_number
                    from_state: int = global_state_number
                    global_state_number += 1
                if is_start_state:
                    start_state_mapping[index] = from_state
                if is_end_state:
                    end_state_mapping[index].add(from_state)
                for character, to_state_set in move_table.items():
                    for to_state in to_state_set:
                        is_end_state: bool = to_state in input_nfa.end_state_set()
                        if to_state in temp_state_mapping:
                            to_state: int = temp_state_mapping[to_state]
                        else:
                            temp_state_mapping[to_state] = global_state_number
                            to_state: int = global_state_number
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

    def add_lexical_symbol(self, lexical_nfa, lexical_symbol_tuple: Tuple[str, int]) -> None:
        default_start_state: int = configure.boson_lexical_default_start_state
        if not self.__state_set:
            self.__state_set.add(default_start_state)
        start_state_mapping, end_state_mapping = self.update([lexical_nfa])
        self.add_move(default_start_state, configure.boson_lexical_epsilon_transition, start_state_mapping[0])
        for state in end_state_mapping[0]:
            self.__lexical_symbol_mapping[state] = lexical_symbol_tuple
            self.add_end_state(state)

    def create_nfa_reverse_delay_construct(self, reverse_character_set: Set[str]) -> None:
        self.__reverse_delay_construct: bool = True
        self.__reverse_character_set: Set[str] = set(reverse_character_set)
        self.__character_set |= reverse_character_set
        self.add_move(configure.boson_lexical_default_start_state, configure.boson_lexical_wildcard, configure.boson_lexical_default_end_state)
        self.set_start_state(configure.boson_lexical_default_start_state)
        self.add_end_state(configure.boson_lexical_default_end_state)

    def create_nfa_character(self, character: str) -> None:
        self.add_move(configure.boson_lexical_default_start_state, character, configure.boson_lexical_default_end_state)
        self.set_start_state(configure.boson_lexical_default_start_state)
        self.add_end_state(configure.boson_lexical_default_end_state)

    def create_nfa_character_set(self, character_set: set) -> None:
        for character in character_set:
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
                start_state: int = start_state_mapping[index]
                for previous_end_state in end_state_mapping[index - 1]:
                    self.add_move(previous_end_state, configure.boson_lexical_epsilon_transition, start_state)

    def create_nfa_or(self, input_nfa_list: list) -> None:
        start_state_mapping, end_state_mapping = self.update(input_nfa_list)
        start_state: int = self.next_state()
        self.set_start_state(start_state)
        for _, state in start_state_mapping.items():
            self.add_move(start_state, configure.boson_lexical_epsilon_transition, state)
        end_state: int = self.next_state()
        self.add_end_state(end_state)
        for _, end_state_set in end_state_mapping.items():
            for state in end_state_set:
                self.add_move(state, configure.boson_lexical_epsilon_transition, end_state)

    def create_nfa_kleene_closure(self, input_nfa) -> None:
        start_state_mapping, end_state_mapping = self.update([input_nfa])
        end_state: int = self.next_state()
        self.add_end_state(end_state)
        for state in end_state_mapping[0]:
            self.add_move(state, configure.boson_lexical_epsilon_transition, start_state_mapping[0])
            self.add_move(state, configure.boson_lexical_epsilon_transition, end_state)
        start_state: int = self.next_state()
        self.set_start_state(start_state)
        self.add_move(start_state, configure.boson_lexical_epsilon_transition, start_state_mapping[0])
        self.add_move(start_state, configure.boson_lexical_epsilon_transition, end_state)

    def create_nfa_plus_closure(self, input_nfa) -> None:
        start_state_mapping, end_state_mapping = self.update([input_nfa])
        end_state: int = self.next_state()
        self.add_end_state(end_state)
        for state in end_state_mapping[0]:
            self.add_move(state, configure.boson_lexical_epsilon_transition, start_state_mapping[0])
            self.add_move(state, configure.boson_lexical_epsilon_transition, end_state)
        start_state: int = self.next_state()
        self.set_start_state(start_state)
        self.add_move(start_state, configure.boson_lexical_epsilon_transition, start_state_mapping[0])

    def create_nfa_count_range(self, input_nfa, min_count: int, max_count: int) -> None:
        input_nfa_list: list = [input_nfa] * max_count
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


def bs_create_nfa_character_set(character_set: Set[str]) -> LexicalNFA:
    nfa = LexicalNFA()
    nfa.create_nfa_character_set(character_set)
    return nfa


def bs_create_nfa_or(input_list: List[LexicalNFA]) -> LexicalNFA:
    nfa = LexicalNFA()
    nfa.create_nfa_or(input_list)
    return nfa


def bs_create_nfa_link(input_list: List[LexicalNFA]) -> LexicalNFA:
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


def bs_create_nfa_reverse_delay_construct(reverse_character_set: Set[str]) -> LexicalNFA:
    nfa = LexicalNFA()
    nfa.create_nfa_reverse_delay_construct(reverse_character_set)
    return nfa
