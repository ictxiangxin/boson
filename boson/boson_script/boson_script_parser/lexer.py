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
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 34],
                [0, {'\n'}, [], 1],
                [0, {';'}, [], 2],
                [0, {'$'}, [], 3],
                [0, {'='}, [], 4],
                [0, {'!'}, [], 5],
                [0, {'@'}, [], 6],
                [0, {'{'}, [], 7],
                [0, {'"'}, [], 8],
                [0, {'}'}, [], 9],
                [0, {','}, [], 10],
                [0, {':'}, [], 11],
                [0, {'|'}, [], 12],
                [0, {'~'}, [], 13],
                [0, {'\''}, [], 29],
                [0, {'('}, [], 14],
                [0, {')'}, [], 15],
                [0, {'['}, [], 16],
                [0, {']'}, [], 17],
                [0, {'*'}, [], 18],
                [0, {'<'}, [], 19],
                [0, {'+'}, [], 20],
                [0, {'#'}, [], 25],
                [0, {'%'}, [], 21],
                [0, {' ', '\t'}, [], 22],
                [0, {'\r'}, [], 23]
            ],
            23: [
                [0, {'\n'}, [], 1]
            ],
            22: [
                [0, {' ', '\t'}, [], 22]
            ],
            21: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 24]
            ],
            24: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 24]
            ],
            25: [
                [2, {'\r', '\n'}, [], 25]
            ],
            19: [
                [2, {'\\'}, [], 26],
                [0, {'\\'}, [], 19]
            ],
            26: [
                [2, {'>', '\\'}, [], 26],
                [0, {'>'}, [], 27],
                [0, {'\\'}, [], 19]
            ],
            27: [
                [2, {'>', '\\'}, [], 26],
                [0, {'>'}, [], 27],
                [0, {'\\'}, [], 19]
            ],
            29: [
                [2, {'\\'}, [], 28],
                [0, {'\\'}, [], 29]
            ],
            28: [
                [2, {'\\', '\''}, [], 28],
                [0, {'\\'}, [], 29],
                [0, {'\''}, [], 30]
            ],
            30: [
                [2, {'\\', '\''}, [], 28],
                [0, {'\\'}, [], 29],
                [0, {'\''}, [], 30]
            ],
            8: [
                [2, {'\\'}, [], 31],
                [0, {'\\'}, [], 8]
            ],
            31: [
                [2, {'\\', '"'}, [], 31],
                [0, {'"'}, [], 32],
                [0, {'\\'}, [], 8]
            ],
            32: [
                [2, {'\\', '"'}, [], 31],
                [0, {'"'}, [], 32],
                [0, {'\\'}, [], 8]
            ],
            3: [
                [0, set(), [('0', '9')], 33]
            ],
            33: [
                [0, set(), [('0', '9')], 33]
            ],
            34: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 34]
            ]
        }
        self.__character_set: set = {'Y', 'J', 'M', 'j', 'T', 'a', '+', '(', 'F', 'A', 'R', '>', 'Q', 'Z', '[', '$', 'x', 'S', '\n', 'm', ']', '*', '\r', 'K', 'd', 'h', 'q', '2', 'N', 'B', '=', 'X', '\t', '@', '"', '6', 'i', 'w', '3', 'b', 'O', 'H', '~', '%', 'o', 'E', '7', ';', 't', 'W', 'v', ',', 'C', 'P', 's', 'D', 'V', ' ', '#', '|', 'f', 'n', '<', '8', '{', 'I', '5', 'r', '\\', 'c', 'G', 'g', 'u', ')', '_', '}', '\'', 'y', '!', '9', '1', 'z', 'e', 'L', 'k', 'p', 'U', '0', '4', ':', 'l'}
        self.__start_state: int = 0
        self.__end_state_set: set = {1, 2, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 25, 27, 30, 32, 33, 34}
        self.__lexical_symbol_mapping: dict = {
            1: 'newline',
            2: '!symbol_1',
            4: '!symbol_2',
            5: '!symbol_3',
            6: '!symbol_4',
            7: '!symbol_5',
            9: '!symbol_6',
            10: '!symbol_7',
            11: '!symbol_8',
            12: '!symbol_9',
            13: '!symbol_10',
            14: '!symbol_11',
            15: '!symbol_12',
            16: '!symbol_13',
            17: '!symbol_14',
            18: '!symbol_15',
            20: '!symbol_16',
            22: 'skip',
            24: 'command',
            25: 'comment',
            27: 'regular',
            30: 'string',
            32: 'string',
            33: 'node',
            34: 'name'
        }
        self.__non_greedy_state_set: set = {32, 27, 30}
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
