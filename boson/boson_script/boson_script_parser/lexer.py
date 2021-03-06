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
                [0, {'\x5f'}, [('\x41', '\x5a'), ('\x61', '\x7a')], 1],
                [0, {'\x22'}, [], 2],
                [0, {'\x27'}, [], 31],
                [0, {'\x3c'}, [], 28],
                [0, {'\x23'}, [], 3],
                [0, {'\x25'}, [], 4],
                [0, {'\x09', '\x20'}, [], 5],
                [0, {'\x0d'}, [], 6],
                [0, {'\x0a'}, [], 25],
                [0, {'\x3b'}, [], 7],
                [0, {'\x3d'}, [], 8],
                [0, {'\x21'}, [], 9],
                [0, {'\x40'}, [], 10],
                [0, {'\x7b'}, [], 11],
                [0, {'\x7d'}, [], 12],
                [0, {'\x2c'}, [], 13],
                [0, {'\x3a'}, [], 14],
                [0, {'\x7c'}, [], 15],
                [0, {'\x7e'}, [], 16],
                [0, {'\x28'}, [], 17],
                [0, {'\x29'}, [], 18],
                [0, {'\x5b'}, [], 19],
                [0, {'\x5d'}, [], 20],
                [0, {'\x2a'}, [], 21],
                [0, {'\x2b'}, [], 22],
                [0, {'\x24'}, [], 23]
            ],
            23: [
                [0, set(), [('\x30', '\x39')], 24]
            ],
            24: [
                [0, set(), [('\x30', '\x39')], 24]
            ],
            6: [
                [0, {'\x0a'}, [], 25]
            ],
            5: [
                [0, {'\x09', '\x20'}, [], 5]
            ],
            4: [
                [0, {'\x5f'}, [('\x41', '\x5a'), ('\x61', '\x7a')], 26]
            ],
            26: [
                [0, {'\x5f'}, [('\x41', '\x5a'), ('\x61', '\x7a')], 26]
            ],
            3: [
                [2, {'\x0a', '\x0d'}, [], 3]
            ],
            28: [
                [2, {'\x5c'}, [], 27],
                [0, {'\x5c'}, [], 28]
            ],
            27: [
                [2, {'\x3e', '\x5c'}, [], 27],
                [0, {'\x3e'}, [], 29],
                [0, {'\x5c'}, [], 28]
            ],
            29: [
                [2, {'\x3e', '\x5c'}, [], 27],
                [0, {'\x3e'}, [], 29],
                [0, {'\x5c'}, [], 28]
            ],
            31: [
                [2, {'\x5c'}, [], 30],
                [0, {'\x5c'}, [], 31]
            ],
            30: [
                [2, {'\x5c', '\x27'}, [], 30],
                [0, {'\x27'}, [], 32],
                [0, {'\x5c'}, [], 31]
            ],
            32: [
                [2, {'\x5c', '\x27'}, [], 30],
                [0, {'\x27'}, [], 32],
                [0, {'\x5c'}, [], 31]
            ],
            2: [
                [2, {'\x5c'}, [], 33],
                [0, {'\x5c'}, [], 2]
            ],
            33: [
                [0, {'\x22'}, [], 34],
                [2, {'\x22', '\x5c'}, [], 33],
                [0, {'\x5c'}, [], 2]
            ],
            34: [
                [2, {'\x22', '\x5c'}, [], 33],
                [0, {'\x22'}, [], 34],
                [0, {'\x5c'}, [], 2]
            ],
            1: [
                [0, {'\x5f'}, [('\x30', '\x39'), ('\x41', '\x5a'), ('\x61', '\x7a')], 1]
            ]
        }
        self.__character_set: set = {'\x78', '\x4b', '\x44', '\x46', '\x4f', '\x57', '\x51', '\x7d', '\x2a', '\x4e', '\x0d', '\x2b', '\x3c', '\x25', '\x73', '\x27', '\x61', '\x6a', '\x41', '\x49', '\x50', '\x54', '\x71', '\x79', '\x72', '\x43', '\x37', '\x3a', '\x6b', '\x32', '\x59', '\x7a', '\x09', '\x63', '\x56', '\x28', '\x35', '\x38', '\x24', '\x42', '\x3e', '\x52', '\x75', '\x36', '\x3d', '\x29', '\x33', '\x6e', '\x65', '\x64', '\x31', '\x5b', '\x5f', '\x5d', '\x4c', '\x48', '\x58', '\x4d', '\x7b', '\x0a', '\x6f', '\x74', '\x3b', '\x76', '\x7e', '\x5a', '\x53', '\x69', '\x47', '\x68', '\x22', '\x7c', '\x6d', '\x4a', '\x23', '\x2c', '\x45', '\x6c', '\x62', '\x55', '\x34', '\x67', '\x30', '\x40', '\x66', '\x5c', '\x20', '\x21', '\x39', '\x77', '\x70'}
        self.__start_state: int = 0
        self.__end_state_set: set = {1, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 29, 32, 34}
        self.__lexical_symbol_mapping: dict = {
            1: 'name',
            3: 'comment',
            5: 'skip',
            7: '!symbol_1',
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
            24: 'node',
            25: 'newline',
            26: 'command',
            29: 'regular',
            32: 'string',
            34: 'string'
        }
        self.__non_greedy_state_set: set = {32, 34, 29}
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
