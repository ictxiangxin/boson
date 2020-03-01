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
        self.__compact_move_table: dict = {
            0: [
                [0, {'\x5f'}, [('\x41', '\x5a'), ('\x61', '\x7a')], 1],
                [0, {'\x22'}, [], 33],
                [0, {'\x27'}, [], 30],
                [0, {'\x3c'}, [], 27],
                [0, {'\x23'}, [], 2],
                [0, {'\x25'}, [], 3],
                [0, {'\x09', '\x20'}, [], 4],
                [0, {'\x0a'}, [], 5],
                [0, {'\x3b'}, [], 6],
                [0, {'\x3d'}, [], 7],
                [0, {'\x21'}, [], 8],
                [0, {'\x40'}, [], 9],
                [0, {'\x7b'}, [], 10],
                [0, {'\x7d'}, [], 11],
                [0, {'\x2c'}, [], 12],
                [0, {'\x3a'}, [], 13],
                [0, {'\x7c'}, [], 14],
                [0, {'\x7e'}, [], 15],
                [0, {'\x28'}, [], 16],
                [0, {'\x29'}, [], 17],
                [0, {'\x2a'}, [], 18],
                [0, {'\x5b'}, [], 19],
                [0, {'\x5d'}, [], 20],
                [0, {'\x2b'}, [], 21],
                [0, {'\x24'}, [], 22]
            ],
            22: [
                [0, set(), [('\x30', '\x39')], 23]
            ],
            23: [
                [0, set(), [('\x30', '\x39')], 23]
            ],
            5: [
                [0, {'\x0d'}, [], 24]
            ],
            4: [
                [0, {'\x09', '\x20'}, [], 4]
            ],
            3: [
                [0, {'\x5f'}, [('\x41', '\x5a'), ('\x61', '\x7a')], 25]
            ],
            25: [
                [0, {'\x5f'}, [('\x41', '\x5a'), ('\x61', '\x7a')], 25]
            ],
            2: [
                [2, {'\x0d', '\x0a'}, [], 2]
            ],
            27: [
                [2, {'\x5c'}, [], 26],
                [0, {'\x5c'}, [], 27]
            ],
            26: [
                [2, {'\x5c', '\x3e'}, [], 26],
                [0, {'\x5c'}, [], 27],
                [0, {'\x3e'}, [], 28]
            ],
            28: [
                [2, {'\x5c', '\x3e'}, [], 26],
                [0, {'\x5c'}, [], 27],
                [0, {'\x3e'}, [], 28]
            ],
            30: [
                [2, {'\x5c'}, [], 29],
                [0, {'\x5c'}, [], 30]
            ],
            29: [
                [2, {'\x5c', '\x27'}, [], 29],
                [0, {'\x5c'}, [], 30],
                [0, {'\x27'}, [], 31]
            ],
            31: [
                [2, {'\x5c', '\x27'}, [], 29],
                [0, {'\x5c'}, [], 30],
                [0, {'\x27'}, [], 31]
            ],
            33: [
                [2, {'\x5c'}, [], 32],
                [0, {'\x5c'}, [], 33]
            ],
            32: [
                [0, {'\x22'}, [], 34],
                [2, {'\x5c', '\x22'}, [], 32],
                [0, {'\x5c'}, [], 33]
            ],
            34: [
                [2, {'\x5c', '\x22'}, [], 32],
                [0, {'\x22'}, [], 34],
                [0, {'\x5c'}, [], 33]
            ],
            1: [
                [0, {'\x5f'}, [('\x30', '\x39'), ('\x41', '\x5a'), ('\x61', '\x7a')], 1]
            ]
        }
        self.__character_set: set = {'\x24', '\x4f', '\x62', '\x78', '\x45', '\x3d', '\x63', '\x73', '\x38', '\x5f', '\x22', '\x6a', '\x42', '\x75', '\x29', '\x4b', '\x40', '\x52', '\x58', '\x7e', '\x2a', '\x70', '\x7c', '\x4a', '\x46', '\x66', '\x41', '\x28', '\x48', '\x5c', '\x49', '\x31', '\x6d', '\x27', '\x20', '\x53', '\x0d', '\x5d', '\x56', '\x76', '\x4c', '\x2b', '\x36', '\x61', '\x74', '\x65', '\x59', '\x67', '\x69', '\x33', '\x3b', '\x21', '\x35', '\x39', '\x09', '\x43', '\x5b', '\x23', '\x5a', '\x57', '\x32', '\x71', '\x4d', '\x3e', '\x34', '\x68', '\x37', '\x6e', '\x3c', '\x6b', '\x79', '\x3a', '\x2c', '\x30', '\x54', '\x77', '\x64', '\x4e', '\x7d', '\x25', '\x6f', '\x51', '\x44', '\x50', '\x47', '\x6c', '\x0a', '\x7b', '\x55', '\x72', '\x7a'}
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
            '$': 0,
            '!symbol_1': 1,
            '!symbol_13': 2,
            'regular': 3,
            '!symbol_12': 4,
            '!symbol_6': 5,
            '!symbol_7': 6,
            'string': 7,
            '!symbol_10': 8,
            '!symbol_2': 9,
            '!symbol_16': 10,
            '!symbol_11': 11,
            '!symbol_5': 12,
            '!symbol_14': 13,
            '!symbol_9': 14,
            '!symbol_4': 15,
            'name': 16,
            '!symbol_3': 17,
            'node': 18,
            '!symbol_8': 19,
            'command': 20,
            '!symbol_15': 21
        }
        self.__sparse_action_table: dict = {
            0: {16: 's8', 20: 's1'},
            1: {7: 's93', 16: 's94'},
            2: {0: 'a'},
            3: {0: 'r68', 16: 's8', 20: 's1'},
            4: {0: 'r63', 16: 'r63', 20: 'r63'},
            5: {0: 'r24', 16: 'r24', 20: 'r24'},
            6: {0: 'r43', 16: 'r43', 20: 'r43'},
            7: {0: 'r46', 16: 'r46', 20: 'r46'},
            8: {9: 's9', 19: 's10'},
            9: {3: 's73'},
            10: {1: 'r2', 7: 's13', 8: 's20', 9: 'r2', 11: 's17', 13: 's11', 14: 'r2', 16: 's14'},
            11: {7: 's13', 11: 's17', 13: 's11', 16: 's14'},
            12: {1: 's72'},
            13: {1: 'r9', 2: 'r9', 4: 'r9', 7: 'r9', 9: 'r9', 10: 'r9', 11: 'r9', 13: 'r9', 14: 'r9', 16: 'r9', 21: 'r9'},
            14: {1: 'r49', 2: 'r49', 4: 'r49', 7: 'r49', 9: 'r49', 10: 'r49', 11: 'r49', 13: 'r49', 14: 'r49', 16: 'r49', 21: 'r49'},
            15: {1: 'r13', 2: 's58', 4: 'r13', 7: 'r13', 9: 'r13', 10: 's57', 11: 'r13', 13: 'r13', 14: 'r13', 16: 'r13', 21: 'r13'},
            16: {1: 'r51', 4: 'r51', 7: 'r51', 9: 'r51', 11: 'r51', 13: 'r51', 14: 'r51', 16: 'r51', 21: 'r51'},
            17: {7: 's13', 11: 's17', 13: 's11', 16: 's14'},
            18: {1: 'r39', 14: 'r39'},
            19: {1: 'r20', 9: 's25', 14: 'r20'},
            20: {1: 'r36', 9: 'r36', 14: 'r36'},
            21: {1: 'r61', 7: 's13', 9: 'r61', 11: 's17', 13: 's11', 14: 'r61', 16: 's14'},
            22: {1: 'r22', 7: 'r22', 9: 'r22', 11: 'r22', 13: 'r22', 14: 'r22', 16: 'r22'},
            23: {1: 'r44', 7: 'r44', 9: 'r44', 11: 'r44', 13: 'r44', 14: 'r44', 16: 'r44'},
            24: {1: 'r41', 14: 'r41'},
            25: {11: 'r54', 16: 's27'},
            26: {1: 'r75', 14: 'r75'},
            27: {11: 'r31'},
            28: {11: 's31'},
            29: {11: 'r29'},
            30: {1: 'r34', 14: 'r34'},
            31: {2: 's35', 18: 'r60'},
            32: {4: 'r14', 6: 'r14'},
            33: {18: 's36'},
            34: {18: 'r21'},
            35: {18: 'r56'},
            36: {2: 's41', 4: 'r45', 6: 'r45', 11: 'r16'},
            37: {4: 'r55', 6: 'r55'},
            38: {4: 'r8', 6: 'r8'},
            39: {11: 's31'},
            40: {11: 'r57'},
            41: {11: 'r33'},
            42: {4: 'r69', 6: 'r69'},
            43: {4: 's45', 6: 's44'},
            44: {2: 's35', 18: 'r60'},
            45: {1: 'r50', 4: 'r50', 6: 'r50', 14: 'r50'},
            46: {4: 'r70', 6: 'r70'},
            47: {4: 'r12', 6: 'r12'},
            48: {1: 'r73', 14: 's50'},
            49: {1: 'r65', 14: 'r65'},
            50: {1: 'r2', 7: 's13', 8: 's20', 9: 'r2', 11: 's17', 13: 's11', 14: 'r2', 16: 's14'},
            51: {1: 'r37', 14: 'r37'},
            52: {4: 's55'},
            53: {4: 'r19', 7: 'r19', 11: 'r19', 13: 'r19', 14: 's69', 16: 'r19', 21: 'r19'},
            54: {4: 'r42', 7: 's13', 11: 's17', 13: 's11', 16: 's14', 21: 'r42'},
            55: {1: 'r32', 2: 's58', 4: 'r32', 7: 'r32', 9: 'r32', 10: 's57', 11: 'r32', 13: 'r32', 14: 'r32', 16: 'r32', 21: 'r32'},
            56: {1: 'r66', 4: 'r66', 7: 'r66', 9: 'r66', 11: 'r66', 13: 'r66', 14: 'r66', 16: 'r66', 21: 'r66'},
            57: {1: 'r52', 4: 'r52', 7: 'r52', 9: 'r52', 11: 'r52', 13: 'r52', 14: 'r52', 16: 'r52', 21: 'r52'},
            58: {1: 'r67', 4: 'r67', 7: 'r67', 9: 'r67', 11: 'r67', 13: 'r67', 14: 'r67', 16: 'r67', 21: 'r67'},
            59: {1: 'r47', 4: 'r47', 7: 'r47', 9: 'r47', 11: 'r47', 13: 'r47', 14: 'r47', 16: 'r47', 21: 'r47'},
            60: {1: 'r53', 4: 'r53', 7: 'r53', 9: 'r53', 11: 'r53', 13: 'r53', 14: 'r53', 16: 'r53', 21: 'r53'},
            61: {1: 'r38', 4: 'r38', 7: 'r38', 9: 'r38', 11: 'r38', 13: 'r38', 14: 'r38', 16: 'r38', 21: 'r38'},
            62: {1: 'r71', 4: 'r71', 7: 'r71', 9: 'r71', 11: 'r71', 13: 'r71', 14: 'r71', 16: 'r71', 21: 'r71'},
            63: {1: 'r23', 4: 'r23', 7: 'r23', 9: 'r23', 11: 'r23', 13: 'r23', 14: 'r23', 16: 'r23', 21: 'r23'},
            64: {4: 'r15', 7: 'r15', 11: 'r15', 13: 'r15', 16: 'r15', 21: 'r15'},
            65: {21: 's66'},
            66: {1: 'r58', 4: 'r58', 7: 'r58', 9: 'r58', 11: 'r58', 13: 'r58', 14: 'r58', 16: 'r58', 21: 'r58'},
            67: {4: 'r10', 14: 's69', 21: 'r10'},
            68: {4: 'r59', 14: 'r59', 21: 'r59'},
            69: {7: 's13', 11: 's17', 13: 's11', 16: 's14'},
            70: {4: 'r35', 14: 'r35', 21: 'r35'},
            71: {4: 'r3', 14: 'r3', 21: 'r3'},
            72: {0: 'r28', 16: 'r28', 20: 'r28'},
            73: {1: 'r5', 15: 'r5', 17: 's76'},
            74: {1: 'r1', 15: 's77'},
            75: {1: 'r62', 15: 'r62'},
            76: {1: 'r27', 15: 'r27'},
            77: {12: 's81'},
            78: {1: 's80'},
            79: {1: 'r7'},
            80: {0: 'r40', 16: 'r40', 20: 'r40'},
            81: {16: 's83'},
            82: {5: 's88'},
            83: {5: 'r74', 6: 'r74'},
            84: {5: 'r11', 6: 's86'},
            85: {5: 'r26', 6: 'r26'},
            86: {16: 's87'},
            87: {5: 'r72', 6: 'r72'},
            88: {1: 'r6'},
            89: {0: 'r4', 16: 'r4', 20: 'r4'},
            90: {1: 's95', 7: 's93', 16: 's94'},
            91: {1: 'r18', 7: 'r18', 16: 'r18'},
            92: {1: 'r48', 7: 'r48', 16: 'r48'},
            93: {1: 'r30', 7: 'r30', 16: 'r30'},
            94: {1: 'r64', 7: 'r64', 16: 'r64'},
            95: {0: 'r17', 16: 'r17', 20: 'r17'},
            96: {1: 'r25', 7: 'r25', 16: 'r25'}
        }
        self.__sparse_goto_table: dict = {
            0: {9: 2, 13: 5, 15: 7, 21: 3, 33: 6, 34: 4},
            1: {7: 92, 23: 91, 39: 90},
            3: {13: 5, 15: 7, 33: 6, 34: 89},
            10: {0: 15, 1: 22, 10: 19, 38: 16, 41: 18, 43: 21, 45: 12},
            11: {0: 15, 1: 53, 8: 65, 19: 54, 38: 16},
            15: {2: 63, 26: 61, 30: 62},
            17: {0: 15, 1: 53, 8: 52, 19: 54, 38: 16},
            18: {18: 48},
            19: {24: 26, 25: 24},
            21: {0: 15, 1: 23, 38: 16},
            25: {37: 29, 40: 28},
            28: {5: 30},
            31: {11: 32, 12: 34, 27: 33},
            32: {4: 43},
            36: {6: 38, 28: 39, 36: 40, 44: 37},
            39: {5: 42},
            43: {31: 46},
            44: {11: 47, 12: 34, 27: 33},
            48: {22: 49},
            50: {0: 15, 1: 22, 10: 19, 38: 16, 41: 51, 43: 21},
            53: {46: 68, 48: 67},
            54: {0: 15, 1: 64, 38: 16},
            55: {20: 60, 29: 59, 30: 56},
            67: {46: 71},
            69: {0: 15, 1: 70, 38: 16},
            73: {32: 74, 42: 75},
            74: {3: 78, 35: 79},
            81: {14: 82},
            83: {17: 84},
            84: {16: 85},
            90: {7: 92, 23: 96}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            10: ('0', '*1'),
            35: ('1',),
            42: ('*0',),
            3: ('*0', '*1'),
            15: ('*0', '1'),
            58: ('1',),
            47: ('1', '*3'),
            32: (),
            53: ('*0',),
            9: ('0',),
            23: ('0', '*1'),
            13: (),
            38: ('*0',),
            55: ('*0', '1', '*2'),
            69: ('*0', '1'),
            45: (),
            8: ('*0',),
            16: (),
            57: ('*0',),
            60: (),
            21: ('*0',),
            50: ('1', '*2'),
            12: ('1',),
            14: (),
            70: ('*0', '*1'),
            61: ('*0',),
            44: ('*0', '1'),
            75: ('0', '*1'),
            34: ('*1', '2'),
            20: (),
            41: ('*0',),
            54: (),
            29: ('*0',),
            73: ('0', '*1'),
            37: ('1',),
            39: (),
            65: ('*0', '*1'),
            28: ('0', '2'),
            11: ('0', '*1'),
            72: ('1',),
            74: (),
            26: ('*0', '*1'),
            40: ('0', '2', '*3', '4'),
            6: ('*2',),
            1: (),
            7: ('*0',),
            5: (),
            62: ('*0',),
            17: ('0', '*1'),
            25: ('*0', '1'),
            4: ('*0', '1'),
            59: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 0, 0, 2, 2, 0, 4, 1, 1, 1, 2, 2, 2, 0, 0, 2, 0, 3, 1, 1, 0, 1, 1, 2, 1, 2, 2, 1, 4, 1, 1, 1, 0, 1, 3, 2, 1, 2, 1, 0, 6, 1, 1, 1, 2, 0, 1, 4, 1, 1, 4, 1, 1, 1, 0, 3, 1, 1, 3, 1, 0, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 2, 2, 0, 2]
        self.__reduce_non_terminal_index: list = [47, 3, 10, 48, 21, 32, 35, 3, 44, 0, 8, 14, 31, 2, 4, 19, 28, 33, 39, 19, 24, 27, 43, 1, 34, 39, 17, 42, 13, 40, 7, 37, 29, 36, 25, 46, 10, 22, 2, 18, 15, 24, 8, 34, 43, 44, 34, 38, 23, 0, 5, 1, 30, 29, 40, 11, 12, 28, 38, 48, 27, 10, 32, 21, 7, 18, 20, 30, 9, 6, 4, 26, 16, 45, 17, 41]

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
                elif statement_index in {0, 2, 18, 19, 22, 24, 27, 30, 31, 33, 36, 43, 46, 48, 49, 51, 52, 56, 63, 64, 66, 67, 68, 71}:
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
            17: 'command',
            40: 'lexical_define',
            28: 'reduce',
            55: 'grammar_node',
            23: 'name_closure',
            9: 'literal',
            47: 'complex_closure',
            58: 'complex_optional',
            10: 'select'
        }
        self.__naive_reduce_number_set: set = {64, 2, 67, 36, 9, 43, 46, 49, 51, 52, 24, 30}
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
