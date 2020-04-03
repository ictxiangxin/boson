from .token import RegularToken


class RegularLexer:
    def __init__(self):
        self.__token_list: list = []
        self.__line: int = 1
        self.__error_index: int = -1
        self.__no_error_index: int = -1
        self.__skip: bool = False
        self.__compact_move_table: dict = {
            0: [
                [0, set(), [('\x30', '\x39')], 1],
                [2, {'\x3f'}, [('\x28', '\x2e'), ('\x30', '\x39'), ('\x5b', '\x5e'), ('\x7b', '\x7d')], 2],
                [0, {'\x7c'}, [], 3],
                [0, {'\x2e'}, [], 4],
                [0, {'\x5b'}, [], 5],
                [0, {'\x5e'}, [], 6],
                [0, {'\x5c'}, [], 7],
                [0, {'\x5d'}, [], 8],
                [0, {'\x28'}, [], 9],
                [0, {'\x29'}, [], 10],
                [0, {'\x7b'}, [], 11],
                [0, {'\x2d'}, [], 12],
                [0, {'\x2b'}, [], 13],
                [0, {'\x2a'}, [], 14],
                [0, {'\x3f'}, [], 15],
                [0, {'\x2c'}, [], 16],
                [0, {'\x7d'}, [], 17]
            ],
            11: [
                [0, {'\x5f'}, [('\x41', '\x5a'), ('\x61', '\x7a')], 18]
            ],
            18: [
                [0, {'\x5f'}, [('\x30', '\x39'), ('\x41', '\x5a'), ('\x61', '\x7a')], 18],
                [0, {'\x7d'}, [], 19]
            ],
            7: [
                [2, set(), [], 20]
            ]
        }
        self.__character_set: set = {'\x51', '\x33', '\x48', '\x73', '\x7d', '\x68', '\x30', '\x6f', '\x4f', '\x44', '\x3f', '\x39', '\x58', '\x6e', '\x6b', '\x5c', '\x74', '\x5e', '\x29', '\x36', '\x69', '\x49', '\x71', '\x6d', '\x70', '\x4b', '\x28', '\x4e', '\x45', '\x6c', '\x4d', '\x54', '\x56', '\x5d', '\x41', '\x38', '\x62', '\x66', '\x72', '\x5a', '\x2e', '\x64', '\x61', '\x52', '\x42', '\x7a', '\x43', '\x63', '\x6a', '\x79', '\x32', '\x59', '\x2b', '\x35', '\x77', '\x78', '\x7c', '\x34', '\x57', '\x67', '\x4a', '\x37', '\x7b', '\x55', '\x2a', '\x46', '\x53', '\x31', '\x75', '\x65', '\x47', '\x50', '\x2c', '\x5b', '\x5f', '\x76', '\x4c', '\x2d'}
        self.__start_state: int = 0
        self.__end_state_set: set = {1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20}
        self.__lexical_symbol_mapping: dict = {
            1: 'single_number',
            2: 'normal_character',
            3: '!symbol_1',
            4: '!symbol_2',
            5: '!symbol_3',
            6: '!symbol_4',
            8: '!symbol_5',
            9: '!symbol_6',
            10: '!symbol_7',
            11: '!symbol_12',
            12: '!symbol_8',
            13: '!symbol_9',
            14: '!symbol_10',
            15: '!symbol_11',
            16: '!symbol_13',
            17: '!symbol_14',
            19: 'reference',
            20: 'escape_character'
        }
        self.__non_greedy_state_set: set = set()
        self.__symbol_function_mapping: dict = {
            'single_number': [],
            'escape_character': [],
            'reference': ['reference'],
            'normal_character': []
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
            self.__token_list.append(RegularToken(token_string, self.__line, symbol))

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
        self.__token_list.append(RegularToken('', self.__line, '$'))
        return self.__error_index

    def register_function(self, function_name: str) -> callable:
        def decorator(f: callable):
            self.__lexical_function[function_name] = f
            return f
        return decorator
