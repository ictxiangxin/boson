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
                [0, {'\x20', '\x09'}, [], 4],
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
                [0, {'\x20', '\x09'}, [], 4]
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
                [2, {'\x3e', '\x5c'}, [], 26],
                [0, {'\x5c'}, [], 27],
                [0, {'\x3e'}, [], 28]
            ],
            28: [
                [2, {'\x3e', '\x5c'}, [], 26],
                [0, {'\x5c'}, [], 27],
                [0, {'\x3e'}, [], 28]
            ],
            30: [
                [2, {'\x5c'}, [], 29],
                [0, {'\x5c'}, [], 30]
            ],
            29: [
                [2, {'\x27', '\x5c'}, [], 29],
                [0, {'\x27'}, [], 31],
                [0, {'\x5c'}, [], 30]
            ],
            31: [
                [2, {'\x27', '\x5c'}, [], 29],
                [0, {'\x27'}, [], 31],
                [0, {'\x5c'}, [], 30]
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
        self.__character_set: set = {'\x48', '\x5f', '\x6d', '\x56', '\x2c', '\x36', '\x3b', '\x5a', '\x4a', '\x2b', '\x25', '\x61', '\x67', '\x77', '\x54', '\x52', '\x35', '\x3a', '\x57', '\x69', '\x4d', '\x55', '\x4c', '\x71', '\x47', '\x5d', '\x41', '\x76', '\x43', '\x53', '\x45', '\x21', '\x42', '\x38', '\x72', '\x4e', '\x0d', '\x64', '\x78', '\x44', '\x58', '\x51', '\x27', '\x66', '\x7b', '\x7d', '\x6f', '\x32', '\x30', '\x65', '\x49', '\x4f', '\x75', '\x0a', '\x31', '\x5b', '\x33', '\x34', '\x39', '\x24', '\x7e', '\x59', '\x37', '\x40', '\x22', '\x46', '\x6c', '\x28', '\x6e', '\x5c', '\x4b', '\x74', '\x63', '\x68', '\x7c', '\x50', '\x29', '\x7a', '\x3e', '\x3c', '\x23', '\x20', '\x3d', '\x62', '\x70', '\x73', '\x79', '\x09', '\x2a', '\x6b', '\x6a'}
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
            '!symbol_3': 0,
            '!symbol_9': 1,
            '!symbol_4': 2,
            '!symbol_5': 3,
            '!symbol_12': 4,
            '!symbol_1': 5,
            '!symbol_16': 6,
            'command': 7,
            '!symbol_15': 8,
            '!symbol_14': 9,
            '!symbol_10': 10,
            '!symbol_11': 11,
            '!symbol_6': 12,
            'node': 13,
            'string': 14,
            '!symbol_8': 15,
            '$': 16,
            '!symbol_7': 17,
            '!symbol_2': 18,
            'name': 19,
            'regular': 20,
            '!symbol_13': 21
        }
        self.__sparse_action_table: dict = {
            0: {7: 's8', 19: 's1'},
            1: {15: 's18', 18: 's17'},
            2: {16: 'a'},
            3: {7: 's8', 16: 'r42', 19: 's1'},
            4: {7: 'r67', 16: 'r67', 19: 'r67'},
            5: {7: 'r50', 16: 'r50', 19: 'r50'},
            6: {7: 'r55', 16: 'r55', 19: 'r55'},
            7: {7: 'r61', 16: 'r61', 19: 'r61'},
            8: {14: 's12', 19: 's13'},
            9: {5: 's14', 14: 's12', 19: 's13'},
            10: {5: 'r26', 14: 'r26', 19: 'r26'},
            11: {5: 'r3', 14: 'r3', 19: 'r3'},
            12: {5: 'r28', 14: 'r28', 19: 'r28'},
            13: {5: 'r43', 14: 'r43', 19: 'r43'},
            14: {7: 'r36', 16: 'r36', 19: 'r36'},
            15: {5: 'r62', 14: 'r62', 19: 'r62'},
            16: {7: 'r52', 16: 'r52', 19: 'r52'},
            17: {20: 's76'},
            18: {1: 'r11', 5: 'r11', 9: 's31', 10: 's24', 11: 's30', 14: 's21', 18: 'r11', 19: 's20'},
            19: {5: 's75'},
            20: {1: 'r8', 4: 'r8', 5: 'r8', 6: 'r8', 8: 'r8', 9: 'r8', 11: 'r8', 14: 'r8', 18: 'r8', 19: 'r8', 21: 'r8'},
            21: {1: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 8: 'r24', 9: 'r24', 11: 'r24', 14: 'r24', 18: 'r24', 19: 'r24', 21: 'r24'},
            22: {1: 'r13', 5: 'r13'},
            23: {1: 'r18', 5: 'r18', 18: 's51'},
            24: {1: 'r57', 5: 'r57', 18: 'r57'},
            25: {1: 'r65', 5: 'r65', 18: 'r65'},
            26: {1: 'r66', 4: 'r66', 5: 'r66', 8: 'r66', 9: 's31', 11: 's30', 14: 's21', 18: 'r66', 19: 's20'},
            27: {1: 'r22', 4: 'r22', 5: 'r22', 8: 'r22', 9: 'r22', 11: 'r22', 14: 'r22', 18: 'r22', 19: 'r22'},
            28: {1: 'r10', 4: 'r10', 5: 'r10', 6: 's46', 8: 'r10', 9: 'r10', 11: 'r10', 14: 'r10', 18: 'r10', 19: 'r10', 21: 's45'},
            29: {1: 'r45', 4: 'r45', 5: 'r45', 8: 'r45', 9: 'r45', 11: 'r45', 14: 'r45', 18: 'r45', 19: 'r45'},
            30: {9: 's31', 11: 's30', 14: 's21', 19: 's20'},
            31: {9: 's31', 11: 's30', 14: 's21', 19: 's20'},
            32: {8: 's39'},
            33: {1: 's36', 4: 'r27', 8: 'r27'},
            34: {1: 's36', 4: 'r32', 8: 'r32'},
            35: {1: 'r68', 4: 'r68', 8: 'r68'},
            36: {9: 's31', 11: 's30', 14: 's21', 19: 's20'},
            37: {1: 'r56', 4: 'r56', 8: 'r56'},
            38: {1: 'r37', 4: 'r37', 8: 'r37'},
            39: {1: 'r21', 4: 'r21', 5: 'r21', 8: 'r21', 9: 'r21', 11: 'r21', 14: 'r21', 18: 'r21', 19: 'r21'},
            40: {4: 's41'},
            41: {1: 'r10', 4: 'r10', 5: 'r10', 6: 's46', 8: 'r10', 9: 'r10', 11: 'r10', 14: 'r10', 18: 'r10', 19: 'r10', 21: 's45'},
            42: {1: 'r20', 4: 'r20', 5: 'r20', 8: 'r20', 9: 'r20', 11: 'r20', 14: 'r20', 18: 'r20', 19: 'r20'},
            43: {1: 'r33', 4: 'r33', 5: 'r33', 8: 'r33', 9: 'r33', 11: 'r33', 14: 'r33', 18: 'r33', 19: 'r33'},
            44: {1: 'r5', 4: 'r5', 5: 'r5', 8: 'r5', 9: 'r5', 11: 'r5', 14: 'r5', 18: 'r5', 19: 'r5'},
            45: {1: 'r14', 4: 'r14', 5: 'r14', 8: 'r14', 9: 'r14', 11: 'r14', 14: 'r14', 18: 'r14', 19: 'r14'},
            46: {1: 'r58', 4: 'r58', 5: 'r58', 8: 'r58', 9: 'r58', 11: 'r58', 14: 'r58', 18: 'r58', 19: 'r58'},
            47: {1: 'r31', 4: 'r31', 5: 'r31', 8: 'r31', 9: 'r31', 11: 'r31', 14: 'r31', 18: 'r31', 19: 'r31'},
            48: {1: 'r30', 4: 'r30', 5: 'r30', 8: 'r30', 9: 'r30', 11: 'r30', 14: 'r30', 18: 'r30', 19: 'r30'},
            49: {1: 'r44', 5: 'r44'},
            50: {1: 'r15', 5: 'r15'},
            51: {11: 'r19', 19: 's54'},
            52: {11: 's56'},
            53: {11: 'r23'},
            54: {11: 'r53'},
            55: {1: 'r38', 5: 'r38'},
            56: {13: 'r16', 21: 's60'},
            57: {4: 'r54', 17: 'r54'},
            58: {13: 's61'},
            59: {11: 'r35', 13: 'r35'},
            60: {11: 'r51', 13: 'r51'},
            61: {4: 'r49', 11: 'r16', 17: 'r49', 21: 's60'},
            62: {4: 'r39', 17: 'r39'},
            63: {4: 'r48', 17: 'r48'},
            64: {11: 's56'},
            65: {4: 'r12', 17: 'r12'},
            66: {4: 's69', 17: 's67'},
            67: {13: 'r16', 21: 's60'},
            68: {4: 'r40', 17: 'r40'},
            69: {1: 'r7', 4: 'r7', 5: 'r7', 17: 'r7'},
            70: {4: 'r4', 17: 'r4'},
            71: {1: 's73', 5: 'r60'},
            72: {1: 'r25', 5: 'r25'},
            73: {1: 'r11', 5: 'r11', 9: 's31', 10: 's24', 11: 's30', 14: 's21', 18: 'r11', 19: 's20'},
            74: {1: 'r17', 5: 'r17'},
            75: {7: 'r1', 16: 'r1', 19: 'r1'},
            76: {0: 's79', 2: 'r29', 5: 'r29'},
            77: {2: 's81', 5: 'r34'},
            78: {2: 'r6', 5: 'r6'},
            79: {2: 'r46', 5: 'r46'},
            80: {5: 'r59'},
            81: {3: 's84'},
            82: {5: 's83'},
            83: {7: 'r2', 16: 'r2', 19: 'r2'},
            84: {19: 's86'},
            85: {12: 's91'},
            86: {12: 'r63', 17: 'r63'},
            87: {12: 'r64', 17: 's89'},
            88: {12: 'r9', 17: 'r9'},
            89: {19: 's90'},
            90: {12: 'r47', 17: 'r47'},
            91: {5: 'r41'}
        }
        self.__sparse_goto_table: dict = {
            0: {14: 4, 17: 2, 21: 3, 33: 7, 40: 6, 42: 5},
            3: {14: 16, 33: 7, 40: 6, 42: 5},
            8: {10: 9, 11: 11, 30: 10},
            9: {11: 11, 30: 15},
            18: {2: 27, 5: 25, 18: 19, 31: 23, 35: 26, 38: 29, 39: 28, 41: 22},
            22: {25: 71},
            23: {13: 50, 29: 49},
            26: {2: 48, 38: 29, 39: 28},
            28: {9: 43, 15: 44, 34: 47},
            30: {2: 27, 5: 33, 26: 40, 35: 26, 38: 29, 39: 28},
            31: {2: 27, 5: 33, 26: 32, 35: 26, 38: 29, 39: 28},
            33: {22: 35, 37: 34},
            34: {22: 38},
            36: {2: 27, 5: 37, 35: 26, 38: 29, 39: 28},
            41: {9: 43, 15: 44, 34: 42},
            51: {12: 53, 27: 52},
            52: {7: 55},
            56: {0: 58, 16: 57, 32: 59},
            57: {23: 66},
            61: {0: 64, 8: 63, 32: 59, 43: 62},
            64: {7: 65},
            66: {24: 68},
            67: {0: 58, 16: 70, 32: 59},
            71: {3: 72},
            73: {2: 27, 5: 25, 31: 23, 35: 26, 38: 29, 39: 28, 41: 74},
            76: {28: 78, 36: 77},
            77: {4: 80, 6: 82},
            84: {1: 85},
            86: {19: 87},
            87: {44: 88}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            32: ('0', '*1'),
            56: ('1',),
            37: ('*0', '*1'),
            21: ('1',),
            20: ('1', '*3'),
            24: ('0',),
            31: ('0', '*1'),
            10: (),
            33: ('*0',),
            39: ('*0', '1', '*2'),
            12: ('*0', '1'),
            49: (),
            48: ('*0',),
            16: (),
            35: ('*0',),
            7: ('1', '*2'),
            4: ('1',),
            54: (),
            40: ('*0', '*1'),
            66: ('*0',),
            30: ('*0', '1'),
            65: ('*0',),
            44: ('0', '*1'),
            38: ('*1', '2'),
            18: (),
            15: ('*0',),
            19: (),
            23: ('*0',),
            60: ('0', '*1'),
            17: ('1',),
            13: (),
            25: ('*0', '*1'),
            1: ('0', '2'),
            64: ('0', '*1'),
            47: ('1',),
            63: (),
            9: ('*0', '*1'),
            2: ('0', '2', '*3', '4'),
            41: ('*2',),
            34: (),
            59: ('*0',),
            29: (),
            6: ('*0',),
            36: ('0', '*1'),
            62: ('*0', '1'),
            52: ('*0', '1'),
            68: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 4, 6, 1, 2, 1, 1, 4, 1, 2, 0, 0, 2, 0, 1, 1, 0, 2, 0, 0, 4, 3, 1, 1, 1, 2, 1, 1, 1, 0, 2, 2, 2, 1, 0, 1, 3, 2, 3, 3, 2, 4, 1, 1, 2, 1, 1, 2, 1, 0, 1, 1, 2, 1, 0, 1, 2, 1, 1, 1, 2, 1, 2, 0, 2, 1, 1, 1, 1]
        self.__reduce_non_terminal_index: list = [20, 33, 40, 30, 24, 9, 36, 7, 39, 19, 34, 31, 8, 25, 15, 29, 0, 3, 29, 27, 38, 38, 35, 27, 39, 25, 10, 26, 11, 36, 35, 2, 26, 34, 6, 0, 42, 37, 13, 16, 23, 4, 17, 11, 41, 2, 28, 44, 43, 43, 14, 32, 21, 12, 23, 14, 22, 31, 15, 6, 18, 14, 10, 19, 1, 31, 5, 21, 37]

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
                elif statement_index in {0, 3, 5, 8, 11, 14, 22, 26, 27, 28, 42, 43, 45, 46, 50, 51, 53, 55, 57, 58, 61, 67}:
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
            36: 'command',
            2: 'lexical_define',
            1: 'reduce',
            39: 'grammar_node',
            31: 'name_closure',
            24: 'literal',
            20: 'complex_closure',
            21: 'complex_optional',
            32: 'select'
        }
        self.__naive_reduce_number_set: set = {65, 8, 11, 43, 45, 14, 50, 55, 24, 57, 58, 27, 28, 61}
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
