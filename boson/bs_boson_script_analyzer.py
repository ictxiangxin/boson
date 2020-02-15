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
                [0, {'}'}, [], 2],
                [0, {':'}, [], 3],
                [0, {'{'}, [], 4],
                [0, {'('}, [], 5],
                [0, {'<'}, [], 34],
                [0, {'\t', ' '}, [], 6],
                [0, {'\n'}, [], 7],
                [0, {"'"}, [], 30],
                [0, {']'}, [], 8],
                [0, {'@'}, [], 9],
                [0, {'~'}, [], 10],
                [0, {','}, [], 11],
                [0, {'#'}, [], 28],
                [0, {'"'}, [], 12],
                [0, {'%'}, [], 13],
                [0, {'|'}, [], 14],
                [0, {'*'}, [], 15],
                [0, {'$'}, [], 16],
                [0, {'['}, [], 17],
                [0, {'+'}, [], 18],
                [0, {')'}, [], 19],
                [0, {'!'}, [], 20],
                [0, {'='}, [], 21],
                [0, {';'}, [], 22]
            ],
            16: [
                [0, set(), [('0', '9')], 23],
                [0, {'$', '?', '@'}, [], 24]
            ],
            23: [
                [0, set(), [('0', '9')], 23]
            ],
            13: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 25]
            ],
            25: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 25]
            ],
            12: [
                [2, {'\\'}, [], 26],
                [0, {'\\'}, [], 12]
            ],
            26: [
                [2, {'\\', '"'}, [], 26],
                [0, {'\\'}, [], 12],
                [0, {'"'}, [], 27]
            ],
            27: [
                [2, {'\\', '"'}, [], 26],
                [0, {'\\'}, [], 12],
                [0, {'"'}, [], 27]
            ],
            28: [
                [2, {'\n', '\r'}, [], 28]
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
            7: [
                [0, {'\r'}, [], 32]
            ],
            6: [
                [0, {'\t', ' '}, [], 6]
            ],
            34: [
                [2, {'\\'}, [], 33],
                [0, {'\\'}, [], 34]
            ],
            33: [
                [2, {'\\', '>'}, [], 33],
                [0, {'>'}, [], 35],
                [0, {'\\'}, [], 34]
            ],
            35: [
                [2, {'\\', '>'}, [], 33],
                [0, {'>'}, [], 35],
                [0, {'\\'}, [], 34]
            ],
            1: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 1]
            ]
        }
        self.__character_set = {'g', 'O', 'R', '}', 'k', ':', 'u', 'd', 'n', 'N', 'P', 'V', '{', '2', '(', '<', 'K', '>', 'v', '7', ' ', '\n', "'", 'L', 'Q', '\\', ']', 'l', 'y', 'r', 'A', '@', 'c', 't', 'I', '3', '~', ',', 'G', 'C', '#', 'T', 'E', '0', 'f', '5', '"', 'p', '%', 's', '\t', '|', 'X', 'x', '?', 'j', '4', 'F', 'M', 'e', 'Z', 'q', '*', '\r', 'U', '9', 'D', 'H', 'h', 'B', 'S', 'W', '6', 'Y', '$', '[', 'a', '+', 'i', 'o', '8', '_', ')', 'm', 'w', 'z', '!', '1', '=', 'J', ';', 'b'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 31, 32, 35}
        self.__lexical_symbol_mapping = {
            1: 'name',
            2: '!symbol_6',
            3: '!symbol_8',
            4: '!symbol_5',
            5: '!symbol_11',
            6: 'skip',
            7: 'newline',
            8: '!symbol_15',
            9: '!symbol_4',
            10: '!symbol_10',
            11: '!symbol_7',
            14: '!symbol_9',
            15: '!symbol_13',
            17: '!symbol_14',
            18: '!symbol_16',
            19: '!symbol_12',
            20: '!symbol_3',
            21: '!symbol_2',
            22: '!symbol_1',
            23: 'node',
            24: 'node',
            25: 'command',
            27: 'string',
            28: 'comment',
            31: 'string',
            32: 'newline',
            35: 'regular'
        }
        self.__non_greedy_state_set = {35, 27, 31}
        self.__symbol_function_mapping = {
            'comment': ['skip'],
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

    def lexical_function_entity(self, function_name):
        def decorator(f):
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
        self.__terminal_index = {
            '!symbol_7': 0,
            '!symbol_16': 1,
            '!symbol_8': 2,
            '$': 3,
            '!symbol_4': 4,
            '!symbol_2': 5,
            'node': 6,
            '!symbol_6': 7,
            '!symbol_15': 8,
            '!symbol_9': 9,
            'regular': 10,
            '!symbol_1': 11,
            '!symbol_14': 12,
            'string': 13,
            'command': 14,
            '!symbol_3': 15,
            '!symbol_5': 16,
            '!symbol_12': 17,
            '!symbol_11': 18,
            '!symbol_13': 19,
            'name': 20,
            '!symbol_10': 21
        }
        self.__action_table = {
            0: {14: 's6', 20: 's3'},
            1: {3: 'r66', 14: 'r66', 20: 'r66'},
            2: {3: 'r2', 14: 'r2', 20: 'r2'},
            3: {2: 's10', 5: 's9'},
            4: {3: 'r48', 14: 's6', 20: 's3'},
            5: {3: 'r68', 14: 'r68', 20: 'r68'},
            6: {13: 's15', 20: 's14'},
            7: {3: 'a'},
            8: {3: 'r67', 14: 'r67', 20: 'r67'},
            9: {10: 's17'},
            10: {5: 'r57', 9: 'r57', 11: 'r57', 12: 's20', 13: 's26', 18: 's24', 20: 's22', 21: 's18'},
            11: {3: 'r1', 14: 'r1', 20: 'r1'},
            12: {11: 'r20', 13: 'r20', 20: 'r20'},
            13: {11: 's30', 13: 's15', 20: 's14'},
            14: {11: 'r3', 13: 'r3', 20: 'r3'},
            15: {11: 'r4', 13: 'r4', 20: 'r4'},
            16: {11: 'r37', 13: 'r37', 20: 'r37'},
            17: {3: 'r41', 4: 'r41', 11: 'r41', 14: 'r41', 15: 's33', 20: 'r41'},
            18: {5: 'r56', 9: 'r56', 11: 'r56'},
            19: {1: 's39', 5: 'r28', 8: 'r28', 9: 'r28', 11: 'r28', 12: 'r28', 13: 'r28', 17: 'r28', 18: 'r28', 19: 's35', 20: 'r28'},
            20: {12: 's20', 13: 's26', 18: 's24', 20: 's22'},
            21: {9: 'r7', 11: 'r7'},
            22: {1: 'r71', 5: 'r71', 8: 'r71', 9: 'r71', 11: 'r71', 12: 'r71', 13: 'r71', 17: 'r71', 18: 'r71', 19: 'r71', 20: 'r71'},
            23: {11: 's44'},
            24: {12: 's20', 13: 's26', 18: 's24', 20: 's22'},
            25: {5: 'r59', 8: 'r59', 9: 'r59', 11: 'r59', 12: 'r59', 13: 'r59', 17: 'r59', 18: 'r59', 20: 'r59'},
            26: {1: 'r72', 5: 'r72', 8: 'r72', 9: 'r72', 11: 'r72', 12: 'r72', 13: 'r72', 17: 'r72', 18: 'r72', 19: 'r72', 20: 'r72'},
            27: {5: 'r55', 9: 'r55', 11: 'r55', 12: 's20', 13: 's26', 18: 's24', 20: 's22'},
            28: {5: 'r15', 9: 'r15', 11: 'r15', 12: 'r15', 13: 'r15', 18: 'r15', 20: 'r15'},
            29: {5: 's49', 9: 'r13', 11: 'r13'},
            30: {3: 'r51', 14: 'r51', 20: 'r51'},
            31: {11: 'r38', 13: 'r38', 20: 'r38'},
            32: {4: 's52', 11: 'r44'},
            33: {3: 'r39', 4: 'r39', 11: 'r39', 14: 'r39', 20: 'r39'},
            34: {3: 'r40', 4: 'r40', 11: 'r40', 14: 'r40', 20: 'r40'},
            35: {5: 'r49', 8: 'r49', 9: 'r49', 11: 'r49', 12: 'r49', 13: 'r49', 17: 'r49', 18: 'r49', 20: 'r49'},
            36: {5: 'r60', 8: 'r60', 9: 'r60', 11: 'r60', 12: 'r60', 13: 'r60', 17: 'r60', 18: 'r60', 20: 'r60'},
            37: {5: 'r26', 8: 'r26', 9: 'r26', 11: 'r26', 12: 'r26', 13: 'r26', 17: 'r26', 18: 'r26', 20: 'r26'},
            38: {5: 'r27', 8: 'r27', 9: 'r27', 11: 'r27', 12: 'r27', 13: 'r27', 17: 'r27', 18: 'r27', 20: 'r27'},
            39: {5: 'r50', 8: 'r50', 9: 'r50', 11: 'r50', 12: 'r50', 13: 'r50', 17: 'r50', 18: 'r50', 20: 'r50'},
            40: {8: 's53'},
            41: {8: 'r69', 12: 's20', 13: 's26', 17: 'r69', 18: 's24', 20: 's22'},
            42: {8: 'r33', 9: 's56', 12: 'r33', 13: 'r33', 17: 'r33', 18: 'r33', 20: 'r33'},
            43: {9: 's58', 11: 'r58'},
            44: {3: 'r61', 14: 'r61', 20: 'r61'},
            45: {17: 's60'},
            46: {5: 'r14', 9: 'r14', 11: 'r14', 12: 'r14', 13: 'r14', 18: 'r14', 20: 'r14'},
            47: {9: 'r54', 11: 'r54'},
            48: {9: 'r12', 11: 'r12'},
            49: {18: 'r10', 20: 's61'},
            50: {11: 's64'},
            51: {11: 'r43'},
            52: {16: 's65'},
            53: {5: 'r53', 8: 'r53', 9: 'r53', 11: 'r53', 12: 'r53', 13: 'r53', 17: 'r53', 18: 'r53', 20: 'r53'},
            54: {8: 'r32', 12: 'r32', 13: 'r32', 17: 'r32', 18: 'r32', 20: 'r32'},
            55: {8: 'r70', 9: 's56', 17: 'r70'},
            56: {12: 's20', 13: 's26', 18: 's24', 20: 's22'},
            57: {8: 'r35', 9: 'r35', 17: 'r35'},
            58: {5: 'r57', 9: 'r57', 11: 'r57', 12: 's20', 13: 's26', 18: 's24', 20: 's22', 21: 's18'},
            59: {9: 'r6', 11: 'r6'},
            60: {1: 's39', 5: 'r31', 8: 'r31', 9: 'r31', 11: 'r31', 12: 'r31', 13: 'r31', 17: 'r31', 18: 'r31', 19: 's35', 20: 'r31'},
            61: {18: 'r8'},
            62: {18: 'r9'},
            63: {18: 's72'},
            64: {3: 'r64', 14: 'r64', 20: 'r64'},
            65: {20: 's75'},
            66: {8: 'r36', 9: 'r36', 17: 'r36'},
            67: {8: 'r34', 9: 'r34', 17: 'r34'},
            68: {9: 'r5', 11: 'r5'},
            69: {5: 'r30', 8: 'r30', 9: 'r30', 11: 'r30', 12: 'r30', 13: 'r30', 17: 'r30', 18: 'r30', 20: 'r30'},
            70: {5: 'r52', 8: 'r52', 9: 'r52', 11: 'r52', 12: 'r52', 13: 'r52', 17: 'r52', 18: 'r52', 20: 'r52'},
            71: {5: 'r29', 8: 'r29', 9: 'r29', 11: 'r29', 12: 'r29', 13: 'r29', 17: 'r29', 18: 'r29', 20: 'r29'},
            72: {6: 'r22', 19: 's76'},
            73: {9: 'r11', 11: 'r11'},
            74: {7: 's80'},
            75: {0: 'r47', 7: 'r47'},
            76: {6: 'r19'},
            77: {6: 's82'},
            78: {6: 'r21'},
            79: {0: 'r18', 17: 'r18'},
            80: {11: 'r42'},
            81: {0: 's85', 7: 'r63'},
            82: {0: 'r25', 9: 'r25', 11: 'r25', 17: 'r25', 18: 's72'},
            83: {0: 's90', 17: 's91'},
            84: {0: 'r46', 7: 'r46'},
            85: {20: 's92'},
            86: {0: 'r24', 9: 'r24', 11: 'r24', 17: 'r24'},
            87: {0: 'r23', 9: 'r23', 11: 'r23', 17: 'r23'},
            88: {0: 'r65', 9: 'r65', 11: 'r65', 17: 'r65'},
            89: {0: 'r17', 17: 'r17'},
            90: {6: 'r22', 19: 's76'},
            91: {0: 'r62', 9: 'r62', 11: 'r62', 17: 'r62'},
            92: {0: 'r45', 7: 'r45'},
            93: {0: 'r16', 17: 'r16'}
        }
        self.__goto_table = {
            0: {0: 5, 4: 4, 10: 8, 18: 1, 28: 2, 39: 7},
            4: {0: 5, 10: 8, 18: 1, 28: 11},
            6: {6: 12, 13: 16, 31: 13},
            10: {3: 27, 14: 25, 17: 23, 26: 29, 27: 28, 33: 21, 41: 19},
            13: {6: 12, 13: 31},
            17: {15: 32, 21: 34},
            19: {32: 37, 36: 36, 40: 38},
            20: {2: 40, 14: 25, 27: 42, 38: 41, 41: 19},
            21: {1: 43},
            24: {2: 45, 14: 25, 27: 42, 38: 41, 41: 19},
            27: {14: 25, 27: 46, 41: 19},
            29: {23: 47, 46: 48},
            32: {20: 51, 35: 50},
            41: {14: 25, 27: 54, 41: 19},
            42: {16: 57, 42: 55},
            43: {34: 59},
            49: {5: 62, 44: 63},
            55: {16: 66},
            56: {14: 25, 27: 67, 41: 19},
            58: {3: 27, 14: 25, 26: 29, 27: 28, 33: 68, 41: 19},
            60: {25: 69, 30: 70, 32: 71},
            63: {24: 73},
            65: {12: 74},
            72: {7: 77, 19: 79, 45: 78},
            75: {9: 81},
            79: {8: 83},
            81: {11: 84},
            82: {24: 87, 29: 88, 43: 86},
            83: {37: 89},
            90: {7: 77, 19: 93, 45: 78}
        }
        self.__node_table = {
            0: ('*0', '1'),
            37: ('*0', '1'),
            50: ('0', ('*1', ('?',))),
            40: (),
            43: (),
            63: ('0', '2', ('*3', ('?',)), ('4', ('*2',))),
            45: ('*0', '1'),
            46: (),
            62: ('0', ('*1', ('1',))),
            60: ('0', '2'),
            5: ('*0', '1'),
            6: (),
            57: ('0', ('*1', ('1',))),
            9: (),
            12: (),
            53: ('0', ('*1', (('*1', ('?',)), '2'))),
            13: ('*0', '1'),
            54: ('*0',),
            16: ('*0', '1'),
            17: (),
            61: ('1', ('*2', ('1',))),
            21: (),
            24: (),
            64: (('*0', ('?',)), '1', ('*2', ('?',))),
            27: (),
            59: ('0', ('*1', ('?',))),
            71: ('0',),
            30: (),
            51: ('1', ('*3', ('?',))),
            52: ('1',),
            31: ('*0', '1'),
            35: ('*0', '1'),
            68: ('*0',),
            69: ('0', ('*1', ('1',)))
        }
        self.__reduce_symbol_sum = [2, 1, 1, 1, 2, 2, 0, 1, 1, 0, 3, 1, 0, 2, 1, 2, 2, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 2, 1, 2, 1, 2, 1, 2, 1, 1, 0, 4, 1, 0, 2, 2, 0, 1, 1, 1, 3, 4, 3, 2, 1, 1, 0, 2, 1, 2, 4, 4, 2, 6, 3, 1, 1, 1, 1, 2, 1, 1]
        self.__reduce_to_non_terminal_index = [4, 4, 6, 6, 34, 1, 1, 5, 44, 44, 46, 23, 23, 3, 3, 37, 8, 8, 45, 13, 7, 7, 43, 29, 29, 40, 36, 36, 25, 30, 30, 38, 38, 16, 42, 42, 31, 31, 21, 15, 15, 20, 35, 35, 11, 9, 9, 39, 32, 32, 18, 14, 14, 33, 26, 26, 26, 17, 27, 27, 10, 24, 12, 0, 19, 28, 28, 28, 2, 2, 41, 41]

    def __generate_grammar_tuple(self, statement_index: int, node_tuple: tuple, symbol_package: list) -> BosonGrammarNode:
        grammar_node = BosonGrammarNode()
        for i in node_tuple:
            if isinstance(i, str):
                if i == '$':
                    grammar_node.append(statement_index)
                elif i == '?':
                    grammar_node += symbol_package
                else:
                    if symbol_package:
                        if i[0] == '*':
                            grammar_node += symbol_package[int(i[1:])]
                        else:
                            grammar_node.append(symbol_package[int(i)])
            else:
                if symbol_package:
                    if i[0][0] == '*':
                        for node in symbol_package[int(i[0][1:])]:
                            grammar_node += self.__generate_grammar_tuple(-1, i[1], node)
                    else:
                        for node in symbol_package[int(i[0])]:
                            grammar_node.append(self.__generate_grammar_tuple(-1, i[1], node))
        grammar_node.reduce_number = statement_index
        return grammar_node

    def grammar_analysis(self, token_list: list) -> BosonGrammar:
        grammar = BosonGrammar()
        analysis_stack = [0]
        symbol_stack = []
        token_index = 0
        while token_index < len(token_list):
            token = token_list[token_index]
            current_state = analysis_stack[-1]
            operation = self.__action_table.get(current_state, {}).get(self.__terminal_index[token.symbol], 'e')
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
                reduce_sum = self.__reduce_symbol_sum[statement_index]
                for _ in range(reduce_sum):
                    analysis_stack.pop()
                current_state = analysis_stack[-1]
                current_non_terminal_index = self.__reduce_to_non_terminal_index[statement_index]
                goto_next_state = self.__goto_table.get(current_state, {}).get(current_non_terminal_index, -1)
                if goto_next_state == -1:
                    raise ValueError('Invalid goto action: state={}, non-terminal={}'.format(current_state, current_non_terminal_index))
                analysis_stack.append(goto_next_state)
                if statement_index in self.__node_table:
                    symbol_package = []
                    for _ in range(reduce_sum):
                        symbol_package.insert(0, symbol_stack.pop())
                    symbol_stack.append(self.__generate_grammar_tuple(statement_index, self.__node_table[statement_index], symbol_package))
                elif statement_index in [1, 2, 3, 4, 7, 8, 10, 11, 14, 15, 18, 19, 20, 22, 23, 25, 26, 28, 29, 32, 33, 34, 36, 38, 39, 41, 42, 44, 47, 48, 49, 55, 56, 58, 65, 66, 67, 70]:
                    grammar_node = BosonGrammarNode()
                    for _ in range(reduce_sum):
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
        self.__reduce_number_to_grammar_name = {
            50: 'command',
            63: 'lexical_define',
            60: 'reduce',
            64: 'grammar_node',
            59: 'name_closure',
            71: 'literal',
            51: 'complex_closure',
            52: 'complex_optional',
            69: 'select'
        }
        self.__reduce_number_to_grammar_number = {
            47: 0,
            65: 1,
            67: 2,
            66: 3,
            62: 6,
            57: 8,
            53: 9,
            54: 10,
            55: 11,
            56: 12,
            61: 13,
            58: 15,
            70: 17,
            68: 21,
            49: 23,
            48: 24
        }
        self.__naive_reduce_number = {65, 2, 66, 3, 67, 70, 71, 48, 49, 55, 56, 58}
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
        if grammar_tree.reduce_number in self.__reduce_number_to_grammar_name:
            grammar_name = self.__reduce_number_to_grammar_name[grammar_tree.reduce_number]
        elif grammar_tree.reduce_number in self.__reduce_number_to_grammar_number:
            grammar_name = '!grammar_{}'.format(self.__reduce_number_to_grammar_number[grammar_tree.reduce_number])
        else:
            grammar_name = '!grammar_hidden'
        grammar_entity = list(map(lambda g: self.__semantics_analysis(g) if isinstance(g, BosonGrammarNode) else g, grammar_tree.data()))
        if grammar_name in self.__semantics_entity:
            return self.__semantics_entity[grammar_name](grammar_entity)
        elif grammar_tree.reduce_number in self.__naive_reduce_number:
            return self.__naive_semantics_entity(grammar_entity)
        else:
            return self.__default_semantics_entity(grammar_entity)

    def semantics_analysis(self, grammar_tree: BosonGrammarNode):
        return self.__semantics_analysis(grammar_tree)

    def semantics_entity(self, sign: (int, str)) -> callable:
        def decorator(f: callable):
            if isinstance(sign, int):
                name = '!grammar_{}'.format(sign)
            elif isinstance(sign, str):
                name = sign
            else:
                raise ValueError('Invalid grammar sign: {}'.format(sign))
            self.__semantics_entity[name] = f
            return f
        return decorator
