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
                [0, {'\x5c'}, [], 33],
                [0, {'\x22'}, [], 34]
            ],
            1: [
                [0, {'\x5f'}, [('\x30', '\x39'), ('\x41', '\x5a'), ('\x61', '\x7a')], 1]
            ]
        }
        self.__character_set: set = {'\x64', '\x6d', '\x54', '\x33', '\x38', '\x61', '\x21', '\x43', '\x62', '\x78', '\x47', '\x67', '\x20', '\x74', '\x49', '\x39', '\x3e', '\x34', '\x2c', '\x75', '\x32', '\x56', '\x2a', '\x4a', '\x3b', '\x6b', '\x6c', '\x50', '\x4f', '\x48', '\x44', '\x3a', '\x68', '\x66', '\x5c', '\x23', '\x77', '\x53', '\x70', '\x5b', '\x46', '\x25', '\x51', '\x57', '\x0d', '\x7b', '\x2b', '\x0a', '\x35', '\x3c', '\x5a', '\x4d', '\x7d', '\x37', '\x29', '\x76', '\x22', '\x31', '\x5d', '\x41', '\x63', '\x55', '\x27', '\x6e', '\x72', '\x6a', '\x09', '\x79', '\x30', '\x5f', '\x65', '\x69', '\x40', '\x59', '\x4b', '\x28', '\x73', '\x4c', '\x42', '\x7a', '\x6f', '\x45', '\x24', '\x36', '\x7e', '\x71', '\x58', '\x4e', '\x7c', '\x52', '\x3d'}
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
            '!symbol_7': 0,
            '!symbol_11': 1,
            'name': 2,
            '!symbol_9': 3,
            'command': 4,
            '!symbol_10': 5,
            'node': 6,
            '!symbol_4': 7,
            '!symbol_6': 8,
            '!symbol_8': 9,
            '!symbol_14': 10,
            '!symbol_3': 11,
            '!symbol_16': 12,
            '!symbol_2': 13,
            '!symbol_15': 14,
            '$': 15,
            '!symbol_5': 16,
            'string': 17,
            'regular': 18,
            '!symbol_12': 19,
            '!symbol_13': 20,
            '!symbol_1': 21
        }
        self.__sparse_action_table: dict = {
            0: {2: 's7', 4: 's8'},
            1: {15: 'a'},
            2: {2: 's7', 4: 's8', 15: 'r64'},
            3: {2: 'r55', 4: 'r55', 15: 'r55'},
            4: {2: 'r26', 4: 'r26', 15: 'r26'},
            5: {2: 'r62', 4: 'r62', 15: 'r62'},
            6: {2: 'r66', 4: 'r66', 15: 'r66'},
            7: {9: 's17', 13: 's16'},
            8: {2: 's12', 17: 's11'},
            9: {2: 's12', 17: 's11', 21: 's15'},
            10: {2: 'r45', 17: 'r45', 21: 'r45'},
            11: {2: 'r51', 17: 'r51', 21: 'r51'},
            12: {2: 'r53', 17: 'r53', 21: 'r53'},
            13: {2: 'r6', 17: 'r6', 21: 'r6'},
            14: {2: 'r65', 17: 'r65', 21: 'r65'},
            15: {2: 'r24', 4: 'r24', 15: 'r24'},
            16: {18: 's75'},
            17: {1: 's30', 2: 's29', 3: 'r60', 5: 's23', 10: 's18', 13: 'r60', 17: 's28', 21: 'r60'},
            18: {1: 's30', 2: 's29', 10: 's18', 17: 's28'},
            19: {21: 's72'},
            20: {3: 'r48', 21: 'r48'},
            21: {3: 'r1', 13: 's46', 21: 'r1'},
            22: {3: 'r28', 13: 'r28', 21: 'r28'},
            23: {3: 'r49', 13: 'r49', 21: 'r49'},
            24: {1: 's30', 2: 's29', 3: 'r18', 10: 's18', 13: 'r18', 14: 'r18', 17: 's28', 19: 'r18', 21: 'r18'},
            25: {1: 'r40', 2: 'r40', 3: 'r40', 10: 'r40', 13: 'r40', 14: 'r40', 17: 'r40', 19: 'r40', 21: 'r40'},
            26: {1: 'r25', 2: 'r25', 3: 'r25', 10: 'r25', 13: 'r25', 14: 'r25', 17: 'r25', 19: 'r25', 21: 'r25'},
            27: {1: 'r44', 2: 'r44', 3: 'r44', 10: 'r44', 12: 's38', 13: 'r44', 14: 'r44', 17: 'r44', 19: 'r44', 20: 's37', 21: 'r44'},
            28: {1: 'r3', 2: 'r3', 3: 'r3', 10: 'r3', 12: 'r3', 13: 'r3', 14: 'r3', 17: 'r3', 19: 'r3', 20: 'r3', 21: 'r3'},
            29: {1: 'r35', 2: 'r35', 3: 'r35', 10: 'r35', 12: 'r35', 13: 'r35', 14: 'r35', 17: 'r35', 19: 'r35', 20: 'r35', 21: 'r35'},
            30: {1: 's30', 2: 's29', 10: 's18', 17: 's28'},
            31: {3: 's41', 14: 'r15', 19: 'r15'},
            32: {19: 's33'},
            33: {1: 'r44', 2: 'r44', 3: 'r44', 10: 'r44', 12: 's38', 13: 'r44', 14: 'r44', 17: 'r44', 19: 'r44', 20: 's37', 21: 'r44'},
            34: {1: 'r67', 2: 'r67', 3: 'r67', 10: 'r67', 13: 'r67', 14: 'r67', 17: 'r67', 19: 'r67', 21: 'r67'},
            35: {1: 'r14', 2: 'r14', 3: 'r14', 10: 'r14', 13: 'r14', 14: 'r14', 17: 'r14', 19: 'r14', 21: 'r14'},
            36: {1: 'r32', 2: 'r32', 3: 'r32', 10: 'r32', 13: 'r32', 14: 'r32', 17: 'r32', 19: 'r32', 21: 'r32'},
            37: {1: 'r20', 2: 'r20', 3: 'r20', 10: 'r20', 13: 'r20', 14: 'r20', 17: 'r20', 19: 'r20', 21: 'r20'},
            38: {1: 'r68', 2: 'r68', 3: 'r68', 10: 'r68', 13: 'r68', 14: 'r68', 17: 'r68', 19: 'r68', 21: 'r68'},
            39: {3: 's41', 14: 'r17', 19: 'r17'},
            40: {3: 'r39', 14: 'r39', 19: 'r39'},
            41: {1: 's30', 2: 's29', 10: 's18', 17: 's28'},
            42: {3: 'r52', 14: 'r52', 19: 'r52'},
            43: {3: 'r30', 14: 'r30', 19: 'r30'},
            44: {1: 'r58', 2: 'r58', 3: 'r58', 10: 'r58', 13: 'r58', 14: 'r58', 17: 'r58', 19: 'r58', 21: 'r58'},
            45: {1: 'r16', 2: 'r16', 3: 'r16', 10: 'r16', 13: 'r16', 14: 'r16', 17: 'r16', 19: 'r16', 21: 'r16'},
            46: {1: 'r47', 2: 's51'},
            47: {3: 'r4', 21: 'r4'},
            48: {3: 'r43', 21: 'r43'},
            49: {1: 's53'},
            50: {1: 'r46'},
            51: {1: 'r8'},
            52: {3: 'r2', 21: 'r2'},
            53: {6: 'r63', 20: 's57'},
            54: {0: 'r33', 19: 'r33'},
            55: {6: 's58'},
            56: {1: 'r22', 6: 'r22'},
            57: {1: 'r11', 6: 'r11'},
            58: {0: 'r9', 1: 'r63', 19: 'r9', 20: 's57'},
            59: {1: 's53'},
            60: {0: 'r50', 19: 'r50'},
            61: {0: 'r42', 19: 'r42'},
            62: {0: 'r57', 19: 'r57'},
            63: {0: 's64', 19: 's65'},
            64: {6: 'r63', 20: 's57'},
            65: {0: 'r56', 3: 'r56', 19: 'r56', 21: 'r56'},
            66: {0: 'r37', 19: 'r37'},
            67: {0: 'r19', 19: 'r19'},
            68: {3: 's70', 21: 'r7'},
            69: {3: 'r23', 21: 'r23'},
            70: {1: 's30', 2: 's29', 3: 'r60', 5: 's23', 10: 's18', 13: 'r60', 17: 's28', 21: 'r60'},
            71: {3: 'r61', 21: 'r61'},
            72: {2: 'r21', 4: 'r21', 15: 'r21'},
            73: {14: 's74'},
            74: {1: 'r29', 2: 'r29', 3: 'r29', 10: 'r29', 13: 'r29', 14: 'r29', 17: 'r29', 19: 'r29', 21: 'r29'},
            75: {7: 'r54', 11: 's78', 21: 'r54'},
            76: {7: 's79', 21: 'r5'},
            77: {7: 'r34', 21: 'r34'},
            78: {7: 'r31', 21: 'r31'},
            79: {16: 's83'},
            80: {21: 's82'},
            81: {21: 'r13'},
            82: {2: 'r38', 4: 'r38', 15: 'r38'},
            83: {2: 's85'},
            84: {8: 's90'},
            85: {0: 'r36', 8: 'r36'},
            86: {0: 's88', 8: 'r10'},
            87: {0: 'r41', 8: 'r41'},
            88: {2: 's89'},
            89: {0: 'r59', 8: 'r59'},
            90: {21: 'r27'},
            91: {2: 'r12', 4: 'r12', 15: 'r12'}
        }
        self.__sparse_goto_table: dict = {
            0: {5: 2, 6: 5, 20: 4, 22: 3, 24: 6, 41: 1},
            2: {6: 5, 20: 4, 22: 91, 24: 6},
            8: {0: 9, 8: 13, 33: 10},
            9: {8: 14, 33: 10},
            17: {9: 24, 14: 27, 28: 21, 31: 19, 32: 25, 37: 26, 40: 20, 42: 22},
            18: {9: 24, 12: 73, 14: 27, 32: 25, 37: 26, 42: 31},
            20: {30: 68},
            21: {1: 47, 4: 48},
            24: {14: 27, 32: 45, 37: 26},
            27: {10: 34, 16: 44, 26: 36},
            30: {9: 24, 12: 32, 14: 27, 32: 25, 37: 26, 42: 31},
            31: {19: 39, 21: 40},
            33: {10: 34, 16: 35, 26: 36},
            39: {21: 43},
            41: {9: 24, 14: 27, 32: 25, 37: 26, 42: 42},
            46: {13: 50, 35: 49},
            49: {43: 52},
            53: {7: 56, 11: 54, 34: 55},
            54: {25: 63},
            58: {7: 56, 29: 61, 34: 59, 39: 60},
            59: {43: 62},
            63: {18: 66},
            64: {7: 56, 11: 67, 34: 55},
            68: {36: 69},
            70: {9: 24, 14: 27, 28: 21, 32: 25, 37: 26, 40: 71, 42: 22},
            75: {23: 77, 38: 76},
            76: {27: 81, 44: 80},
            83: {3: 84},
            85: {15: 86},
            86: {17: 87}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            17: ('0', '*1'),
            52: ('1',),
            30: ('*0', '*1'),
            29: ('1',),
            14: ('1', '*3'),
            3: ('0',),
            58: ('0', '*1'),
            44: (),
            67: ('*0',),
            50: ('*0', '1', '*2'),
            57: ('*0', '1'),
            9: (),
            42: ('*0',),
            63: (),
            22: ('*0',),
            56: ('1', '*2'),
            19: ('1',),
            33: (),
            37: ('*0', '*1'),
            18: ('*0',),
            16: ('*0', '1'),
            28: ('*0',),
            4: ('0', '*1'),
            2: ('*1', '2'),
            1: (),
            43: ('*0',),
            47: (),
            46: ('*0',),
            7: ('0', '*1'),
            61: ('1',),
            48: (),
            23: ('*0', '*1'),
            21: ('0', '2'),
            10: ('0', '*1'),
            59: ('1',),
            36: (),
            41: ('*0', '*1'),
            38: ('0', '2', '*3', '4'),
            27: ('*2',),
            5: (),
            13: ('*0',),
            54: (),
            34: ('*0',),
            24: ('0', '*1'),
            65: ('*0', '1'),
            12: ('*0', '1'),
            39: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 0, 3, 1, 2, 0, 1, 2, 1, 0, 2, 1, 2, 1, 4, 1, 2, 2, 1, 2, 1, 4, 1, 2, 3, 1, 1, 4, 1, 3, 2, 1, 1, 0, 1, 1, 0, 2, 6, 1, 1, 2, 1, 1, 0, 1, 1, 0, 0, 1, 3, 1, 2, 1, 0, 1, 4, 2, 2, 2, 0, 2, 1, 0, 1, 2, 1, 1, 1]
        self.__reduce_non_terminal_index: list = [2, 1, 4, 14, 40, 44, 0, 31, 13, 39, 3, 7, 5, 44, 37, 12, 9, 12, 42, 18, 26, 24, 34, 30, 6, 32, 22, 27, 28, 37, 19, 23, 10, 25, 38, 14, 15, 25, 20, 19, 9, 15, 39, 1, 16, 8, 35, 35, 30, 28, 11, 33, 21, 33, 38, 5, 43, 29, 32, 17, 28, 36, 22, 34, 41, 0, 22, 16, 26]

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
                elif statement_index in {0, 6, 8, 11, 15, 20, 25, 26, 31, 32, 35, 40, 45, 49, 51, 53, 55, 60, 62, 64, 66, 68}:
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
            24: 'command',
            38: 'lexical_define',
            21: 'reduce',
            50: 'grammar_node',
            58: 'name_closure',
            3: 'literal',
            14: 'complex_closure',
            29: 'complex_optional',
            17: 'select'
        }
        self.__naive_reduce_number_set: set = {66, 35, 3, 68, 28, 15, 49, 51, 20, 53, 25, 26, 60, 62}
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
