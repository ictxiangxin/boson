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
                [0, {' ', '\t'}, [], 23],
                [0, {'*'}, [], 2],
                [0, {'\n'}, [], 3],
                [0, {')'}, [], 4],
                [0, {'$'}, [], 5],
                [0, {'"'}, [], 6],
                [0, {'('}, [], 7],
                [0, {'%'}, [], 8],
                [0, {':'}, [], 9],
                [0, {'@'}, [], 10],
                [0, {'['}, [], 11],
                [0, {'{'}, [], 12],
                [0, {','}, [], 13],
                [0, {'}'}, [], 14],
                [0, {';'}, [], 15],
                [0, {'|'}, [], 16],
                [0, {'+'}, [], 17],
                [0, {'~'}, [], 18],
                [0, {']'}, [], 19],
                [0, {'#'}, [], 20],
                [0, {'!'}, [], 21],
                [0, {"'"}, [], 22],
                [0, {'<'}, [], 24],
                [0, {'='}, [], 25]
            ],
            24: [
                [2, {'\\'}, [], 26],
                [0, {'\\'}, [], 24]
            ],
            26: [
                [2, {'\\', '>'}, [], 26],
                [0, {'\\'}, [], 24],
                [0, {'>'}, [], 27]
            ],
            27: [
                [2, {'\\', '>'}, [], 26],
                [0, {'\\'}, [], 24],
                [0, {'>'}, [], 27]
            ],
            23: [
                [0, {' ', '\t'}, [], 23]
            ],
            22: [
                [2, {'\\'}, [], 28],
                [0, {'\\'}, [], 22]
            ],
            28: [
                [2, {'\\', "'"}, [], 28],
                [0, {'\\'}, [], 22],
                [0, {"'"}, [], 29]
            ],
            29: [
                [2, {'\\', "'"}, [], 28],
                [0, {'\\'}, [], 22],
                [0, {"'"}, [], 29]
            ],
            20: [
                [2, {'\r', '\n'}, [], 20]
            ],
            8: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 30]
            ],
            30: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 30]
            ],
            6: [
                [2, {'\\'}, [], 31],
                [0, {'\\'}, [], 6]
            ],
            31: [
                [2, {'"', '\\'}, [], 31],
                [0, {'"'}, [], 32],
                [0, {'\\'}, [], 6]
            ],
            32: [
                [2, {'"', '\\'}, [], 31],
                [0, {'"'}, [], 32],
                [0, {'\\'}, [], 6]
            ],
            5: [
                [0, {'@', '?', '$'}, [], 34],
                [0, set(), [('0', '9')], 33]
            ],
            33: [
                [0, set(), [('0', '9')], 33]
            ],
            3: [
                [0, {'\r'}, [], 35]
            ],
            1: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 1]
            ]
        }
        self.__character_set = {'U', 'I', '_', ' ', '*', '6', 'j', 'W', '\n', 'k', 'g', 'L', 'P', '4', 'Q', ')', 'p', '$', 'h', 'N', '"', 'n', 'H', 'a', '2', '?', '(', '\\', 'o', '%', 'i', 'C', ':', 'D', '@', 'K', '[', 'c', 'l', 'q', '{', 'y', ',', 'T', '1', 's', '8', '}', 'm', '5', 'R', 'd', '7', ';', 'M', '>', '|', 'S', 'V', 'e', 'v', '3', 'u', '+', 't', '~', 'G', ']', '0', '#', 'Y', 'x', 'B', 'r', 'A', 'X', 'O', 'f', 'J', 'E', 'w', '!', 'z', '\r', "'", 'F', '\t', '9', 'b', 'Z', '<', '='}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 3, 4, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 25, 27, 29, 30, 32, 33, 34, 35}
        self.__lexical_symbol_mapping = {
            1: 'name',
            2: '!symbol_13',
            3: 'newline',
            4: '!symbol_12',
            7: '!symbol_11',
            9: '!symbol_8',
            10: '!symbol_4',
            11: '!symbol_14',
            12: '!symbol_5',
            13: '!symbol_7',
            14: '!symbol_6',
            15: '!symbol_1',
            16: '!symbol_9',
            17: '!symbol_16',
            18: '!symbol_10',
            19: '!symbol_15',
            20: 'comment',
            21: '!symbol_3',
            23: 'skip',
            25: '!symbol_2',
            27: 'regular',
            29: 'string',
            30: 'command',
            32: 'string',
            33: 'node',
            34: 'node',
            35: 'newline'
        }
        self.__non_greedy_state_set = {32, 27, 29}
        self.__symbol_function_mapping = {
            'comment': ['skip'],
            'skip': ['skip'],
            'newline': ['skip', 'newline']
        }
        self.__lexical_function = {}

    def _invoke_lexical_function(self, symbol: str, token_string: str):
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

    def _generate_token(self, state: int, token_string: str):
        symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
        token_string = self._invoke_lexical_function(symbol, token_string)
        if not self.__skip:
            self.__token_list.append(LexicalToken(token_string, self.__line, symbol))

    def skip(self):
        self.__skip = True

    def newline(self):
        self.__line += 1

    def token_list(self):
        return self.__token_list

    def error_line(self):
        return self.__error_line

    def no_error_line(self):
        return self.__no_error_line

    def tokenize(self, text: str):
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
            '!symbol_5': 0,
            '!symbol_15': 1,
            '!symbol_4': 2,
            '!symbol_6': 3,
            '!symbol_8': 4,
            'command': 5,
            '!symbol_10': 6,
            '!symbol_9': 7,
            'node': 8,
            '!symbol_2': 9,
            '!symbol_3': 10,
            'string': 11,
            'regular': 12,
            '!symbol_13': 13,
            '!symbol_16': 14,
            '!symbol_12': 15,
            '$': 16,
            '!symbol_14': 17,
            'name': 18,
            '!symbol_1': 19,
            '!symbol_11': 20,
            '!symbol_7': 21
        }
        self.__action_table = {
            0: {5: 's7', 18: 's3'},
            1: {5: 'r68', 16: 'r68', 18: 'r68'},
            2: {5: 'r2', 16: 'r2', 18: 'r2'},
            3: {4: 's9', 9: 's10'},
            4: {5: 's7', 16: 'r48', 18: 's3'},
            5: {5: 'r67', 16: 'r67', 18: 'r67'},
            6: {16: 'a'},
            7: {11: 's14', 18: 's16'},
            8: {5: 'r69', 16: 'r69', 18: 'r69'},
            9: {6: 's19', 7: 'r57', 9: 'r57', 11: 's27', 17: 's28', 18: 's18', 19: 'r57', 20: 's24'},
            10: {12: 's29'},
            11: {5: 'r1', 16: 'r1', 18: 'r1'},
            12: {11: 'r20', 18: 'r20', 19: 'r20'},
            13: {11: 'r37', 18: 'r37', 19: 'r37'},
            14: {11: 'r4', 18: 'r4', 19: 'r4'},
            15: {11: 's14', 18: 's16', 19: 's32'},
            16: {11: 'r3', 18: 'r3', 19: 'r3'},
            17: {7: 'r7', 19: 'r7'},
            18: {1: 'r72', 7: 'r72', 9: 'r72', 11: 'r72', 13: 'r72', 14: 'r72', 15: 'r72', 17: 'r72', 18: 'r72', 19: 'r72', 20: 'r72'},
            19: {7: 'r56', 9: 'r56', 19: 'r56'},
            20: {7: 'r13', 9: 's34', 19: 'r13'},
            21: {1: 'r59', 7: 'r59', 9: 'r59', 11: 'r59', 15: 'r59', 17: 'r59', 18: 'r59', 19: 'r59', 20: 'r59'},
            22: {7: 'r15', 9: 'r15', 11: 'r15', 17: 'r15', 18: 'r15', 19: 'r15', 20: 'r15'},
            23: {19: 's37'},
            24: {11: 's27', 17: 's28', 18: 's18', 20: 's24'},
            25: {7: 'r55', 9: 'r55', 11: 's27', 17: 's28', 18: 's18', 19: 'r55', 20: 's24'},
            26: {1: 'r28', 7: 'r28', 9: 'r28', 11: 'r28', 13: 's44', 14: 's43', 15: 'r28', 17: 'r28', 18: 'r28', 19: 'r28', 20: 'r28'},
            27: {1: 'r73', 7: 'r73', 9: 'r73', 11: 'r73', 13: 'r73', 14: 'r73', 15: 'r73', 17: 'r73', 18: 'r73', 19: 'r73', 20: 'r73'},
            28: {11: 's27', 17: 's28', 18: 's18', 20: 's24'},
            29: {2: 'r41', 10: 's50', 19: 'r41'},
            30: {19: 's51'},
            31: {11: 'r38', 18: 'r38', 19: 'r38'},
            32: {5: 'r51', 16: 'r51', 18: 'r51'},
            33: {7: 's53', 19: 'r58'},
            34: {18: 's56', 20: 'r10'},
            35: {7: 'r54', 19: 'r54'},
            36: {7: 'r12', 19: 'r12'},
            37: {5: 'r61', 16: 'r61', 18: 'r61'},
            38: {1: 'r33', 7: 's59', 11: 'r33', 15: 'r33', 17: 'r33', 18: 'r33', 20: 'r33'},
            39: {1: 'r70', 11: 's27', 15: 'r70', 17: 's28', 18: 's18', 20: 's24'},
            40: {15: 's61'},
            41: {7: 'r14', 9: 'r14', 11: 'r14', 17: 'r14', 18: 'r14', 19: 'r14', 20: 'r14'},
            42: {1: 'r26', 7: 'r26', 9: 'r26', 11: 'r26', 15: 'r26', 17: 'r26', 18: 'r26', 19: 'r26', 20: 'r26'},
            43: {1: 'r50', 7: 'r50', 9: 'r50', 11: 'r50', 15: 'r50', 17: 'r50', 18: 'r50', 19: 'r50', 20: 'r50'},
            44: {1: 'r49', 7: 'r49', 9: 'r49', 11: 'r49', 15: 'r49', 17: 'r49', 18: 'r49', 19: 'r49', 20: 'r49'},
            45: {1: 'r27', 7: 'r27', 9: 'r27', 11: 'r27', 15: 'r27', 17: 'r27', 18: 'r27', 19: 'r27', 20: 'r27'},
            46: {1: 'r60', 7: 'r60', 9: 'r60', 11: 'r60', 15: 'r60', 17: 'r60', 18: 'r60', 19: 'r60', 20: 'r60'},
            47: {1: 's62'},
            48: {2: 'r40', 19: 'r40'},
            49: {2: 's64', 19: 'r44'},
            50: {2: 'r39', 19: 'r39'},
            51: {5: 'r65', 16: 'r65', 18: 'r65'},
            52: {7: 'r6', 19: 'r6'},
            53: {6: 's19', 7: 'r57', 9: 'r57', 11: 's27', 17: 's28', 18: 's18', 19: 'r57', 20: 's24'},
            54: {20: 'r9'},
            55: {20: 's67'},
            56: {20: 'r8'},
            57: {1: 'r71', 7: 's59', 15: 'r71'},
            58: {1: 'r35', 7: 'r35', 15: 'r35'},
            59: {11: 's27', 17: 's28', 18: 's18', 20: 's24'},
            60: {1: 'r32', 11: 'r32', 15: 'r32', 17: 'r32', 18: 'r32', 20: 'r32'},
            61: {1: 'r31', 7: 'r31', 9: 'r31', 11: 'r31', 13: 's44', 14: 's43', 15: 'r31', 17: 'r31', 18: 'r31', 19: 'r31', 20: 'r31'},
            62: {1: 'r53', 7: 'r53', 9: 'r53', 11: 'r53', 15: 'r53', 17: 'r53', 18: 'r53', 19: 'r53', 20: 'r53'},
            63: {19: 'r63'},
            64: {0: 's74'},
            65: {19: 'r43'},
            66: {7: 'r5', 19: 'r5'},
            67: {8: 'r22', 13: 's75'},
            68: {7: 'r11', 19: 'r11'},
            69: {1: 'r36', 7: 'r36', 15: 'r36'},
            70: {1: 'r34', 7: 'r34', 15: 'r34'},
            71: {1: 'r29', 7: 'r29', 9: 'r29', 11: 'r29', 15: 'r29', 17: 'r29', 18: 'r29', 19: 'r29', 20: 'r29'},
            72: {1: 'r52', 7: 'r52', 9: 'r52', 11: 'r52', 15: 'r52', 17: 'r52', 18: 'r52', 19: 'r52', 20: 'r52'},
            73: {1: 'r30', 7: 'r30', 9: 'r30', 11: 'r30', 15: 'r30', 17: 'r30', 18: 'r30', 19: 'r30', 20: 'r30'},
            74: {18: 's79'},
            75: {8: 'r19'},
            76: {15: 'r18', 21: 'r18'},
            77: {8: 's82'},
            78: {8: 'r21'},
            79: {3: 'r47', 21: 'r47'},
            80: {3: 's84'},
            81: {15: 's87', 21: 's86'},
            82: {7: 'r25', 15: 'r25', 19: 'r25', 20: 's67', 21: 'r25'},
            83: {3: 'r64', 21: 's92'},
            84: {19: 'r42'},
            85: {15: 'r17', 21: 'r17'},
            86: {8: 'r22', 13: 's75'},
            87: {7: 'r62', 15: 'r62', 19: 'r62', 21: 'r62'},
            88: {7: 'r24', 15: 'r24', 19: 'r24', 21: 'r24'},
            89: {7: 'r23', 15: 'r23', 19: 'r23', 21: 'r23'},
            90: {7: 'r66', 15: 'r66', 19: 'r66', 21: 'r66'},
            91: {3: 'r46', 21: 'r46'},
            92: {18: 's94'},
            93: {15: 'r16', 21: 'r16'},
            94: {3: 'r45', 21: 'r45'}
        }
        self.__goto_table = {
            0: {16: 6, 23: 8, 29: 5, 36: 4, 37: 2, 44: 1},
            4: {23: 8, 29: 5, 37: 11, 44: 1},
            7: {18: 13, 19: 12, 22: 15},
            9: {2: 17, 5: 22, 6: 21, 7: 25, 39: 23, 45: 26, 46: 20},
            10: {3: 30},
            15: {18: 31, 19: 12},
            17: {43: 33},
            20: {14: 36, 33: 35},
            24: {5: 38, 6: 21, 9: 40, 34: 39, 45: 26},
            25: {5: 41, 6: 21, 45: 26},
            26: {1: 42, 8: 45, 32: 46},
            28: {5: 38, 6: 21, 9: 47, 34: 39, 45: 26},
            29: {17: 48, 38: 49},
            33: {13: 52},
            34: {25: 54, 30: 55},
            38: {28: 57, 41: 58},
            39: {5: 60, 6: 21, 45: 26},
            49: {24: 65, 35: 63},
            53: {2: 66, 5: 22, 6: 21, 7: 25, 45: 26, 46: 20},
            55: {11: 68},
            57: {41: 69},
            59: {5: 70, 6: 21, 45: 26},
            61: {1: 71, 21: 72, 31: 73},
            67: {4: 76, 15: 77, 42: 78},
            74: {26: 80},
            76: {27: 81},
            79: {0: 83},
            81: {12: 85},
            82: {10: 88, 11: 89, 47: 90},
            83: {20: 91},
            86: {4: 93, 15: 77, 42: 78}
        }
        self.__node_table = {
            0: ('*0', '1'),
            37: ('*0', '1'),
            50: ('0', ('*1', ('?',))),
            64: ('0', '2'),
            40: (),
            43: (),
            62: ('0', ('*1', ('?',)), ('2', ('*2',))),
            45: ('*0', '1'),
            46: (),
            63: ('0', ('*1', ('1',))),
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
            65: (('*0', ('?',)), '1', ('*2', ('?',))),
            27: (),
            59: ('0', ('*1', ('?',))),
            72: ('0',),
            30: (),
            51: ('1', ('*3', ('?',))),
            52: ('1',),
            31: ('*0', '1'),
            35: ('*0', '1'),
            69: ('*0',),
            70: ('0', ('*1', ('1',)))
        }
        self.__reduce_symbol_sum = [2, 1, 1, 1, 2, 2, 0, 1, 1, 0, 3, 1, 0, 2, 1, 2, 2, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 2, 1, 2, 1, 2, 1, 2, 1, 1, 0, 4, 1, 0, 2, 2, 0, 1, 1, 1, 3, 4, 3, 2, 1, 1, 0, 2, 1, 2, 4, 4, 3, 2, 4, 3, 1, 1, 1, 1, 2, 1, 1]
        self.__reduce_to_non_terminal_index = [36, 36, 19, 19, 13, 43, 43, 25, 30, 30, 14, 33, 33, 7, 7, 12, 27, 27, 42, 18, 15, 15, 10, 47, 47, 8, 32, 32, 31, 21, 21, 34, 34, 41, 28, 28, 22, 22, 17, 38, 38, 24, 35, 35, 20, 0, 0, 16, 1, 1, 29, 6, 6, 2, 46, 46, 46, 39, 5, 5, 44, 11, 3, 26, 23, 4, 37, 37, 37, 9, 9, 45, 45]

    def __generate_grammar_tuple(self, statement_index: int, node_tuple: tuple, symbol_package: list):
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

    def grammar_analysis(self, token_list):
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
                elif statement_index in [1, 2, 3, 4, 7, 8, 10, 11, 14, 15, 18, 19, 20, 22, 23, 25, 26, 28, 29, 32, 33, 34, 36, 38, 39, 41, 42, 44, 47, 48, 49, 55, 56, 58, 66, 67, 68, 71]:
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
            64: 'lexical_define',
            60: 'reduce',
            65: 'grammar_node',
            59: 'name_closure',
            72: 'literal',
            51: 'complex_closure',
            52: 'complex_optional',
            70: 'select'
        }
        self.__reduce_number_to_grammar_number = {
            47: 0,
            66: 1,
            68: 2,
            67: 3,
            62: 6,
            63: 7,
            57: 9,
            53: 10,
            54: 11,
            55: 12,
            56: 13,
            61: 14,
            58: 16,
            71: 18,
            69: 22,
            49: 24,
            48: 25
        }
        self.__naive_reduce_number = {2, 67, 68, 3, 66, 71, 72, 48, 49, 55, 56, 58}
        self.__semantics_entity = {}

    @staticmethod
    def __default_semantics_entity(grammar_entity):
        return grammar_entity

    @staticmethod
    def __naive_semantics_entity(grammar_entity):
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

    def semantics_entity(self, sign):
        def decorator(f):
            if isinstance(sign, int):
                name = '!grammar_{}'.format(sign)
            elif isinstance(sign, str):
                name = sign
            else:
                raise ValueError('Invalid grammar sign: {}'.format(sign))
            self.__semantics_entity[name] = f
            return f
        return decorator
