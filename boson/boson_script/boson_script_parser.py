class LexicalToken:
    text: str
    line: int
    symbol: str

    def __init__(self, text: str, line: int, symbol: str):
        self.text = text
        self.line = line
        self.symbol = symbol


class BosonLexicalAnalyzer:
    def __init__(self):
        self.__token_list = []
        self.__line = 1
        self.__error_line = -1
        self.__no_error_line = -1
        self.__skip = False
        self.__move_table = {
            0: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 1],
                [0, {'|'}, [], 2],
                [0, {'"'}, [], 33],
                [0, {'@'}, [], 3],
                [0, {'='}, [], 4],
                [0, {')'}, [], 5],
                [0, {'}'}, [], 6],
                [0, {'\n'}, [], 7],
                [0, {'<'}, [], 8],
                [0, {' ', '\t'}, [], 9],
                [0, {'#'}, [], 28],
                [0, {']'}, [], 10],
                [0, {'%'}, [], 11],
                [0, {'~'}, [], 12],
                [0, {';'}, [], 13],
                [0, {'*'}, [], 14],
                [0, {':'}, [], 15],
                [0, {','}, [], 16],
                [0, {'['}, [], 17],
                [0, {'('}, [], 18],
                [0, {'$'}, [], 19],
                [0, {'!'}, [], 20],
                [0, {'+'}, [], 21],
                [0, {'{'}, [], 22],
                [0, {"'"}, [], 23]
            ],
            23: [
                [2, {'\\'}, [], 24],
                [0, {'\\'}, [], 23]
            ],
            24: [
                [2, {"'", '\\'}, [], 24],
                [0, {'\\'}, [], 23],
                [0, {"'"}, [], 25]
            ],
            25: [
                [2, {"'", '\\'}, [], 24],
                [0, {'\\'}, [], 23],
                [0, {"'"}, [], 25]
            ],
            19: [
                [0, set(), [('0', '9')], 26]
            ],
            26: [
                [0, set(), [('0', '9')], 26]
            ],
            11: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 27]
            ],
            27: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 27]
            ],
            28: [
                [2, {'\n', '\r'}, [], 28]
            ],
            9: [
                [0, {' ', '\t'}, [], 9]
            ],
            8: [
                [2, {'\\'}, [], 29],
                [0, {'\\'}, [], 8]
            ],
            29: [
                [2, {'>', '\\'}, [], 29],
                [0, {'\\'}, [], 8],
                [0, {'>'}, [], 30]
            ],
            30: [
                [2, {'>', '\\'}, [], 29],
                [0, {'\\'}, [], 8],
                [0, {'>'}, [], 30]
            ],
            7: [
                [0, {'\r'}, [], 31]
            ],
            33: [
                [2, {'\\'}, [], 32],
                [0, {'\\'}, [], 33]
            ],
            32: [
                [2, {'"', '\\'}, [], 32],
                [0, {'"'}, [], 34],
                [0, {'\\'}, [], 33]
            ],
            34: [
                [2, {'"', '\\'}, [], 32],
                [0, {'"'}, [], 34],
                [0, {'\\'}, [], 33]
            ],
            1: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 1]
            ]
        }
        self.__character_set = {'q', 'U', '|', '8', 'u', 'E', '3', '"', '@', 'd', '_', '=', '5', ')', '}', '4', 'Y', '7', '2', '\\', 'B', '9', 'O', '\n', '<', 'x', ' ', 's', 't', 'p', 'N', 'G', 'b', 'L', 'F', 'j', 'v', 'V', 'R', 'y', '#', 'm', '%', ']', '~', ';', '1', 'l', 'T', '>', 'e', 'P', '*', ':', 'r', 'g', '\t', 'z', 'o', 'D', ',', 'a', 'J', 'Z', '[', 'f', 'k', '(', '$', '!', '+', 'i', 'W', 'Q', 'H', 'K', 'n', 'M', 'S', 'C', 'A', '6', 'c', 'I', 'w', '0', '{', '\r', 'h', "'", 'X'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 25, 26, 27, 28, 30, 31, 34}
        self.__lexical_symbol_mapping = {
            1: 'name',
            2: '!symbol_9',
            3: '!symbol_4',
            4: '!symbol_2',
            5: '!symbol_12',
            6: '!symbol_6',
            7: 'newline',
            9: 'skip',
            10: '!symbol_15',
            12: '!symbol_10',
            13: '!symbol_1',
            14: '!symbol_13',
            15: '!symbol_8',
            16: '!symbol_7',
            17: '!symbol_14',
            18: '!symbol_11',
            20: '!symbol_3',
            21: '!symbol_16',
            22: '!symbol_5',
            25: 'string',
            26: 'node',
            27: 'command',
            28: 'comment',
            30: 'regular',
            31: 'newline',
            34: 'string'
        }
        self.__non_greedy_state_set = {25, 34, 30}
        self.__symbol_function_mapping = {
            'name': [],
            'node': [],
            'string': [],
            'regular': [],
            'comment': ['skip'],
            'command': [],
            'skip': ['skip'],
            'newline': ['skip', 'newline']
        }
        self.__lexical_function = {}

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

    def lexical_function_entity(self, function_name: str) -> callable:
        def decorator(f: callable):
            self.__lexical_function[function_name] = f
            return f
        return decorator


class BosonGrammar:
    def __init__(self):
        self.__grammar_tree = None
        self.__error_index = -1
        self.__no_error_index = -1

    def get_grammar_tree(self):
        return self.__grammar_tree

    def set_grammar_tree(self, grammar_tree: tuple):
        self.__grammar_tree = grammar_tree

    grammar_tree = property(get_grammar_tree, set_grammar_tree)

    def get_error_index(self):
        return self.__error_index

    def set_error_index(self, error_index: int):
        self.__error_index = error_index

    error_index = property(get_error_index, set_error_index)

    def no_error_index(self):
        return self.__no_error_index


class BosonGrammarNode:
    def __init__(self):
        self.reduce_number = -1
        self.__data = []

    def __getitem__(self, item):
        return self.__data[item]

    def __iadd__(self, other):
        self.__data += other
        return self

    def append(self, item):
        self.__data.append(item)

    def insert(self, index, item):
        self.__data.insert(index, item)

    def data(self):
        return self.__data


class BosonGrammarAnalyzer:
    def __init__(self):
        self.__terminal_index_mapping = {
            '!symbol_1': 0,
            '!symbol_12': 1,
            '$': 2,
            'node': 3,
            '!symbol_11': 4,
            '!symbol_10': 5,
            '!symbol_3': 6,
            'name': 7,
            '!symbol_14': 8,
            '!symbol_7': 9,
            '!symbol_2': 10,
            'string': 11,
            '!symbol_16': 12,
            '!symbol_4': 13,
            '!symbol_15': 14,
            'command': 15,
            '!symbol_5': 16,
            'regular': 17,
            '!symbol_9': 18,
            '!symbol_13': 19,
            '!symbol_6': 20,
            '!symbol_8': 21
        }
        self.__sparse_action_table = {
            0: {7: 's4', 15: 's3'},
            1: {2: 'r63', 7: 's4', 15: 's3'},
            2: {2: 'r14', 7: 'r14', 15: 'r14'},
            3: {7: 's12', 11: 's14'},
            4: {10: 's16', 21: 's15'},
            5: {2: 'a'},
            6: {2: 'r69', 7: 'r69', 15: 'r69'},
            7: {2: 'r4', 7: 'r4', 15: 'r4'},
            8: {2: 'r38', 7: 'r38', 15: 'r38'},
            9: {2: 'r3', 7: 'r3', 15: 'r3'},
            10: {0: 'r43', 7: 'r43', 11: 'r43'},
            11: {0: 'r2', 7: 'r2', 11: 'r2'},
            12: {0: 'r52', 7: 'r52', 11: 'r52'},
            13: {0: 's17', 7: 's12', 11: 's14'},
            14: {0: 'r15', 7: 'r15', 11: 'r15'},
            15: {0: 'r59', 4: 's28', 5: 's26', 7: 's20', 8: 's30', 10: 'r59', 11: 's24', 18: 'r59'},
            16: {17: 's31'},
            17: {2: 'r27', 7: 'r27', 15: 'r27'},
            18: {0: 'r53', 7: 'r53', 11: 'r53'},
            19: {0: 'r37', 4: 's28', 7: 's20', 8: 's30', 10: 'r37', 11: 's24', 18: 'r37'},
            20: {0: 'r24', 1: 'r24', 4: 'r24', 7: 'r24', 8: 'r24', 10: 'r24', 11: 'r24', 12: 'r24', 14: 'r24', 18: 'r24', 19: 'r24'},
            21: {0: 'r17', 10: 's34', 18: 'r17'},
            22: {0: 'r40', 18: 'r40'},
            23: {0: 'r23', 1: 'r23', 4: 'r23', 7: 'r23', 8: 'r23', 10: 'r23', 11: 'r23', 14: 'r23', 18: 'r23'},
            24: {0: 'r67', 1: 'r67', 4: 'r67', 7: 'r67', 8: 'r67', 10: 'r67', 11: 'r67', 12: 'r67', 14: 'r67', 18: 'r67', 19: 'r67'},
            25: {0: 's37'},
            26: {0: 'r16', 10: 'r16', 18: 'r16'},
            27: {0: 'r10', 4: 'r10', 7: 'r10', 8: 'r10', 10: 'r10', 11: 'r10', 18: 'r10'},
            28: {4: 's28', 7: 's20', 8: 's30', 11: 's24'},
            29: {0: 'r7', 1: 'r7', 4: 'r7', 7: 'r7', 8: 'r7', 10: 'r7', 11: 'r7', 12: 's44', 14: 'r7', 18: 'r7', 19: 's43'},
            30: {4: 's28', 7: 's20', 8: 's30', 11: 's24'},
            31: {0: 'r34', 6: 's47', 13: 'r34'},
            32: {0: 'r73', 4: 'r73', 7: 'r73', 8: 'r73', 10: 'r73', 11: 'r73', 18: 'r73'},
            33: {0: 'r12', 18: 'r12'},
            34: {4: 'r6', 7: 's52'},
            35: {0: 'r60', 18: 'r60'},
            36: {0: 'r56', 18: 's54'},
            37: {2: 'r44', 7: 'r44', 15: 'r44'},
            38: {1: 'r9', 4: 'r9', 7: 'r9', 8: 'r9', 11: 'r9', 14: 'r9', 18: 's57'},
            39: {1: 'r49', 4: 's28', 7: 's20', 8: 's30', 11: 's24', 14: 'r49'},
            40: {1: 's59'},
            41: {0: 'r22', 1: 'r22', 4: 'r22', 7: 'r22', 8: 'r22', 10: 'r22', 11: 'r22', 14: 'r22', 18: 'r22'},
            42: {0: 'r5', 1: 'r5', 4: 'r5', 7: 'r5', 8: 'r5', 10: 'r5', 11: 'r5', 14: 'r5', 18: 'r5'},
            43: {0: 'r46', 1: 'r46', 4: 'r46', 7: 'r46', 8: 'r46', 10: 'r46', 11: 'r46', 14: 'r46', 18: 'r46'},
            44: {0: 'r42', 1: 'r42', 4: 'r42', 7: 'r42', 8: 'r42', 10: 'r42', 11: 'r42', 14: 'r42', 18: 'r42'},
            45: {0: 'r21', 1: 'r21', 4: 'r21', 7: 'r21', 8: 'r21', 10: 'r21', 11: 'r21', 14: 'r21', 18: 'r21'},
            46: {14: 's60'},
            47: {0: 'r51', 13: 'r51'},
            48: {0: 'r8', 13: 'r8'},
            49: {0: 'r57', 13: 's61'},
            50: {4: 's64'},
            51: {4: 'r35'},
            52: {4: 'r11'},
            53: {0: 'r25', 18: 'r25'},
            54: {0: 'r59', 4: 's28', 5: 's26', 7: 's20', 8: 's30', 10: 'r59', 11: 's24', 18: 'r59'},
            55: {1: 'r33', 14: 'r33', 18: 's57'},
            56: {1: 'r18', 14: 'r18', 18: 'r18'},
            57: {4: 's28', 7: 's20', 8: 's30', 11: 's24'},
            58: {1: 'r36', 4: 'r36', 7: 'r36', 8: 'r36', 11: 'r36', 14: 'r36'},
            59: {0: 'r74', 1: 'r74', 4: 'r74', 7: 'r74', 8: 'r74', 10: 'r74', 11: 'r74', 12: 's44', 14: 'r74', 18: 'r74', 19: 's43'},
            60: {0: 'r41', 1: 'r41', 4: 'r41', 7: 'r41', 8: 'r41', 10: 'r41', 11: 'r41', 14: 'r41', 18: 'r41'},
            61: {16: 's72'},
            62: {0: 's73'},
            63: {0: 'r65'},
            64: {3: 'r70', 19: 's74'},
            65: {0: 'r31', 18: 'r31'},
            66: {0: 'r29', 18: 'r29'},
            67: {1: 'r72', 14: 'r72', 18: 'r72'},
            68: {1: 'r54', 14: 'r54', 18: 'r54'},
            69: {0: 'r26', 1: 'r26', 4: 'r26', 7: 'r26', 8: 'r26', 10: 'r26', 11: 'r26', 14: 'r26', 18: 'r26'},
            70: {0: 'r50', 1: 'r50', 4: 'r50', 7: 'r50', 8: 'r50', 10: 'r50', 11: 'r50', 14: 'r50', 18: 'r50'},
            71: {0: 'r48', 1: 'r48', 4: 'r48', 7: 'r48', 8: 'r48', 10: 'r48', 11: 'r48', 14: 'r48', 18: 'r48'},
            72: {7: 's79'},
            73: {2: 'r28', 7: 'r28', 15: 'r28'},
            74: {3: 'r71'},
            75: {3: 'r58'},
            76: {3: 's80'},
            77: {1: 'r64', 9: 'r64'},
            78: {20: 's82'},
            79: {9: 'r19', 20: 'r19'},
            80: {1: 'r13', 4: 'r39', 9: 'r13', 19: 's88'},
            81: {1: 's91', 9: 's90'},
            82: {0: 'r30'},
            83: {9: 's92', 20: 'r55'},
            84: {1: 'r47', 9: 'r47'},
            85: {1: 'r20', 9: 'r20'},
            86: {4: 's64'},
            87: {4: 'r32'},
            88: {4: 'r62'},
            89: {1: 'r1', 9: 'r1'},
            90: {3: 'r70', 19: 's74'},
            91: {0: 'r68', 1: 'r68', 9: 'r68', 18: 'r68'},
            92: {7: 's96'},
            93: {9: 'r45', 20: 'r45'},
            94: {1: 'r75', 9: 'r75'},
            95: {1: 'r61', 9: 'r61'},
            96: {9: 'r66', 20: 'r66'}
        }
        self.__sparse_goto_table = {
            0: {6: 8, 19: 1, 23: 6, 24: 7, 41: 5, 42: 2},
            1: {6: 9, 23: 6, 24: 7, 42: 2},
            3: {7: 13, 27: 10, 32: 11},
            13: {27: 10, 32: 18},
            15: {1: 19, 9: 25, 18: 22, 21: 29, 29: 23, 33: 27, 38: 21},
            19: {21: 29, 29: 23, 33: 32},
            21: {3: 33, 22: 35},
            22: {2: 36},
            28: {14: 40, 21: 29, 29: 23, 33: 38, 39: 39},
            29: {28: 45, 30: 41, 45: 42},
            30: {14: 46, 21: 29, 29: 23, 33: 38, 39: 39},
            31: {0: 49, 16: 48},
            34: {4: 51, 44: 50},
            36: {31: 53},
            38: {5: 56, 26: 55},
            39: {21: 29, 29: 23, 33: 58},
            49: {12: 63, 43: 62},
            50: {15: 65},
            54: {1: 19, 18: 66, 21: 29, 29: 23, 33: 27, 38: 21},
            55: {5: 67},
            57: {21: 29, 29: 23, 33: 68},
            59: {8: 70, 10: 69, 30: 71},
            64: {37: 77, 46: 76, 48: 75},
            72: {40: 78},
            77: {11: 81},
            79: {35: 83},
            80: {13: 84, 17: 86, 34: 85, 47: 87},
            81: {20: 89},
            83: {25: 93},
            86: {15: 94},
            90: {37: 95, 46: 76, 48: 75}
        }
        self.__sentence_index_grammar_tuple_mapping = {
            32: ('0', '*1'),
            53: ('1',),
            48: ('*0',),
            71: ('*0', '*1'),
            35: ('*0', '1'),
            40: ('1',),
            25: ('1', '*3'),
            73: (),
            49: ('*0',),
            66: ('0',),
            4: ('0', '*1'),
            6: (),
            20: ('*0',),
            46: ('*0', '1', '*2'),
            74: ('*0', '1'),
            12: (),
            19: ('*0',),
            38: (),
            31: ('*0',),
            69: (),
            57: ('*0',),
            67: ('1', '*2'),
            60: ('1',),
            63: (),
            0: ('*0', '*1'),
            36: ('*0',),
            72: ('*0', '1'),
            59: ('0', '*1'),
            30: ('*1', '2'),
            16: (),
            11: ('*0',),
            5: (),
            34: ('*0',),
            55: ('0', '*1'),
            28: ('1',),
            39: (),
            24: ('*0', '*1'),
            43: ('0', '2'),
            54: ('0', '*1'),
            65: ('1',),
            18: (),
            44: ('*0', '*1'),
            27: ('0', '2', '*3', '4'),
            29: ('*2',),
            56: (),
            64: ('*0',),
            33: (),
            7: ('*0',),
            26: ('0', '*1'),
            52: ('*0', '1'),
            2: ('*0', '1'),
            17: ('*0',)
        }
        self.__reduce_symbol_count = [2, 1, 2, 1, 2, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 2, 4, 3, 6, 2, 4, 3, 1, 2, 0, 1, 2, 1, 1, 0, 0, 3, 1, 1, 4, 2, 1, 3, 1, 1, 1, 1, 1, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1, 1, 0, 1, 2, 1, 4, 1, 0, 1, 2, 2, 0, 2]
        self.__reduce_non_terminal_index = [11, 7, 19, 6, 33, 44, 45, 0, 39, 1, 4, 22, 13, 6, 27, 38, 22, 26, 35, 13, 45, 28, 33, 21, 2, 29, 23, 24, 31, 12, 3, 17, 14, 0, 44, 39, 38, 19, 17, 2, 29, 30, 32, 42, 35, 30, 37, 8, 14, 10, 16, 27, 7, 5, 40, 9, 43, 46, 38, 18, 20, 47, 41, 11, 43, 25, 21, 15, 6, 46, 48, 26, 1, 10, 34]

    def grammar_analysis(self, token_list: list) -> BosonGrammar:
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
                statement_index = int(operation[1:]) - 1
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
                elif statement_index in {1, 3, 8, 9, 10, 13, 14, 15, 21, 22, 23, 37, 41, 42, 45, 47, 50, 51, 58, 61, 62, 68, 70}:
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


class BosonSemanticsAnalyzer:
    def __init__(self):
        self.__reduce_number_grammar_name_mapping = {
            26: 'command',
            27: 'lexical_define',
            43: 'reduce',
            46: 'grammar_node',
            4: 'name_closure',
            66: 'literal',
            25: 'complex_closure',
            40: 'complex_optional',
            32: 'select'
        }
        self.__naive_reduce_number_set = {66, 3, 68, 41, 13, 14, 15, 45, 51, 22, 23, 58}
        self.__semantics_entity = {}

    @staticmethod
    def __default_semantics_entity(grammar_entity: list) -> list:
        return grammar_entity

    @staticmethod
    def __naive_semantics_entity(grammar_entity: list):
        if len(grammar_entity) == 0:
            return None
        elif len(grammar_entity) == 1:
            return grammar_entity[0]
        else:
            return grammar_entity

    def __semantics_analysis(self, grammar_tree: BosonGrammarNode):
        if grammar_tree.reduce_number in self.__reduce_number_grammar_name_mapping:
            grammar_name = self.__reduce_number_grammar_name_mapping[grammar_tree.reduce_number]
        else:
            grammar_name = '!grammar_hidden'
        grammar_entity = list(map(lambda g: self.__semantics_analysis(g) if isinstance(g, BosonGrammarNode) else g, grammar_tree.data()))
        if grammar_name in self.__semantics_entity:
            return self.__semantics_entity[grammar_name](grammar_entity)
        elif grammar_tree.reduce_number in self.__naive_reduce_number_set:
            return self.__naive_semantics_entity(grammar_entity)
        else:
            return self.__default_semantics_entity(grammar_entity)

    def semantics_analysis(self, grammar_tree: BosonGrammarNode):
        return self.__semantics_analysis(grammar_tree)

    def semantics_entity(self, name: str) -> callable:
        def decorator(f: callable):
            self.__semantics_entity[name] = f
            return f
        return decorator
