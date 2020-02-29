class LexicalToken:
    text: str
    line: int
    symbol: str

    def __init__(self, text: str, line: int, symbol: str):
        self.text = text
        self.line = line
        self.symbol = symbol


class BosonLexer:
    def __init__(self):
        self.__token_list: list = []
        self.__line: int = 1
        self.__error_line: int = -1
        self.__no_error_line: int = -1
        self.__skip: bool = False
        self.__move_table: dict = {
            0: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 1],
                [0, {'"'}, [], 33],
                [0, {"'"}, [], 30],
                [0, {'<'}, [], 27],
                [0, {'#'}, [], 2],
                [0, {'%'}, [], 3],
                [0, {' ', '\t'}, [], 4],
                [0, {'\n'}, [], 5],
                [0, {';'}, [], 6],
                [0, {'='}, [], 7],
                [0, {'!'}, [], 8],
                [0, {'@'}, [], 9],
                [0, {'{'}, [], 10],
                [0, {'}'}, [], 11],
                [0, {','}, [], 12],
                [0, {':'}, [], 13],
                [0, {'|'}, [], 14],
                [0, {'~'}, [], 15],
                [0, {'('}, [], 16],
                [0, {')'}, [], 17],
                [0, {'*'}, [], 18],
                [0, {'['}, [], 19],
                [0, {']'}, [], 20],
                [0, {'+'}, [], 21],
                [0, {'$'}, [], 22]
            ],
            22: [
                [0, set(), [('0', '9')], 23]
            ],
            23: [
                [0, set(), [('0', '9')], 23]
            ],
            5: [
                [0, {'\r'}, [], 24]
            ],
            4: [
                [0, {' ', '\t'}, [], 4]
            ],
            3: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 25]
            ],
            25: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 25]
            ],
            2: [
                [2, {'\n', '\r'}, [], 2]
            ],
            27: [
                [2, {'\\'}, [], 26],
                [0, {'\\'}, [], 27]
            ],
            26: [
                [2, {'\\', '>'}, [], 26],
                [0, {'\\'}, [], 27],
                [0, {'>'}, [], 28]
            ],
            28: [
                [2, {'\\', '>'}, [], 26],
                [0, {'\\'}, [], 27],
                [0, {'>'}, [], 28]
            ],
            30: [
                [2, {'\\'}, [], 29],
                [0, {'\\'}, [], 30]
            ],
            29: [
                [2, {"'", '\\'}, [], 29],
                [0, {"'"}, [], 31],
                [0, {'\\'}, [], 30]
            ],
            31: [
                [2, {"'", '\\'}, [], 29],
                [0, {"'"}, [], 31],
                [0, {'\\'}, [], 30]
            ],
            33: [
                [2, {'\\'}, [], 32],
                [0, {'\\'}, [], 33]
            ],
            32: [
                [0, {'"'}, [], 34],
                [2, {'\\', '"'}, [], 32],
                [0, {'\\'}, [], 33]
            ],
            34: [
                [2, {'\\', '"'}, [], 32],
                [0, {'\\'}, [], 33],
                [0, {'"'}, [], 34]
            ],
            1: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 1]
            ]
        }
        self.__character_set: set = {'e', 'w', '\n', 'g', '5', 'm', 'x', '%', ']', "'", 'c', 'z', 'I', 'U', '_', 'b', 's', 'Z', '\t', '@', 'k', ':', 'B', 'C', 'r', '{', 'N', 'o', 'q', 'X', 'Y', 'y', 'M', '=', 'p', '7', '\r', 'A', '4', 'P', '9', '<', 'u', 'S', 'd', 'T', 'n', 'a', 'J', '*', ',', 'R', 'G', '}', '6', '1', ' ', '\\', '(', 'h', 'E', '~', 'i', '>', '+', ';', 'L', 'j', 't', '2', 'F', 'D', 'H', 'V', 'l', 'Q', 'W', ')', '3', '#', '!', 'K', 'O', 'f', '$', '"', '0', '[', '|', '8', 'v'}
        self.__start_state: int = 0
        self.__end_state_set: set = {1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 28, 31, 34}
        self.__lexical_symbol_mapping: dict = {
            1: 'name',
            2: 'comment',
            4: 'skip',
            5: 'newline',
            6: '!symbol_1',
            7: '!symbol_2',
            8: '!symbol_3',
            9: '!symbol_4',
            10: '!symbol_5',
            11: '!symbol_6',
            12: '!symbol_7',
            13: '!symbol_8',
            14: '!symbol_9',
            15: '!symbol_10',
            16: '!symbol_11',
            17: '!symbol_12',
            18: '!symbol_13',
            19: '!symbol_14',
            20: '!symbol_15',
            21: '!symbol_16',
            23: 'node',
            24: 'newline',
            25: 'command',
            28: 'regular',
            31: 'string',
            34: 'string'
        }
        self.__non_greedy_state_set: set = {34, 28, 31}
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
            if not get_token and state in self.__move_table:
                for attribute, character_set, range_list, next_state in self.__move_table[state]:
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
                    raise ValueError('Invalid state: state={}'.format(state))
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

    def register(self, function_name: str) -> callable:
        def decorator(f: callable):
            self.__lexical_function[function_name] = f
            return f
        return decorator


class BosonGrammarNode:
    def __init__(self):
        self.reduce_number = -1
        self.__data: list = []

    def __getitem__(self, item):
        return self.__data[item]

    def __iadd__(self, other):
        self.__data += other
        return self

    def append(self, item) -> None:
        self.__data.append(item)

    def insert(self, index, item) -> None:
        self.__data.insert(index, item)

    def data(self) -> list:
        return self.__data


class BosonGrammar:
    def __init__(self):
        self.__grammar_tree: (BosonGrammarNode, None) = None
        self.__error_index: int = -1
        self.__no_error_index: int = -1

    def get_grammar_tree(self) -> (BosonGrammarNode, None):
        return self.__grammar_tree

    def set_grammar_tree(self, grammar_tree: BosonGrammarNode) -> None:
        self.__grammar_tree = grammar_tree

    grammar_tree = property(get_grammar_tree, set_grammar_tree)

    def get_error_index(self) -> int:
        return self.__error_index

    def set_error_index(self, error_index: int) -> None:
        self.__error_index = error_index

    error_index = property(get_error_index, set_error_index)

    def no_error_index(self) -> int:
        return self.__no_error_index


class BosonParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            'name': 0,
            'regular': 1,
            '!symbol_7': 2,
            '!symbol_10': 3,
            'string': 4,
            '!symbol_16': 5,
            '!symbol_9': 6,
            '!symbol_14': 7,
            '!symbol_11': 8,
            '!symbol_3': 9,
            '!symbol_2': 10,
            '!symbol_12': 11,
            '!symbol_13': 12,
            'command': 13,
            'node': 14,
            '!symbol_4': 15,
            '$': 16,
            '!symbol_8': 17,
            '!symbol_5': 18,
            '!symbol_1': 19,
            '!symbol_15': 20,
            '!symbol_6': 21
        }
        self.__sparse_action_table: dict = {
            0: {0: 's1', 13: 's8'},
            1: {10: 's17', 17: 's18'},
            2: {16: 'a'},
            3: {0: 's1', 13: 's8', 16: 'r45'},
            4: {0: 'r71', 13: 'r71', 16: 'r71'},
            5: {0: 'r2', 13: 'r2', 16: 'r2'},
            6: {0: 'r51', 13: 'r51', 16: 'r51'},
            7: {0: 'r72', 13: 'r72', 16: 'r72'},
            8: {0: 's10', 4: 's11'},
            9: {0: 'r11', 4: 'r11', 19: 'r11'},
            10: {0: 'r28', 4: 'r28', 19: 'r28'},
            11: {0: 'r68', 4: 'r68', 19: 'r68'},
            12: {0: 's10', 4: 's11', 19: 's14'},
            13: {0: 'r20', 4: 'r20', 19: 'r20'},
            14: {0: 'r73', 13: 'r73', 16: 'r73'},
            15: {0: 'r65', 4: 'r65', 19: 'r65'},
            16: {0: 'r48', 13: 'r48', 16: 'r48'},
            17: {1: 's81'},
            18: {0: 's19', 3: 's28', 4: 's20', 6: 'r22', 7: 's25', 8: 's24', 10: 'r22', 19: 'r22'},
            19: {0: 'r7', 4: 'r7', 5: 'r7', 6: 'r7', 7: 'r7', 8: 'r7', 10: 'r7', 11: 'r7', 12: 'r7', 19: 'r7', 20: 'r7'},
            20: {0: 'r63', 4: 'r63', 5: 'r63', 6: 'r63', 7: 'r63', 8: 'r63', 10: 'r63', 11: 'r63', 12: 'r63', 19: 'r63', 20: 'r63'},
            21: {19: 's80'},
            22: {0: 'r8', 4: 'r8', 5: 's65', 6: 'r8', 7: 'r8', 8: 'r8', 10: 'r8', 11: 'r8', 12: 's66', 19: 'r8', 20: 'r8'},
            23: {0: 'r69', 4: 'r69', 6: 'r69', 7: 'r69', 8: 'r69', 10: 'r69', 11: 'r69', 19: 'r69', 20: 'r69'},
            24: {0: 's19', 4: 's20', 7: 's25', 8: 's24'},
            25: {0: 's19', 4: 's20', 7: 's25', 8: 's24'},
            26: {6: 'r60', 19: 'r60'},
            27: {6: 'r50', 10: 's33', 19: 'r50'},
            28: {6: 'r43', 10: 'r43', 19: 'r43'},
            29: {0: 's19', 4: 's20', 6: 'r75', 7: 's25', 8: 's24', 10: 'r75', 19: 'r75'},
            30: {0: 'r3', 4: 'r3', 6: 'r3', 7: 'r3', 8: 'r3', 10: 'r3', 19: 'r3'},
            31: {0: 'r52', 4: 'r52', 6: 'r52', 7: 'r52', 8: 'r52', 10: 'r52', 19: 'r52'},
            32: {6: 'r13', 19: 'r13'},
            33: {0: 's37', 8: 'r57'},
            34: {6: 'r9', 19: 'r9'},
            35: {8: 's39'},
            36: {8: 'r42'},
            37: {8: 'r17'},
            38: {6: 'r25', 19: 'r25'},
            39: {12: 's43', 14: 'r37'},
            40: {2: 'r10', 11: 'r10'},
            41: {14: 's44'},
            42: {14: 'r18'},
            43: {14: 'r64'},
            44: {2: 'r1', 8: 'r12', 11: 'r1', 12: 's48'},
            45: {2: 'r23', 11: 'r23'},
            46: {8: 's39'},
            47: {8: 'r27'},
            48: {8: 'r19'},
            49: {2: 'r61', 11: 'r61'},
            50: {2: 'r67', 11: 'r67'},
            51: {2: 's53', 11: 's52'},
            52: {2: 'r70', 6: 'r70', 11: 'r70', 19: 'r70'},
            53: {12: 's43', 14: 'r37'},
            54: {2: 'r38', 11: 'r38'},
            55: {2: 'r47', 11: 'r47'},
            56: {6: 's58', 19: 'r39'},
            57: {6: 'r31', 19: 'r31'},
            58: {0: 's19', 3: 's28', 4: 's20', 6: 'r22', 7: 's25', 8: 's24', 10: 'r22', 19: 'r22'},
            59: {6: 'r21', 19: 'r21'},
            60: {0: 's19', 4: 's20', 7: 's25', 8: 's24', 11: 'r5', 20: 'r5'},
            61: {0: 'r24', 4: 'r24', 6: 's72', 7: 'r24', 8: 'r24', 11: 'r24', 20: 'r24'},
            62: {20: 's63'},
            63: {0: 'r46', 4: 'r46', 6: 'r46', 7: 'r46', 8: 'r46', 10: 'r46', 11: 'r46', 19: 'r46', 20: 'r46'},
            64: {11: 's74'},
            65: {0: 'r26', 4: 'r26', 6: 'r26', 7: 'r26', 8: 'r26', 10: 'r26', 11: 'r26', 19: 'r26', 20: 'r26'},
            66: {0: 'r35', 4: 'r35', 6: 'r35', 7: 'r35', 8: 'r35', 10: 'r35', 11: 'r35', 19: 'r35', 20: 'r35'},
            67: {0: 'r62', 4: 'r62', 6: 'r62', 7: 'r62', 8: 'r62', 10: 'r62', 11: 'r62', 19: 'r62', 20: 'r62'},
            68: {0: 'r41', 4: 'r41', 6: 'r41', 7: 'r41', 8: 'r41', 10: 'r41', 11: 'r41', 19: 'r41', 20: 'r41'},
            69: {0: 'r32', 4: 'r32', 6: 'r32', 7: 'r32', 8: 'r32', 10: 'r32', 11: 'r32', 19: 'r32', 20: 'r32'},
            70: {6: 's72', 11: 'r58', 20: 'r58'},
            71: {6: 'r56', 11: 'r56', 20: 'r56'},
            72: {0: 's19', 4: 's20', 7: 's25', 8: 's24'},
            73: {6: 'r40', 11: 'r40', 20: 'r40'},
            74: {0: 'r30', 4: 'r30', 5: 's65', 6: 'r30', 7: 'r30', 8: 'r30', 10: 'r30', 11: 'r30', 12: 's66', 19: 'r30', 20: 'r30'},
            75: {0: 'r55', 4: 'r55', 6: 'r55', 7: 'r55', 8: 'r55', 10: 'r55', 11: 'r55', 19: 'r55', 20: 'r55'},
            76: {0: 'r33', 4: 'r33', 6: 'r33', 7: 'r33', 8: 'r33', 10: 'r33', 11: 'r33', 19: 'r33', 20: 'r33'},
            77: {0: 'r6', 4: 'r6', 6: 'r6', 7: 'r6', 8: 'r6', 10: 'r6', 11: 'r6', 19: 'r6', 20: 'r6'},
            78: {6: 'r14', 11: 'r14', 20: 'r14'},
            79: {0: 'r15', 4: 'r15', 7: 'r15', 8: 'r15', 11: 'r15', 20: 'r15'},
            80: {0: 'r59', 13: 'r59', 16: 'r59'},
            81: {9: 's84', 15: 'r53', 19: 'r53'},
            82: {15: 's85', 19: 'r16'},
            83: {15: 'r29', 19: 'r29'},
            84: {15: 'r34', 19: 'r34'},
            85: {18: 's89'},
            86: {19: 's88'},
            87: {19: 'r44'},
            88: {0: 'r49', 13: 'r49', 16: 'r49'},
            89: {0: 's91'},
            90: {21: 's96'},
            91: {2: 'r36', 21: 'r36'},
            92: {2: 's94', 21: 'r4'},
            93: {2: 'r54', 21: 'r54'},
            94: {0: 's95'},
            95: {2: 'r66', 21: 'r66'},
            96: {19: 'r74'}
        }
        self.__sparse_goto_table: dict = {
            0: {4: 3, 10: 5, 25: 2, 27: 7, 35: 6, 41: 4},
            3: {10: 5, 27: 7, 35: 6, 41: 16},
            8: {22: 9, 30: 12, 32: 13},
            12: {22: 9, 32: 15},
            18: {13: 26, 19: 22, 23: 29, 31: 23, 36: 27, 38: 21, 40: 30},
            22: {3: 69, 5: 67, 9: 68},
            24: {16: 60, 19: 22, 31: 23, 40: 61, 44: 64},
            25: {16: 60, 19: 22, 31: 23, 40: 61, 44: 62},
            26: {45: 56},
            27: {2: 32, 39: 34},
            29: {19: 22, 31: 23, 40: 31},
            33: {0: 35, 6: 36},
            35: {18: 38},
            39: {37: 41, 42: 42, 48: 40},
            40: {14: 51},
            44: {8: 46, 12: 47, 15: 45, 20: 49},
            46: {18: 50},
            51: {43: 54},
            53: {37: 41, 42: 42, 48: 55},
            56: {17: 57},
            58: {13: 59, 19: 22, 23: 29, 31: 23, 36: 27, 40: 30},
            60: {19: 22, 31: 23, 40: 79},
            61: {1: 70, 7: 71},
            70: {7: 78},
            72: {19: 22, 31: 23, 40: 73},
            74: {3: 76, 11: 75, 47: 77},
            81: {24: 83, 46: 82},
            82: {33: 87, 34: 86},
            89: {29: 90},
            91: {28: 92},
            92: {21: 93}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            58: ('0', '*1'),
            40: ('1',),
            5: ('*0',),
            14: ('*0', '*1'),
            15: ('*0', '1'),
            46: ('1',),
            6: ('1', '*3'),
            30: (),
            55: ('*0',),
            63: ('0',),
            62: ('0', '*1'),
            8: (),
            41: ('*0',),
            61: ('*0', '1', '*2'),
            67: ('*0', '1'),
            1: (),
            23: ('*0',),
            12: (),
            27: ('*0',),
            37: (),
            18: ('*0',),
            70: ('1', '*2'),
            47: ('1',),
            10: (),
            38: ('*0', '*1'),
            75: ('*0',),
            52: ('*0', '1'),
            9: ('0', '*1'),
            25: ('*1', '2'),
            50: (),
            13: ('*0',),
            57: (),
            42: ('*0',),
            39: ('0', '*1'),
            21: ('1',),
            60: (),
            31: ('*0', '*1'),
            59: ('0', '2'),
            4: ('0', '*1'),
            66: ('1',),
            36: (),
            54: ('*0', '*1'),
            49: ('0', '2', '*3', '4'),
            74: ('*2',),
            16: (),
            44: ('*0',),
            53: (),
            29: ('*0',),
            73: ('0', '*1'),
            65: ('*0', '1'),
            48: ('*0', '1'),
            56: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 0, 1, 1, 2, 1, 4, 1, 0, 2, 0, 1, 0, 1, 2, 2, 0, 1, 1, 1, 1, 2, 0, 1, 1, 3, 1, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0, 0, 2, 2, 2, 1, 1, 1, 1, 1, 3, 2, 2, 6, 0, 1, 2, 0, 2, 1, 1, 0, 2, 4, 0, 3, 2, 1, 1, 2, 2, 2, 1, 1, 4, 1, 1, 3, 4, 1]
        self.__reduce_non_terminal_index: list = [26, 20, 41, 23, 29, 44, 31, 19, 5, 13, 14, 32, 8, 39, 1, 16, 34, 6, 37, 12, 30, 17, 36, 20, 16, 2, 3, 8, 22, 46, 47, 45, 9, 11, 24, 3, 28, 37, 14, 38, 7, 5, 0, 36, 34, 25, 31, 43, 4, 27, 39, 41, 23, 46, 28, 47, 1, 0, 44, 35, 45, 48, 40, 19, 42, 30, 21, 15, 22, 40, 18, 4, 41, 10, 33, 36]

    def parse(self, token_list: list) -> BosonGrammar:
        grammar = BosonGrammar()
        analysis_stack = [0]
        symbol_stack = []
        token_index = 0
        while token_index < len(token_list):
            token = token_list[token_index]
            current_state = analysis_stack[-1]
            operation = self.__sparse_action_table.get(current_state, {}).get(self.__terminal_index_mapping[token.symbol], 'e')
            operation_flag = operation[0]
            if operation_flag == 'e':
                grammar.error_index = token_index
                return grammar
            elif operation_flag == 's':
                state_number = int(operation[1:])
                analysis_stack.append(state_number)
                token_index += 1
                symbol_stack.append(token.text)
            elif operation_flag == 'r':
                statement_index = int(operation[1:])
                reduce_count = self.__reduce_symbol_count[statement_index]
                for _ in range(reduce_count):
                    analysis_stack.pop()
                current_state = analysis_stack[-1]
                current_non_terminal_index = self.__reduce_non_terminal_index[statement_index]
                goto_next_state = self.__sparse_goto_table.get(current_state, {}).get(current_non_terminal_index, -1)
                if goto_next_state == -1:
                    raise ValueError('Invalid goto action: state={}, non-terminal={}'.format(current_state, current_non_terminal_index))
                analysis_stack.append(goto_next_state)
                if statement_index in self.__sentence_index_grammar_tuple_mapping:
                    symbol_package = []
                    for _ in range(reduce_count):
                        symbol_package.insert(0, symbol_stack.pop())
                    grammar_node = BosonGrammarNode()
                    for node in self.__sentence_index_grammar_tuple_mapping[statement_index]:
                        if node[0] == '*':
                            grammar_node += symbol_package[int(node[1:])]
                        else:
                            grammar_node.append(symbol_package[int(node)])
                    grammar_node.reduce_number = statement_index
                    symbol_stack.append(grammar_node)
                elif statement_index in {0, 2, 3, 7, 11, 17, 19, 20, 22, 24, 26, 28, 32, 33, 34, 35, 43, 45, 51, 64, 68, 69, 71, 72}:
                    grammar_node = BosonGrammarNode()
                    for _ in range(reduce_count):
                        grammar_node.insert(0, symbol_stack.pop())
                    grammar_node.reduce_number = statement_index
                    symbol_stack.append(grammar_node)
                else:
                    raise ValueError('Invalid reduce number: reduce={}'.format(statement_index))
            elif operation_flag == 'a':
                grammar.grammar_tree = symbol_stack[0]
                return grammar
            else:
                raise ValueError('Invalid action: action={}'.format(operation))
        raise RuntimeError('Analyzer unusual exit.')


class BosonInterpreter:
    def __init__(self):
        self.__reduce_number_grammar_name_mapping: dict = {
            73: 'command',
            49: 'lexical_define',
            59: 'reduce',
            61: 'grammar_node',
            62: 'name_closure',
            63: 'literal',
            6: 'complex_closure',
            46: 'complex_optional',
            58: 'select'
        }
        self.__naive_reduce_number_set: set = {2, 35, 68, 69, 7, 72, 43, 51, 22, 26, 28, 63}
        self.__semantic_action_mapping: dict = {}

    def __semantic_analysis(self, grammar_tree: BosonGrammarNode):
        if grammar_tree.reduce_number in self.__reduce_number_grammar_name_mapping:
            grammar_name = self.__reduce_number_grammar_name_mapping[grammar_tree.reduce_number]
        else:
            grammar_name = '!grammar_hidden'
        semantic_node_list = []
        for grammar_node in grammar_tree.data():
            if isinstance(grammar_node, BosonGrammarNode):
                semantic_node = self.__semantic_analysis(grammar_node)
            else:
                semantic_node = grammar_node
            semantic_node_list.append(semantic_node)
        if grammar_name in self.__semantic_action_mapping:
            return self.__semantic_action_mapping[grammar_name](semantic_node_list)
        elif grammar_tree.reduce_number in self.__naive_reduce_number_set:
            if len(semantic_node_list) == 0:
                return None
            elif len(semantic_node_list) == 1:
                return semantic_node_list[0]
            else:
                return semantic_node_list
        else:
            return semantic_node_list

    def execute(self, grammar_tree: BosonGrammarNode):
        return self.__semantic_analysis(grammar_tree)

    def register_action(self, name: str) -> callable:
        def decorator(f: callable):
            self.__semantic_action_mapping[name] = f
            return f
        return decorator
