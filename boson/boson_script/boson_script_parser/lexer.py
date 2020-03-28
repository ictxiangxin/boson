from .token import LexicalToken


class BosonLexer:
    def __init__(self):
        self.__token_list: list = []
        self.__line: int = 1
        self.__error_line: int = -1
        self.__no_error_line: int = -1
        self.__skip: bool = False
        self.__compact_move_table: dict = {
            0: [
                [0, {'\x5f'}, [('\x41', '\x5a'), ('\x61', '\x7a')], 1],
                [0, {'\x22'}, [], 2],
                [0, {'\x27'}, [], 31],
                [0, {'\x3c'}, [], 28],
                [0, {'\x23'}, [], 3],
                [0, {'\x25'}, [], 4],
                [0, {'\x20', '\x09'}, [], 5],
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
                [0, {'\x2a'}, [], 19],
                [0, {'\x5b'}, [], 20],
                [0, {'\x5d'}, [], 21],
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
                [0, {'\x20', '\x09'}, [], 5]
            ],
            4: [
                [0, {'\x5f'}, [('\x41', '\x5a'), ('\x61', '\x7a')], 26]
            ],
            26: [
                [0, {'\x5f'}, [('\x41', '\x5a'), ('\x61', '\x7a')], 26]
            ],
            3: [
                [2, {'\x0d', '\x0a'}, [], 3]
            ],
            28: [
                [2, {'\x5c'}, [], 27],
                [0, {'\x5c'}, [], 28]
            ],
            27: [
                [2, {'\x5c', '\x3e'}, [], 27],
                [0, {'\x5c'}, [], 28],
                [0, {'\x3e'}, [], 29]
            ],
            29: [
                [2, {'\x5c', '\x3e'}, [], 27],
                [0, {'\x5c'}, [], 28],
                [0, {'\x3e'}, [], 29]
            ],
            31: [
                [2, {'\x5c'}, [], 30],
                [0, {'\x5c'}, [], 31]
            ],
            30: [
                [2, {'\x5c', '\x27'}, [], 30],
                [0, {'\x5c'}, [], 31],
                [0, {'\x27'}, [], 32]
            ],
            32: [
                [2, {'\x5c', '\x27'}, [], 30],
                [0, {'\x5c'}, [], 31],
                [0, {'\x27'}, [], 32]
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
                [0, {'\x5c'}, [], 2],
                [0, {'\x22'}, [], 34]
            ],
            1: [
                [0, {'\x5f'}, [('\x30', '\x39'), ('\x41', '\x5a'), ('\x61', '\x7a')], 1]
            ]
        }
        self.__character_set: set = {'\x21', '\x66', '\x7b', '\x6d', '\x6c', '\x50', '\x69', '\x57', '\x0d', '\x51', '\x5f', '\x5c', '\x3e', '\x36', '\x5b', '\x3c', '\x4f', '\x48', '\x4e', '\x58', '\x70', '\x6a', '\x4a', '\x77', '\x2b', '\x4c', '\x27', '\x61', '\x63', '\x68', '\x46', '\x41', '\x22', '\x54', '\x64', '\x6f', '\x7d', '\x32', '\x0a', '\x74', '\x43', '\x09', '\x31', '\x78', '\x44', '\x7e', '\x55', '\x72', '\x79', '\x38', '\x42', '\x75', '\x6b', '\x65', '\x76', '\x59', '\x56', '\x45', '\x37', '\x4b', '\x3d', '\x23', '\x25', '\x53', '\x67', '\x2a', '\x39', '\x28', '\x7c', '\x71', '\x3b', '\x40', '\x5a', '\x73', '\x29', '\x33', '\x2c', '\x5d', '\x4d', '\x7a', '\x52', '\x6e', '\x47', '\x30', '\x34', '\x24', '\x62', '\x35', '\x3a', '\x20', '\x49'}
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
            'name': [],
            'node': [],
            'string': [],
            'regular': [],
            'comment': ['skip'],
            'command': [],
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

    def skip(self) -> None:
        self.__skip = True

    def newline(self) -> None:
        self.__line += 1

    def token_list(self) -> list:
        return self.__token_list

    def error_line(self) -> int:
        return self.__error_line

    def no_error_line(self) -> int:
        return self.__no_error_line

    def tokenize(self, text: str) -> int:
        self.__token_list = []
        self.__error_line = self.__no_error_line
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
                        self.__error_line = self.__line
                        return self.__error_line
            else:
                if get_token or state in self.__end_state_set:
                    get_token = True
                else:
                    self.__error_line = self.__line
                    return self.__error_line
            if get_token:
                self._generate_token(state, token_string)
                token_string = ''
                state = self.__start_state
                index -= 1
        if state in self.__end_state_set:
            self._generate_token(state, token_string)
        else:
            raise ValueError('Invalid state: state={}'.format(state))
        self.__token_list.append(LexicalToken('', self.__line, '$'))
        return self.__error_line

    def register_function(self, function_name: str) -> callable:
        def decorator(f: callable):
            self.__lexical_function[function_name] = f
            return f
        return decorator
