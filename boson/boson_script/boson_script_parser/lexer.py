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
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 41],
                [0, {'-'}, [], 1],
                [0, set(), [('1', '9')], 2],
                [0, {'0'}, [], 3],
                [0, {'"'}, [], 37],
                [0, {'\''}, [], 34],
                [0, {'<'}, [], 31],
                [0, {'#'}, [], 4],
                [0, {' ', '\t'}, [], 5],
                [0, {'\r'}, [], 6],
                [0, {'\n'}, [], 29],
                [0, {'%'}, [], 7],
                [0, {';'}, [], 8],
                [0, {'='}, [], 9],
                [0, {'!'}, [], 10],
                [0, {'@'}, [], 11],
                [0, {'{'}, [], 12],
                [0, {'}'}, [], 13],
                [0, {','}, [], 14],
                [0, {':'}, [], 15],
                [0, {'|'}, [], 16],
                [0, {'~'}, [], 17],
                [0, {'('}, [], 18],
                [0, {')'}, [], 19],
                [0, {'['}, [], 20],
                [0, {']'}, [], 21],
                [0, {'*'}, [], 22],
                [0, {'$'}, [], 23],
                [0, {'+'}, [], 24],
                [0, {'?'}, [], 25]
            ],
            23: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 27],
                [0, set(), [('0', '9')], 26]
            ],
            26: [
                [0, set(), [('0', '9')], 26]
            ],
            27: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 27]
            ],
            7: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 28]
            ],
            28: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 28]
            ],
            6: [
                [0, {'\n'}, [], 29]
            ],
            5: [
                [0, {' ', '\t'}, [], 5]
            ],
            4: [
                [2, {'\r', '\n'}, [], 4]
            ],
            31: [
                [2, {'\\'}, [], 30],
                [0, {'\\'}, [], 31]
            ],
            30: [
                [2, {'\\', '>'}, [], 30],
                [0, {'>'}, [], 32],
                [0, {'\\'}, [], 31]
            ],
            32: [
                [2, {'\\', '>'}, [], 30],
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
            3: [
                [0, set(), [('0', '9')], 2],
                [0, {'x'}, [], 39]
            ],
            39: [
                [0, set(), [('0', '9'), ('A', 'F'), ('a', 'f')], 40]
            ],
            40: [
                [0, set(), [('0', '9'), ('A', 'F'), ('a', 'f')], 40]
            ],
            2: [
                [0, set(), [('0', '9')], 2]
            ],
            1: [
                [0, set(), [('0', '9')], 2]
            ],
            41: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 41]
            ]
        }
        self.__character_set: Set[str] = {'y', '!', '\'', 'B', 'x', 'w', '1', ']', 'm', '@', 'r', 'Y', '[', 'u', 'C', 'Q', '4', 'M', 'p', ',', '$', 'D', '(', '0', '{', 'Z', 'a', 't', 'G', ':', 's', '#', 'K', 'S', '*', 'e', 'A', '}', 'f', 'h', 'F', 'l', 'H', '3', 'I', 'U', 'P', 'b', '>', '-', '=', '|', 'd', ')', '5', 'R', 'k', ' ', 'n', '\n', '~', '?', 'i', '"', '\t', 'g', 'o', 'N', '9', 'X', '\r', '_', 'j', '\\', 'L', 'v', 'E', 'W', '6', 'z', ';', 'V', 'c', '2', '8', '7', '+', 'O', '%', '<', 'J', 'T', 'q'}
        self.__start_state: int = 0
        self.__end_state_set: Set[int] = {2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 32, 35, 38, 40, 41}
        self.__lexical_symbol_mapping: Dict[int, str] = {
            2: 'number',
            3: 'number',
            4: 'comment',
            5: 'skip',
            8: '!symbol_2',
            9: '!symbol_3',
            10: '!symbol_4',
            11: '!symbol_5',
            12: '!symbol_6',
            13: '!symbol_7',
            14: '!symbol_8',
            15: '!symbol_9',
            16: '!symbol_10',
            17: '!symbol_11',
            18: '!symbol_12',
            19: '!symbol_13',
            20: '!symbol_14',
            21: '!symbol_15',
            22: '!symbol_16',
            24: '!symbol_19',
            25: '!symbol_20',
            26: '!symbol_17',
            27: '!symbol_18',
            28: '!symbol_1',
            29: 'newline',
            32: 'regular',
            35: 'string',
            38: 'string',
            40: 'number',
            41: 'name'
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
