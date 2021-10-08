from .token import LexicalToken


class BosonLexer:
    def __init__(self):
        self.__token_list: list = []
        self.__line: int = 1
        self.__error_index: int = -1
        self.__no_error_index: int = -1
        self.__skip: bool = False
        self.__compact_move_table: dict = {
            0: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 1],
                [0, {'$'}, [], 2],
                [0, {'-'}, [], 3],
                [0, set(), [('1', '9')], 4],
                [0, {'0'}, [], 5],
                [0, {'"'}, [], 35],
                [0, {'\''}, [], 32],
                [0, {'<'}, [], 6],
                [0, {'#'}, [], 28],
                [0, {'%'}, [], 7],
                [0, {'\t', ' '}, [], 8],
                [0, {'\r'}, [], 9],
                [0, {'\n'}, [], 10],
                [0, {';'}, [], 11],
                [0, {'='}, [], 12],
                [0, {'!'}, [], 13],
                [0, {'@'}, [], 14],
                [0, {'{'}, [], 15],
                [0, {'}'}, [], 16],
                [0, {','}, [], 17],
                [0, {':'}, [], 18],
                [0, {'|'}, [], 19],
                [0, {'~'}, [], 20],
                [0, {'('}, [], 21],
                [0, {')'}, [], 22],
                [0, {'['}, [], 23],
                [0, {']'}, [], 24],
                [0, {'*'}, [], 25],
                [0, {'+'}, [], 26]
            ],
            9: [
                [0, {'\n'}, [], 10]
            ],
            8: [
                [0, {'\t', ' '}, [], 8]
            ],
            7: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 27]
            ],
            27: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 27]
            ],
            28: [
                [2, {'\n', '\r'}, [], 28]
            ],
            6: [
                [2, {'\\'}, [], 29],
                [0, {'\\'}, [], 6]
            ],
            29: [
                [2, {'\\', '>'}, [], 29],
                [0, {'\\'}, [], 6],
                [0, {'>'}, [], 30]
            ],
            30: [
                [2, {'\\', '>'}, [], 29],
                [0, {'\\'}, [], 6],
                [0, {'>'}, [], 30]
            ],
            32: [
                [2, {'\\'}, [], 31],
                [0, {'\\'}, [], 32]
            ],
            31: [
                [2, {'\\', '\''}, [], 31],
                [0, {'\\'}, [], 32],
                [0, {'\''}, [], 33]
            ],
            33: [
                [2, {'\\', '\''}, [], 31],
                [0, {'\\'}, [], 32],
                [0, {'\''}, [], 33]
            ],
            35: [
                [2, {'\\'}, [], 34],
                [0, {'\\'}, [], 35]
            ],
            34: [
                [2, {'\\', '"'}, [], 34],
                [0, {'"'}, [], 36],
                [0, {'\\'}, [], 35]
            ],
            36: [
                [2, {'\\', '"'}, [], 34],
                [0, {'"'}, [], 36],
                [0, {'\\'}, [], 35]
            ],
            5: [
                [0, set(), [('0', '9')], 4],
                [0, {'x'}, [], 37]
            ],
            37: [
                [0, set(), [('0', '9'), ('A', 'F'), ('a', 'f')], 38]
            ],
            38: [
                [0, set(), [('0', '9'), ('A', 'F'), ('a', 'f')], 38]
            ],
            4: [
                [0, set(), [('0', '9')], 4]
            ],
            3: [
                [0, set(), [('0', '9')], 4]
            ],
            2: [
                [0, set(), [('0', '9')], 39]
            ],
            39: [
                [0, set(), [('0', '9')], 39]
            ],
            1: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 1]
            ]
        }
        self.__character_set: set = {'m', 'I', '%', 't', '\t', 'z', 'D', 'Q', 'C', 'i', 'P', 'H', '\\', '!', 'n', '[', 'o', '$', 'F', 'g', 'd', 's', 'c', '\r', 'y', '\n', 'v', '"', 'q', ']', 'L', 'R', 'U', '(', '{', 'h', 'k', 'j', 'b', 'a', 'X', '4', '}', 'J', ':', '-', 'Z', '0', ',', '*', '@', '3', '7', 'M', 'l', 'W', 'f', 'S', 'B', 'A', '5', ')', '9', 'u', 'N', 'O', 'Y', '1', '=', 'x', 'E', 'G', '2', '>', '<', '~', '_', '8', 'K', '#', '\'', 'V', '|', 'w', ' ', 'e', 'r', '6', ';', '+', 'p', 'T'}
        self.__start_state: int = 0
        self.__end_state_set: set = {1, 4, 5, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 33, 36, 38, 39}
        self.__lexical_symbol_mapping: dict = {
            1: 'name',
            4: 'number',
            5: 'number',
            8: 'skip',
            10: 'newline',
            11: '!symbol_1',
            12: '!symbol_2',
            13: '!symbol_3',
            14: '!symbol_4',
            15: '!symbol_5',
            16: '!symbol_6',
            17: '!symbol_7',
            18: '!symbol_8',
            19: '!symbol_9',
            20: '!symbol_10',
            21: '!symbol_11',
            22: '!symbol_12',
            23: '!symbol_13',
            24: '!symbol_14',
            25: '!symbol_15',
            26: '!symbol_16',
            27: 'command',
            28: 'comment',
            30: 'regular',
            33: 'string',
            36: 'string',
            38: 'number',
            39: 'node'
        }
        self.__non_greedy_state_set: set = {33, 36, 30}
        self.__symbol_function_mapping: dict = {
            'comment': ['skip'],
            'skip': ['skip'],
            'newline': ['skip', 'newline']
        }
        self.__lexical_function: dict = {}

    def _invoke_lexical_function(self, symbol: str, token_string: str) -> str:
        self.__skip = False
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
        symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
        token_string = self._invoke_lexical_function(symbol, token_string)
        if not self.__skip:
            self.__token_list.append(LexicalToken(token_string, self.__line, symbol))

    def token_list(self) -> list:
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
        self.__token_list = []
        self.__error_index = self.__no_error_index
        self.__line = 1
        state = self.__start_state
        token_string = ''
        index = 0
        while index < len(text):
            character = text[index]
            index += 1
            get_token = False
            if state in self.__non_greedy_state_set:
                get_token = True
            if not get_token and state in self.__compact_move_table:
                for attribute, character_set, range_list, next_state in self.__compact_move_table[state]:
                    if attribute == 2:
                        condition = character not in character_set
                        for min_character, max_character in range_list:
                            condition &= character < min_character or character > max_character
                    else:
                        condition = character in character_set
                        if attribute == 1 and character not in self.__character_set:
                            condition = True
                        for min_character, max_character in range_list:
                            if condition or min_character <= character <= max_character:
                                condition = True
                                break
                    if condition:
                        token_string += character
                        state = next_state
                        break
                else:
                    if state in self.__end_state_set:
                        get_token = True
                    else:
                        self.__error_index = index - 1
                        return self.__error_index
            else:
                if get_token or state in self.__end_state_set:
                    get_token = True
                else:
                    self.__error_index = index - 1
                    return self.__error_index
            if get_token:
                self._generate_token(state, token_string)
                token_string = ''
                state = self.__start_state
                index -= 1
        if state in self.__end_state_set:
            self._generate_token(state, token_string)
        else:
            self.__error_index = index - 1
            return self.__error_index
        self.__token_list.append(LexicalToken('', self.__line, '$'))
        return self.__error_index

    def register_function(self, function_name: str) -> callable:
        def decorator(f: callable):
            self.__lexical_function[function_name] = f
            return f
        return decorator
