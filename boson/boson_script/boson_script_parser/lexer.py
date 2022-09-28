from typing import Dict, List, Set

from .token import BosonToken


class BosonLexer:
    def __init__(self):
        self.__token_list: List[BosonToken] = []
        self.__line: int = 1
        self.__error_index: int = -1
        self.__no_error_index: int = -1
        self.__skip: bool = False
        self.__compact_move_table: Dict[int, List[list]] = {
            0: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 1],
                [0, {'-'}, [], 2],
                [0, {'0'}, [], 3],
                [0, set(), [('1', '9')], 4],
                [0, {'"'}, [], 37],
                [0, {'\''}, [], 34],
                [0, {'<'}, [], 31],
                [0, {'#'}, [], 5],
                [0, {'\t', ' '}, [], 6],
                [0, {'\r'}, [], 7],
                [0, {'\n'}, [], 29],
                [0, {'%'}, [], 8],
                [0, {';'}, [], 9],
                [0, {'='}, [], 10],
                [0, {'!'}, [], 11],
                [0, {'@'}, [], 12],
                [0, {'{'}, [], 13],
                [0, {'}'}, [], 14],
                [0, {','}, [], 15],
                [0, {':'}, [], 16],
                [0, {'|'}, [], 17],
                [0, {'~'}, [], 18],
                [0, {'('}, [], 19],
                [0, {')'}, [], 20],
                [0, {'['}, [], 21],
                [0, {']'}, [], 22],
                [0, {'*'}, [], 23],
                [0, {'$'}, [], 24],
                [0, {'+'}, [], 25]
            ],
            24: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 27],
                [0, set(), [('0', '9')], 26]
            ],
            26: [
                [0, set(), [('0', '9')], 26]
            ],
            27: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 27]
            ],
            8: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 28]
            ],
            28: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 28]
            ],
            7: [
                [0, {'\n'}, [], 29]
            ],
            6: [
                [0, {'\t', ' '}, [], 6]
            ],
            5: [
                [2, {'\n', '\r'}, [], 5]
            ],
            31: [
                [2, {'\\'}, [], 30],
                [0, {'\\'}, [], 31]
            ],
            30: [
                [2, {'>', '\\'}, [], 30],
                [0, {'>'}, [], 32],
                [0, {'\\'}, [], 31]
            ],
            32: [
                [2, {'>', '\\'}, [], 30],
                [0, {'>'}, [], 32],
                [0, {'\\'}, [], 31]
            ],
            34: [
                [2, {'\\'}, [], 33],
                [0, {'\\'}, [], 34]
            ],
            33: [
                [2, {'\'', '\\'}, [], 33],
                [0, {'\''}, [], 35],
                [0, {'\\'}, [], 34]
            ],
            35: [
                [2, {'\'', '\\'}, [], 33],
                [0, {'\''}, [], 35],
                [0, {'\\'}, [], 34]
            ],
            37: [
                [2, {'\\'}, [], 36],
                [0, {'\\'}, [], 37]
            ],
            36: [
                [2, {'"', '\\'}, [], 36],
                [0, {'"'}, [], 38],
                [0, {'\\'}, [], 37]
            ],
            38: [
                [2, {'"', '\\'}, [], 36],
                [0, {'"'}, [], 38],
                [0, {'\\'}, [], 37]
            ],
            4: [
                [0, set(), [('0', '9')], 4]
            ],
            3: [
                [0, set(), [('0', '9')], 4],
                [0, {'x'}, [], 39]
            ],
            39: [
                [0, set(), [('0', '9'), ('A', 'F'), ('a', 'f')], 40]
            ],
            40: [
                [0, set(), [('0', '9'), ('A', 'F'), ('a', 'f')], 40]
            ],
            2: [
                [0, set(), [('0', '9')], 4]
            ],
            1: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 1]
            ]
        }
        self.__character_set: Set[str] = {'6', 'A', '(', ')', '4', 'k', 'j', 'a', ' ', 'l', 'C', 'K', '*', '\'', '\t', 'W', '5', 'y', 'f', '}', 'H', 'i', 'T', 'F', 'D', '7', 'd', 'Y', 'r', 'Z', '@', 'R', 's', '1', '9', '"', '3', ']', '\n', ',', '#', 'M', 'L', '2', 'I', 'p', '8', '$', '>', '[', 'w', 'S', 'u', 'J', 'P', '=', 'U', 'X', 'e', 'x', '%', 't', 'g', 'V', '-', 'N', ':', 'o', 'c', 'G', '\r', '~', 'q', 'b', '+', '!', '_', ';', '<', 'O', 'z', 'n', '\\', '0', 'v', 'h', 'Q', '{', 'm', 'E', '|', 'B'}
        self.__start_state: int = 0
        self.__end_state_set: Set[int] = {1, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 32, 35, 38, 40}
        self.__lexical_symbol_mapping: Dict[int, str] = {
            1: 'name',
            3: 'number',
            4: 'number',
            5: 'comment',
            6: 'skip',
            9: '!symbol_2',
            10: '!symbol_3',
            11: '!symbol_4',
            12: '!symbol_5',
            13: '!symbol_6',
            14: '!symbol_7',
            15: '!symbol_8',
            16: '!symbol_9',
            17: '!symbol_10',
            18: '!symbol_11',
            19: '!symbol_12',
            20: '!symbol_13',
            21: '!symbol_14',
            22: '!symbol_15',
            23: '!symbol_16',
            25: '!symbol_19',
            26: '!symbol_17',
            27: '!symbol_18',
            28: '!symbol_1',
            29: 'newline',
            32: 'regular',
            35: 'string',
            38: 'string',
            40: 'number'
        }
        self.__non_greedy_state_set: Set[int] = {32, 35, 38}
        self.__symbol_function_mapping: Dict[str, List[str]] = {
            'comment': ['skip'],
            'skip': ['skip'],
            'newline': ['skip', 'newline']
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
            self.__token_list.append(BosonToken(token_string, self.__line, symbol))

    def token_list(self) -> List[BosonToken]:
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
        self.__token_list: List[BosonToken] = []
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
        self.__token_list.append(BosonToken('', self.__line, '$'))
        return self.__error_index

    def register_function(self, function_name: str) -> callable:
        def decorator(f: callable):
            self.__lexical_function[function_name] = f
            return f
        return decorator
