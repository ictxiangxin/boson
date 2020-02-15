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
                [0, {"'"}, [], 34],
                [0, {'\n'}, [], 2],
                [0, {'#'}, [], 3],
                [0, {'%'}, [], 4],
                [0, {'('}, [], 5],
                [0, {'$'}, [], 6],
                [0, {')'}, [], 7],
                [0, {'\t', ' '}, [], 9],
                [0, {']'}, [], 8],
                [0, {'{'}, [], 10],
                [0, {'<'}, [], 27],
                [0, {'|'}, [], 11],
                [0, {'['}, [], 12],
                [0, {';'}, [], 13],
                [0, {'!'}, [], 14],
                [0, {':'}, [], 15],
                [0, {'~'}, [], 16],
                [0, {'='}, [], 17],
                [0, {','}, [], 18],
                [0, {'*'}, [], 19],
                [0, {'"'}, [], 20],
                [0, {'+'}, [], 21],
                [0, {'@'}, [], 22],
                [0, {'}'}, [], 23]
            ],
            20: [
                [2, {'\\'}, [], 24],
                [0, {'\\'}, [], 20]
            ],
            24: [
                [2, {'\\', '"'}, [], 24],
                [0, {'\\'}, [], 20],
                [0, {'"'}, [], 25]
            ],
            25: [
                [2, {'\\', '"'}, [], 24],
                [0, {'\\'}, [], 20],
                [0, {'"'}, [], 25]
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
            9: [
                [0, {'\t', ' '}, [], 9]
            ],
            6: [
                [0, set(), [('0', '9')], 29],
                [0, {'@', '?', '$'}, [], 30]
            ],
            29: [
                [0, set(), [('0', '9')], 29]
            ],
            4: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 31]
            ],
            31: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 31]
            ],
            3: [
                [2, {'\r', '\n'}, [], 3]
            ],
            2: [
                [0, {'\r'}, [], 32]
            ],
            34: [
                [2, {'\\'}, [], 33],
                [0, {'\\'}, [], 34]
            ],
            33: [
                [0, {"'"}, [], 35],
                [2, {"'", '\\'}, [], 33],
                [0, {'\\'}, [], 34]
            ],
            35: [
                [0, {"'"}, [], 35],
                [2, {"'", '\\'}, [], 33],
                [0, {'\\'}, [], 34]
            ],
            1: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 1]
            ]
        }
        self.__character_set = {'O', "'", '\n', 'E', '#', '9', '_', '%', 'y', '(', 'g', 'c', '$', ')', 'e', '\t', 'x', '2', ']', 'n', ' ', '\\', 'Q', '{', 'h', 'd', 'M', 'u', '<', 'f', 'k', 'F', '|', '0', 'H', 'q', 's', 'j', 'l', 'A', 'v', 'U', '[', 'b', 'Y', '5', '?', ';', '!', ':', 'I', 'N', 'i', '~', '=', '7', '6', ',', '*', '4', 'p', 'r', 'D', '\r', 'W', 'a', 'L', '"', '>', 't', 'P', 'J', 'K', '8', 'R', '+', '@', 'S', 'V', 'w', 'Z', 'o', '1', 'z', 'B', '3', '}', 'T', 'C', 'X', 'm', 'G'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 25, 28, 29, 30, 31, 32, 35}
        self.__lexical_symbol_mapping = {
            1: 'name',
            2: 'newline',
            3: 'comment',
            5: '!symbol_11',
            7: '!symbol_12',
            8: '!symbol_15',
            9: 'skip',
            10: '!symbol_5',
            11: '!symbol_9',
            12: '!symbol_14',
            13: '!symbol_1',
            14: '!symbol_3',
            15: '!symbol_8',
            16: '!symbol_10',
            17: '!symbol_2',
            18: '!symbol_7',
            19: '!symbol_13',
            21: '!symbol_16',
            22: '!symbol_4',
            23: '!symbol_6',
            25: 'string',
            28: 'regular',
            29: 'node',
            30: 'node',
            31: 'command',
            32: 'newline',
            35: 'string'
        }
        self.__non_greedy_state_set = {25, 35, 28}
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
            'string': 0,
            'node': 1,
            '!symbol_12': 2,
            '!symbol_6': 3,
            '!symbol_11': 4,
            '!symbol_16': 5,
            '!symbol_3': 6,
            '!symbol_10': 7,
            'name': 8,
            '!symbol_2': 9,
            '!symbol_14': 10,
            '!symbol_1': 11,
            '!symbol_13': 12,
            '$': 13,
            'command': 14,
            '!symbol_15': 15,
            '!symbol_9': 16,
            '!symbol_8': 17,
            '!symbol_7': 18,
            '!symbol_4': 19,
            '!symbol_5': 20,
            'regular': 21
        }
        self.__action_table = {
            0: {8: 's2', 14: 's8'},
            1: {8: 'r66', 13: 'r66', 14: 'r66'},
            2: {9: 's10', 17: 's9'},
            3: {13: 'a'},
            4: {8: 'r67', 13: 'r67', 14: 'r67'},
            5: {8: 's2', 13: 'r48', 14: 's8'},
            6: {8: 'r68', 13: 'r68', 14: 'r68'},
            7: {8: 'r2', 13: 'r2', 14: 'r2'},
            8: {0: 's12', 8: 's15'},
            9: {0: 's24', 4: 's25', 7: 's21', 8: 's27', 9: 'r57', 10: 's28', 11: 'r57', 16: 'r57'},
            10: {21: 's29'},
            11: {8: 'r1', 13: 'r1', 14: 'r1'},
            12: {0: 'r4', 8: 'r4', 11: 'r4'},
            13: {0: 'r20', 8: 'r20', 11: 'r20'},
            14: {0: 'r37', 8: 'r37', 11: 'r37'},
            15: {0: 'r3', 8: 'r3', 11: 'r3'},
            16: {0: 's12', 8: 's15', 11: 's30'},
            17: {11: 'r7', 16: 'r7'},
            18: {0: 's24', 4: 's25', 8: 's27', 9: 'r55', 10: 's28', 11: 'r55', 16: 'r55'},
            19: {0: 'r15', 4: 'r15', 8: 'r15', 9: 'r15', 10: 'r15', 11: 'r15', 16: 'r15'},
            20: {0: 'r28', 2: 'r28', 4: 'r28', 5: 's36', 8: 'r28', 9: 'r28', 10: 'r28', 11: 'r28', 12: 's35', 15: 'r28', 16: 'r28'},
            21: {9: 'r56', 11: 'r56', 16: 'r56'},
            22: {9: 's41', 11: 'r13', 16: 'r13'},
            23: {0: 'r59', 2: 'r59', 4: 'r59', 8: 'r59', 9: 'r59', 10: 'r59', 11: 'r59', 15: 'r59', 16: 'r59'},
            24: {0: 'r72', 2: 'r72', 4: 'r72', 5: 'r72', 8: 'r72', 9: 'r72', 10: 'r72', 11: 'r72', 12: 'r72', 15: 'r72', 16: 'r72'},
            25: {0: 's24', 4: 's25', 8: 's27', 10: 's28'},
            26: {11: 's45'},
            27: {0: 'r71', 2: 'r71', 4: 'r71', 5: 'r71', 8: 'r71', 9: 'r71', 10: 'r71', 11: 'r71', 12: 'r71', 15: 'r71', 16: 'r71'},
            28: {0: 's24', 4: 's25', 8: 's27', 10: 's28'},
            29: {6: 's49', 8: 'r41', 11: 'r41', 13: 'r41', 14: 'r41', 19: 'r41'},
            30: {8: 'r51', 13: 'r51', 14: 'r51'},
            31: {0: 'r38', 8: 'r38', 11: 'r38'},
            32: {11: 'r58', 16: 's50'},
            33: {0: 'r14', 4: 'r14', 8: 'r14', 9: 'r14', 10: 'r14', 11: 'r14', 16: 'r14'},
            34: {0: 'r26', 2: 'r26', 4: 'r26', 8: 'r26', 9: 'r26', 10: 'r26', 11: 'r26', 15: 'r26', 16: 'r26'},
            35: {0: 'r49', 2: 'r49', 4: 'r49', 8: 'r49', 9: 'r49', 10: 'r49', 11: 'r49', 15: 'r49', 16: 'r49'},
            36: {0: 'r50', 2: 'r50', 4: 'r50', 8: 'r50', 9: 'r50', 10: 'r50', 11: 'r50', 15: 'r50', 16: 'r50'},
            37: {0: 'r60', 2: 'r60', 4: 'r60', 8: 'r60', 9: 'r60', 10: 'r60', 11: 'r60', 15: 'r60', 16: 'r60'},
            38: {0: 'r27', 2: 'r27', 4: 'r27', 8: 'r27', 9: 'r27', 10: 'r27', 11: 'r27', 15: 'r27', 16: 'r27'},
            39: {11: 'r12', 16: 'r12'},
            40: {11: 'r54', 16: 'r54'},
            41: {4: 'r10', 8: 's54'},
            42: {0: 'r33', 2: 'r33', 4: 'r33', 8: 'r33', 10: 'r33', 15: 'r33', 16: 's56'},
            43: {0: 's24', 2: 'r69', 4: 's25', 8: 's27', 10: 's28', 15: 'r69'},
            44: {2: 's59'},
            45: {8: 'r61', 13: 'r61', 14: 'r61'},
            46: {15: 's60'},
            47: {11: 'r44', 19: 's61'},
            48: {8: 'r40', 11: 'r40', 13: 'r40', 14: 'r40', 19: 'r40'},
            49: {8: 'r39', 11: 'r39', 13: 'r39', 14: 'r39', 19: 'r39'},
            50: {0: 's24', 4: 's25', 7: 's21', 8: 's27', 9: 'r57', 10: 's28', 11: 'r57', 16: 'r57'},
            51: {11: 'r6', 16: 'r6'},
            52: {4: 's66'},
            53: {4: 'r9'},
            54: {4: 'r8'},
            55: {2: 'r70', 15: 'r70', 16: 's56'},
            56: {0: 's24', 4: 's25', 8: 's27', 10: 's28'},
            57: {2: 'r35', 15: 'r35', 16: 'r35'},
            58: {0: 'r32', 2: 'r32', 4: 'r32', 8: 'r32', 10: 'r32', 15: 'r32'},
            59: {0: 'r31', 2: 'r31', 4: 'r31', 5: 's36', 8: 'r31', 9: 'r31', 10: 'r31', 11: 'r31', 12: 's35', 15: 'r31', 16: 'r31'},
            60: {0: 'r53', 2: 'r53', 4: 'r53', 8: 'r53', 9: 'r53', 10: 'r53', 11: 'r53', 15: 'r53', 16: 'r53'},
            61: {20: 's72'},
            62: {11: 's73'},
            63: {11: 'r43'},
            64: {11: 'r5', 16: 'r5'},
            65: {11: 'r11', 16: 'r11'},
            66: {1: 'r22', 12: 's74'},
            67: {2: 'r36', 15: 'r36', 16: 'r36'},
            68: {2: 'r34', 15: 'r34', 16: 'r34'},
            69: {0: 'r29', 2: 'r29', 4: 'r29', 8: 'r29', 9: 'r29', 10: 'r29', 11: 'r29', 15: 'r29', 16: 'r29'},
            70: {0: 'r52', 2: 'r52', 4: 'r52', 8: 'r52', 9: 'r52', 10: 'r52', 11: 'r52', 15: 'r52', 16: 'r52'},
            71: {0: 'r30', 2: 'r30', 4: 'r30', 8: 'r30', 9: 'r30', 10: 'r30', 11: 'r30', 15: 'r30', 16: 'r30'},
            72: {8: 's78'},
            73: {8: 'r64', 13: 'r64', 14: 'r64'},
            74: {1: 'r19'},
            75: {2: 'r18', 18: 'r18'},
            76: {1: 's81'},
            77: {1: 'r21'},
            78: {3: 'r47', 18: 'r47'},
            79: {3: 's83'},
            80: {2: 's85', 18: 's86'},
            81: {2: 'r25', 4: 's66', 11: 'r25', 16: 'r25', 18: 'r25'},
            82: {3: 'r63', 18: 's91'},
            83: {11: 'r42'},
            84: {2: 'r17', 18: 'r17'},
            85: {2: 'r62', 11: 'r62', 16: 'r62', 18: 'r62'},
            86: {1: 'r22', 12: 's74'},
            87: {2: 'r23', 11: 'r23', 16: 'r23', 18: 'r23'},
            88: {2: 'r24', 11: 'r24', 16: 'r24', 18: 'r24'},
            89: {2: 'r65', 11: 'r65', 16: 'r65', 18: 'r65'},
            90: {3: 'r46', 18: 'r46'},
            91: {8: 's93'},
            92: {2: 'r16', 18: 'r16'},
            93: {3: 'r45', 18: 'r45'}
        }
        self.__goto_table = {
            0: {0: 4, 4: 6, 25: 7, 33: 1, 36: 5, 39: 3},
            5: {0: 4, 4: 6, 25: 11, 33: 1},
            8: {1: 14, 32: 13, 43: 16},
            9: {10: 19, 11: 22, 14: 17, 15: 26, 26: 23, 27: 20, 31: 18},
            16: {1: 31, 32: 13},
            17: {34: 32},
            18: {10: 33, 26: 23, 27: 20},
            20: {21: 34, 45: 38, 46: 37},
            22: {3: 39, 8: 40},
            25: {10: 42, 26: 23, 27: 20, 40: 43, 44: 44},
            28: {10: 42, 26: 23, 27: 20, 40: 43, 44: 46},
            29: {23: 48, 24: 47},
            32: {42: 51},
            41: {30: 53, 41: 52},
            42: {2: 55, 22: 57},
            43: {10: 58, 26: 23, 27: 20},
            47: {20: 63, 37: 62},
            50: {10: 19, 11: 22, 14: 64, 26: 23, 27: 20, 31: 18},
            52: {38: 65},
            55: {22: 67},
            56: {10: 68, 26: 23, 27: 20},
            59: {5: 71, 17: 70, 21: 69},
            66: {6: 77, 9: 76, 35: 75},
            72: {7: 79},
            75: {29: 80},
            78: {12: 82},
            80: {16: 84},
            81: {19: 88, 28: 89, 38: 87},
            82: {13: 90},
            86: {6: 77, 9: 76, 35: 92}
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
        self.__reduce_to_non_terminal_index = [36, 36, 32, 32, 42, 34, 34, 30, 41, 41, 3, 8, 8, 31, 31, 16, 29, 29, 6, 1, 9, 9, 19, 28, 28, 45, 46, 46, 5, 17, 17, 40, 40, 22, 2, 2, 43, 43, 23, 24, 24, 20, 37, 37, 13, 12, 12, 39, 21, 21, 33, 26, 26, 14, 11, 11, 11, 15, 10, 10, 0, 38, 7, 4, 35, 25, 25, 25, 44, 44, 27, 27]

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
        self.__naive_reduce_number = {65, 2, 3, 67, 66, 70, 71, 48, 49, 55, 56, 58}
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
