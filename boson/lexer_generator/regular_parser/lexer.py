from typing import Dict, List, Set

from .token import RegularToken


class RegularLexer:
    def __init__(self):
        self.__token_list: List[RegularToken] = []
        self.__line: int = 1
        self.__error_index: int = -1
        self.__no_error_index: int = -1
        self.__skip: bool = False
        self.__compact_move_table: Dict[int, List[list]] = {
            0: [
                [0, {'{'}, [], 1],
                [0, {'|'}, [], 2],
                [0, {'.'}, [], 3],
                [0, {'\\'}, [], 4],
                [2, {'?'}, [('(', '.'), ('0', '9'), ('[', '^'), ('{', '}')], 5],
                [0, set(), [('0', '9')], 6],
                [0, {'['}, [], 7],
                [0, {'^'}, [], 8],
                [0, {']'}, [], 9],
                [0, {'('}, [], 10],
                [0, {')'}, [], 11],
                [0, {'-'}, [], 12],
                [0, {'+'}, [], 13],
                [0, {'*'}, [], 14],
                [0, {'?'}, [], 15],
                [0, {','}, [], 16],
                [0, {'}'}, [], 17]
            ],
            4: [
                [2, {'u'}, [], 18],
                [0, {'u'}, [], 19]
            ],
            19: [
                [0, set(), [('0', '9'), ('A', 'F'), ('a', 'f')], 20]
            ],
            20: [
                [0, set(), [('0', '9'), ('A', 'F'), ('a', 'f')], 21]
            ],
            21: [
                [0, set(), [('0', '9'), ('A', 'F'), ('a', 'f')], 22]
            ],
            22: [
                [0, set(), [('0', '9'), ('A', 'F'), ('a', 'f')], 23]
            ],
            1: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 24]
            ],
            24: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 24],
                [0, {'}'}, [], 25]
            ]
        }
        self.__character_set: Set[str] = {'6', '_', '7', 'x', '0', 'O', '9', 'l', '-', '1', 'b', 'P', 'F', 'e', 'Y', 'o', 'k', 'd', '^', 'n', 'W', '.', 'G', ')', '}', 'u', 'N', 'p', ']', 'A', ',', 'q', 't', 'f', 'Z', '8', 'R', '{', 'K', 'L', 'Q', '+', 'T', 'U', 'i', 'y', 'a', 'I', 'j', 'm', 'B', '3', 'C', '|', '*', 'J', 'h', 's', 'D', 'S', 'r', 'H', 'V', 'v', 'X', '[', 'w', 'M', 'z', '2', '?', '4', 'g', 'E', '5', 'c', '(', '\\'}
        self.__start_state: int = 0
        self.__end_state_set: Set[int] = {1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 23, 25}
        self.__lexical_symbol_mapping: Dict[int, str] = {
            1: '!symbol_16',
            2: '!symbol_1',
            3: '!symbol_2',
            5: '!symbol_4',
            6: '!symbol_6',
            7: '!symbol_7',
            8: '!symbol_8',
            9: '!symbol_9',
            10: '!symbol_10',
            11: '!symbol_11',
            12: '!symbol_12',
            13: '!symbol_13',
            14: '!symbol_14',
            15: '!symbol_15',
            16: '!symbol_17',
            17: '!symbol_18',
            18: '!symbol_3',
            19: '!symbol_3',
            23: '!symbol_5',
            25: 'reference'
        }
        self.__non_greedy_state_set: Set[int] = set()
        self.__symbol_function_mapping: Dict[str, List[str]] = {
            'reference': ['reference']
        }
        self.__lexical_function: Dict[str, callable] = {}

    def _invoke_lexical_function(self, symbol: str, token_string: str) -> str:
        self.__skip: bool = False
        if symbol in self.__symbol_function_mapping:
            for function in self.__symbol_function_mapping[symbol]:
                if function in self.__lexical_function:
                    token_string = self.__lexical_function[function](token_string)
                elif function == 'skip':
                    self.skip()
                elif function == 'newline':
                    self.newline()
        return token_string

    def _generate_token(self, state: int, token_string: str) -> None:
        symbol: str = self.__lexical_symbol_mapping.get(state, '!symbol')
        token_string: str = self._invoke_lexical_function(symbol, token_string)
        if not self.__skip:
            self.__token_list.append(RegularToken(token_string, self.__line, symbol))

    def token_list(self) -> List[RegularToken]:
        return self.__token_list

    def line(self) -> int:
        return self.__line

    def skip(self) -> None:
        self.__skip = True

    def newline(self) -> None:
        self.__line += 1

    def error_index(self) -> int:
        return self.__error_index

    def no_error_index(self) -> int:
        return self.__no_error_index

    def tokenize(self, text: str) -> int:
        self.__token_list: List[RegularToken] = []
        self.__error_index: int = self.__no_error_index
        self.__line: int = 1
        state: int = self.__start_state
        token_string: str = ''
        index: int = 0
        while index < len(text):
            character: str = text[index]
            index += 1
            get_token: bool = False
            if state in self.__non_greedy_state_set:
                get_token: bool = True
            if not get_token and state in self.__compact_move_table:
                for attribute, character_set, range_list, next_state in self.__compact_move_table[state]:
                    if attribute == 2:
                        condition: bool = character not in character_set
                        for min_character, max_character in range_list:
                            condition &= character < min_character or character > max_character
                    else:
                        condition: bool = character in character_set
                        if attribute == 1 and character not in self.__character_set:
                            condition: bool = True
                        for min_character, max_character in range_list:
                            if condition or min_character <= character <= max_character:
                                condition: bool = True
                                break
                    if condition:
                        token_string += character
                        state: int = next_state
                        break
                else:
                    if state in self.__end_state_set:
                        get_token: bool = True
                    else:
                        self.__error_index: int = index - 1
                        return self.__error_index
            else:
                if get_token or state in self.__end_state_set:
                    get_token: bool = True
                else:
                    self.__error_index: int = index - 1
                    return self.__error_index
            if get_token:
                self._generate_token(state, token_string)
                token_string: str = ''
                state: int = self.__start_state
                index -= 1
        if state in self.__end_state_set:
            self._generate_token(state, token_string)
        else:
            self.__error_index: int = index - 1
            return self.__error_index
        self.__token_list.append(RegularToken('', self.__line, '$'))
        return self.__error_index

    def register_function(self, function_name: str) -> callable:
        def decorator(f: callable):
            self.__lexical_function[function_name] = f
            return f
        return decorator
