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
                [2, {'\x0a', '\x0d'}, [], 2]
            ],
            27: [
                [2, {'\x5c'}, [], 26],
                [0, {'\x5c'}, [], 27]
            ],
            26: [
                [2, {'\x3e', '\x5c'}, [], 26],
                [0, {'\x3e'}, [], 28],
                [0, {'\x5c'}, [], 27]
            ],
            28: [
                [2, {'\x3e', '\x5c'}, [], 26],
                [0, {'\x3e'}, [], 28],
                [0, {'\x5c'}, [], 27]
            ],
            30: [
                [2, {'\x5c'}, [], 29],
                [0, {'\x5c'}, [], 30]
            ],
            29: [
                [2, {'\x27', '\x5c'}, [], 29],
                [0, {'\x5c'}, [], 30],
                [0, {'\x27'}, [], 31]
            ],
            31: [
                [2, {'\x27', '\x5c'}, [], 29],
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
                [0, {'\x5c'}, [], 33],
                [0, {'\x22'}, [], 34]
            ],
            1: [
                [0, {'\x5f'}, [('\x30', '\x39'), ('\x41', '\x5a'), ('\x61', '\x7a')], 1]
            ]
        }
        self.__character_set: set = {'\x50', '\x20', '\x7b', '\x47', '\x6f', '\x77', '\x69', '\x56', '\x76', '\x3e', '\x33', '\x43', '\x64', '\x53', '\x58', '\x63', '\x7e', '\x51', '\x5c', '\x6a', '\x3b', '\x4c', '\x78', '\x65', '\x48', '\x28', '\x2c', '\x71', '\x61', '\x45', '\x30', '\x79', '\x44', '\x75', '\x24', '\x74', '\x68', '\x42', '\x2a', '\x52', '\x31', '\x5a', '\x40', '\x73', '\x67', '\x7a', '\x4e', '\x57', '\x39', '\x6e', '\x37', '\x27', '\x55', '\x59', '\x6c', '\x5f', '\x7c', '\x6b', '\x0d', '\x41', '\x0a', '\x4a', '\x49', '\x34', '\x70', '\x25', '\x36', '\x09', '\x29', '\x5b', '\x46', '\x3a', '\x7d', '\x21', '\x2b', '\x3d', '\x32', '\x4b', '\x4f', '\x35', '\x4d', '\x23', '\x38', '\x66', '\x22', '\x72', '\x3c', '\x5d', '\x62', '\x6d', '\x54'}
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
            '!symbol_14': 0,
            '!symbol_10': 1,
            '!symbol_6': 2,
            '!symbol_5': 3,
            '!symbol_4': 4,
            '!symbol_15': 5,
            '!symbol_3': 6,
            '!symbol_8': 7,
            '!symbol_12': 8,
            '$': 9,
            '!symbol_16': 10,
            '!symbol_7': 11,
            'name': 12,
            '!symbol_13': 13,
            'command': 14,
            '!symbol_9': 15,
            '!symbol_2': 16,
            '!symbol_1': 17,
            'node': 18,
            'regular': 19,
            '!symbol_11': 20,
            'string': 21
        }
        self.__sparse_action_table: dict = {
            0: {12: 's3', 14: 's5'},
            1: {9: 'a'},
            2: {9: 'r61', 12: 's3', 14: 's5'},
            3: {7: 's16', 16: 's17'},
            4: {9: 'r3', 12: 'r3', 14: 'r3'},
            5: {12: 's13', 21: 's12'},
            6: {9: 'r11', 12: 'r11', 14: 'r11'},
            7: {9: 'r38', 12: 'r38', 14: 'r38'},
            8: {9: 'r69', 12: 'r69', 14: 'r69'},
            9: {12: 's13', 17: 's14', 21: 's12'},
            10: {12: 'r30', 17: 'r30', 21: 'r30'},
            11: {12: 'r10', 17: 'r10', 21: 'r10'},
            12: {12: 'r24', 17: 'r24', 21: 'r24'},
            13: {12: 'r48', 17: 'r48', 21: 'r48'},
            14: {9: 'r63', 12: 'r63', 14: 'r63'},
            15: {12: 'r62', 17: 'r62', 21: 'r62'},
            16: {0: 's35', 1: 's45', 12: 's40', 15: 'r41', 16: 'r41', 17: 'r41', 20: 's36', 21: 's39'},
            17: {19: 's18'},
            18: {4: 'r12', 6: 's21', 17: 'r12'},
            19: {4: 's23', 17: 'r66'},
            20: {4: 'r28', 17: 'r28'},
            21: {4: 'r19', 17: 'r19'},
            22: {17: 'r65'},
            23: {3: 's26'},
            24: {17: 's25'},
            25: {9: 'r22', 12: 'r22', 14: 'r22'},
            26: {12: 's28'},
            27: {2: 's33'},
            28: {2: 'r67', 11: 'r67'},
            29: {2: 'r58', 11: 's31'},
            30: {2: 'r13', 11: 'r13'},
            31: {12: 's32'},
            32: {2: 'r34', 11: 'r34'},
            33: {17: 'r29'},
            34: {0: 's35', 5: 'r47', 8: 'r47', 12: 's40', 15: 'r47', 16: 'r47', 17: 'r47', 20: 's36', 21: 's39'},
            35: {0: 's35', 12: 's40', 20: 's36', 21: 's39'},
            36: {0: 's35', 12: 's40', 20: 's36', 21: 's39'},
            37: {0: 'r5', 5: 'r5', 8: 'r5', 12: 'r5', 15: 'r5', 16: 'r5', 17: 'r5', 20: 'r5', 21: 'r5'},
            38: {0: 'r51', 5: 'r51', 8: 'r51', 10: 's84', 12: 'r51', 13: 's83', 15: 'r51', 16: 'r51', 17: 'r51', 20: 'r51', 21: 'r51'},
            39: {0: 'r1', 5: 'r1', 8: 'r1', 10: 'r1', 12: 'r1', 13: 'r1', 15: 'r1', 16: 'r1', 17: 'r1', 20: 'r1', 21: 'r1'},
            40: {0: 'r6', 5: 'r6', 8: 'r6', 10: 'r6', 12: 'r6', 13: 'r6', 15: 'r6', 16: 'r6', 17: 'r6', 20: 'r6', 21: 'r6'},
            41: {17: 's94'},
            42: {15: 'r4', 17: 'r4'},
            43: {15: 'r50', 16: 's49', 17: 'r50'},
            44: {15: 'r23', 16: 'r23', 17: 'r23'},
            45: {15: 'r74', 16: 'r74', 17: 'r74'},
            46: {0: 'r27', 5: 'r27', 8: 'r27', 12: 'r27', 15: 'r27', 16: 'r27', 17: 'r27', 20: 'r27', 21: 'r27'},
            47: {15: 'r31', 17: 'r31'},
            48: {15: 'r46', 17: 'r46'},
            49: {12: 's50', 20: 'r35'},
            50: {20: 'r53'},
            51: {20: 's54'},
            52: {20: 'r2'},
            53: {15: 'r36', 17: 'r36'},
            54: {13: 's58', 18: 'r33'},
            55: {8: 'r60', 11: 'r60'},
            56: {18: 's59'},
            57: {18: 'r54'},
            58: {18: 'r42'},
            59: {8: 'r15', 11: 'r15', 13: 's60', 20: 'r59'},
            60: {20: 'r52'},
            61: {8: 'r20', 11: 'r20'},
            62: {8: 'r8', 11: 'r8'},
            63: {20: 's54'},
            64: {20: 'r49'},
            65: {8: 'r72', 11: 'r72'},
            66: {8: 's68', 11: 's67'},
            67: {13: 's58', 18: 'r33'},
            68: {8: 'r21', 11: 'r21', 15: 'r21', 17: 'r21'},
            69: {8: 'r73', 11: 'r73'},
            70: {8: 'r56', 11: 'r56'},
            71: {15: 's73', 17: 'r18'},
            72: {15: 'r32', 17: 'r32'},
            73: {0: 's35', 1: 's45', 12: 's40', 15: 'r41', 16: 'r41', 17: 'r41', 20: 's36', 21: 's39'},
            74: {15: 'r40', 17: 'r40'},
            75: {8: 's82'},
            76: {5: 'r9', 8: 'r9', 15: 's79'},
            77: {5: 'r14', 8: 'r14', 15: 'r14'},
            78: {5: 'r70', 8: 'r70', 15: 's79'},
            79: {0: 's35', 12: 's40', 20: 's36', 21: 's39'},
            80: {5: 'r39', 8: 'r39', 15: 'r39'},
            81: {5: 'r55', 8: 'r55', 15: 'r55'},
            82: {0: 'r26', 5: 'r26', 8: 'r26', 10: 's84', 12: 'r26', 13: 's83', 15: 'r26', 16: 'r26', 17: 'r26', 20: 'r26', 21: 'r26'},
            83: {0: 'r25', 5: 'r25', 8: 'r25', 12: 'r25', 15: 'r25', 16: 'r25', 17: 'r25', 20: 'r25', 21: 'r25'},
            84: {0: 'r45', 5: 'r45', 8: 'r45', 12: 'r45', 15: 'r45', 16: 'r45', 17: 'r45', 20: 'r45', 21: 'r45'},
            85: {0: 'r57', 5: 'r57', 8: 'r57', 12: 'r57', 15: 'r57', 16: 'r57', 17: 'r57', 20: 'r57', 21: 'r57'},
            86: {0: 'r68', 5: 'r68', 8: 'r68', 12: 'r68', 15: 'r68', 16: 'r68', 17: 'r68', 20: 'r68', 21: 'r68'},
            87: {0: 'r16', 5: 'r16', 8: 'r16', 12: 'r16', 15: 'r16', 16: 'r16', 17: 'r16', 20: 'r16', 21: 'r16'},
            88: {5: 's89'},
            89: {0: 'r37', 5: 'r37', 8: 'r37', 12: 'r37', 15: 'r37', 16: 'r37', 17: 'r37', 20: 'r37', 21: 'r37'},
            90: {0: 'r17', 5: 'r17', 8: 'r17', 12: 'r17', 15: 'r17', 16: 'r17', 17: 'r17', 20: 'r17', 21: 'r17'},
            91: {0: 'r43', 5: 'r43', 8: 'r43', 12: 'r43', 15: 'r43', 16: 'r43', 17: 'r43', 20: 'r43', 21: 'r43'},
            92: {0: 'r7', 5: 'r7', 8: 'r7', 12: 'r7', 15: 'r7', 16: 'r7', 17: 'r7', 20: 'r7', 21: 'r7'},
            93: {0: 'r71', 5: 'r71', 8: 'r71', 12: 'r71', 15: 'r71', 16: 'r71', 17: 'r71', 20: 'r71', 21: 'r71'},
            94: {9: 'r44', 12: 'r44', 14: 'r44'},
            95: {9: 'r64', 12: 'r64', 14: 'r64'}
        }
        self.__sparse_goto_table: dict = {
            0: {6: 1, 30: 7, 31: 4, 36: 8, 45: 2, 48: 6},
            2: {30: 7, 31: 95, 36: 8, 48: 6},
            5: {0: 11, 18: 10, 33: 9},
            9: {0: 11, 18: 15},
            16: {4: 41, 5: 43, 32: 42, 40: 46, 42: 38, 43: 34, 44: 37, 46: 44},
            18: {2: 20, 22: 19},
            19: {25: 22, 28: 24},
            26: {27: 27},
            28: {12: 29},
            29: {11: 30},
            34: {40: 93, 42: 38, 44: 37},
            35: {16: 88, 40: 46, 42: 38, 43: 34, 44: 37, 46: 76},
            36: {16: 75, 40: 46, 42: 38, 43: 34, 44: 37, 46: 76},
            38: {1: 92, 15: 90, 24: 91},
            42: {39: 71},
            43: {17: 48, 21: 47},
            49: {26: 52, 29: 51},
            51: {38: 53},
            54: {3: 56, 19: 55, 37: 57},
            55: {9: 66},
            59: {14: 63, 23: 61, 35: 64, 47: 62},
            63: {38: 65},
            66: {10: 69},
            67: {3: 56, 19: 70, 37: 57},
            71: {13: 72},
            73: {5: 43, 32: 74, 40: 46, 42: 38, 43: 34, 44: 37, 46: 44},
            76: {20: 77, 34: 78},
            78: {20: 81},
            79: {40: 46, 42: 38, 43: 34, 44: 37, 46: 80},
            82: {7: 85, 15: 87, 41: 86}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            70: ('0', '*1'),
            39: ('1',),
            55: ('*0', '*1'),
            37: ('1',),
            57: ('1', '*3'),
            26: (),
            68: ('*0',),
            1: ('0',),
            43: ('0', '*1'),
            51: (),
            7: ('*0',),
            20: ('*0', '1', '*2'),
            72: ('*0', '1'),
            15: (),
            8: ('*0',),
            59: (),
            49: ('*0',),
            33: (),
            54: ('*0',),
            21: ('1', '*2'),
            56: ('1',),
            60: (),
            73: ('*0', '*1'),
            47: ('*0',),
            71: ('*0', '1'),
            23: ('*0',),
            31: ('0', '*1'),
            36: ('*1', '2'),
            50: (),
            46: ('*0',),
            35: (),
            2: ('*0',),
            18: ('0', '*1'),
            40: ('1',),
            4: (),
            32: ('*0', '*1'),
            44: ('0', '2'),
            58: ('0', '*1'),
            34: ('1',),
            67: (),
            13: ('*0', '*1'),
            22: ('0', '2', '*3', '4'),
            29: ('*2',),
            66: (),
            65: ('*0',),
            12: (),
            28: ('*0',),
            63: ('0', '*1'),
            62: ('*0', '1'),
            64: ('*0', '1'),
            14: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 2, 1, 0, 1, 1, 2, 1, 3, 4, 6, 1, 1, 1, 0, 1, 1, 4, 1, 2, 2, 0, 2, 0, 3, 3, 1, 2, 2, 0, 1, 2, 4, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 2, 2, 4, 2, 0, 0, 1, 2, 3, 2, 1, 0, 0, 1, 1, 2, 2, 2, 2, 1]
        self.__reduce_non_terminal_index: list = [8, 42, 29, 45, 39, 40, 42, 24, 23, 16, 18, 31, 22, 12, 34, 23, 41, 1, 4, 2, 19, 38, 36, 5, 0, 15, 7, 43, 22, 25, 33, 32, 39, 3, 11, 29, 17, 44, 31, 20, 13, 5, 37, 40, 48, 15, 21, 46, 0, 14, 21, 24, 35, 26, 3, 34, 10, 44, 27, 14, 9, 6, 33, 30, 45, 28, 28, 12, 7, 31, 16, 43, 47, 9, 5]

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
                elif statement_index in {0, 3, 5, 6, 9, 10, 11, 16, 17, 19, 24, 25, 27, 30, 38, 41, 42, 45, 48, 52, 53, 61, 69, 74}:
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
            63: 'command',
            22: 'lexical_define',
            44: 'reduce',
            20: 'grammar_node',
            43: 'name_closure',
            1: 'literal',
            57: 'complex_closure',
            37: 'complex_optional',
            70: 'select'
        }
        self.__naive_reduce_number_set: set = {1, 5, 38, 69, 6, 41, 9, 11, 74, 45, 48, 23, 24, 25}
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
