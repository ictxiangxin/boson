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
                [2, {'\r', '\n'}, [], 2]
            ],
            27: [
                [2, {'\\'}, [], 26],
                [0, {'\\'}, [], 27]
            ],
            26: [
                [2, {'>', '\\'}, [], 26],
                [0, {'>'}, [], 28],
                [0, {'\\'}, [], 27]
            ],
            28: [
                [2, {'>', '\\'}, [], 26],
                [0, {'>'}, [], 28],
                [0, {'\\'}, [], 27]
            ],
            30: [
                [2, {'\\'}, [], 29],
                [0, {'\\'}, [], 30]
            ],
            29: [
                [2, {"'", '\\'}, [], 29],
                [0, {'\\'}, [], 30],
                [0, {"'"}, [], 31]
            ],
            31: [
                [2, {"'", '\\'}, [], 29],
                [0, {'\\'}, [], 30],
                [0, {"'"}, [], 31]
            ],
            33: [
                [2, {'\\'}, [], 32],
                [0, {'\\'}, [], 33]
            ],
            32: [
                [0, {'"'}, [], 34],
                [2, {'"', '\\'}, [], 32],
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
        self.__character_set = {'u', 'F', '5', 'Q', 'z', 'k', '%', 'w', '!', '3', '1', 'N', '9', '\t', ';', 'v', 'J', 't', 'p', '+', '$', '0', '@', '>', '|', 'b', 'c', '8', 'h', '"', '\n', 'o', '*', '2', 'E', 'f', 'g', 'U', ']', '}', 'n', 'Z', 'M', '\\', '#', ':', 's', 'O', ' ', '~', 'P', 'V', 'H', '7', '=', 'l', 'q', "'", 'a', 'D', '(', 'R', 'e', '_', 'A', '[', 'C', 'Y', 'X', 'm', 'W', '6', 'L', 'd', ')', ',', 'B', 'x', 'K', 'i', 'T', 'G', '4', 'r', '\r', 'y', '{', 'I', 'S', 'j', '<'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 28, 31, 34}
        self.__lexical_symbol_mapping = {
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
        self.__non_greedy_state_set = {34, 28, 31}
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


class BosonGrammarAnalyzer:
    def __init__(self):
        self.__terminal_index_mapping = {
            '!symbol_12': 0,
            '!symbol_9': 1,
            'name': 2,
            'command': 3,
            '!symbol_1': 4,
            '!symbol_14': 5,
            '!symbol_2': 6,
            '!symbol_7': 7,
            'regular': 8,
            '!symbol_13': 9,
            '!symbol_10': 10,
            'string': 11,
            'node': 12,
            '!symbol_3': 13,
            '!symbol_6': 14,
            '!symbol_4': 15,
            '!symbol_15': 16,
            '!symbol_11': 17,
            '!symbol_8': 18,
            '!symbol_16': 19,
            '$': 20,
            '!symbol_5': 21
        }
        self.__sparse_action_table = {
            0: {2: 's6', 3: 's7', 20: 'a'},
            1: {2: 's6', 3: 's7', 20: 'r68'},
            2: {2: 'r59', 3: 'r59', 20: 'r59'},
            3: {2: 'r8', 3: 'r8', 20: 'r8'},
            4: {2: 'r19', 3: 'r19', 20: 'r19'},
            5: {2: 'r74', 3: 'r74', 20: 'r74'},
            6: {6: 's16', 18: 's15'},
            7: {2: 's12', 11: 's8'},
            8: {2: 'r69', 4: 'r69', 11: 'r69'},
            9: {2: 's12', 4: 's13', 11: 's8'},
            10: {2: 'r20', 4: 'r20', 11: 'r20'},
            11: {2: 'r72', 4: 'r72', 11: 'r72'},
            12: {2: 'r1', 4: 'r1', 11: 'r1'},
            13: {2: 'r15', 3: 'r15', 20: 'r15'},
            14: {2: 'r26', 4: 'r26', 11: 'r26'},
            15: {1: 'r54', 2: 's38', 4: 'r54', 5: 's40', 6: 'r54', 10: 's33', 11: 's39', 17: 's41'},
            16: {8: 's17'},
            17: {4: 'r2', 13: 's20', 15: 'r2'},
            18: {4: 'r17', 15: 's21'},
            19: {4: 'r35', 15: 'r35'},
            20: {4: 'r49', 15: 'r49'},
            21: {21: 's25'},
            22: {4: 's24'},
            23: {4: 'r11'},
            24: {2: 'r48', 3: 'r48', 20: 'r48'},
            25: {2: 's27'},
            26: {14: 's32'},
            27: {7: 'r64', 14: 'r64'},
            28: {7: 's29', 14: 'r56'},
            29: {2: 's31'},
            30: {7: 'r25', 14: 'r25'},
            31: {7: 'r60', 14: 'r60'},
            32: {4: 'r27'},
            33: {1: 'r10', 4: 'r10', 6: 'r10'},
            34: {1: 'r34', 2: 's38', 4: 'r34', 5: 's40', 6: 'r34', 11: 's39', 17: 's41'},
            35: {1: 'r53', 2: 'r53', 4: 'r53', 5: 'r53', 6: 'r53', 11: 'r53', 17: 'r53'},
            36: {0: 'r12', 1: 'r12', 2: 'r12', 4: 'r12', 5: 'r12', 6: 'r12', 11: 'r12', 16: 'r12', 17: 'r12'},
            37: {0: 'r73', 1: 'r73', 2: 'r73', 4: 'r73', 5: 'r73', 6: 'r73', 9: 's87', 11: 'r73', 16: 'r73', 17: 'r73', 19: 's85'},
            38: {0: 'r38', 1: 'r38', 2: 'r38', 4: 'r38', 5: 'r38', 6: 'r38', 9: 'r38', 11: 'r38', 16: 'r38', 17: 'r38', 19: 'r38'},
            39: {0: 'r55', 1: 'r55', 2: 'r55', 4: 'r55', 5: 'r55', 6: 'r55', 9: 'r55', 11: 'r55', 16: 'r55', 17: 'r55', 19: 'r55'},
            40: {2: 's38', 5: 's40', 11: 's39', 17: 's41'},
            41: {2: 's38', 5: 's40', 11: 's39', 17: 's41'},
            42: {4: 's73'},
            43: {1: 'r14', 4: 'r14'},
            44: {1: 'r50', 4: 'r50', 6: 's46'},
            45: {1: 'r45', 4: 'r45'},
            46: {2: 's50', 17: 'r32'},
            47: {1: 'r52', 4: 'r52'},
            48: {17: 's52'},
            49: {17: 'r66'},
            50: {17: 'r33'},
            51: {1: 'r31', 4: 'r31'},
            52: {9: 's55', 12: 'r75'},
            53: {12: 's62'},
            54: {12: 'r9'},
            55: {12: 'r67'},
            56: {0: 'r23', 7: 'r23'},
            57: {0: 's59', 7: 's58'},
            58: {9: 's55', 12: 'r75'},
            59: {0: 'r18', 1: 'r18', 4: 'r18', 7: 'r18'},
            60: {0: 'r40', 7: 'r40'},
            61: {0: 'r63', 7: 'r63'},
            62: {0: 'r71', 7: 'r71', 9: 's67', 17: 'r57'},
            63: {0: 'r58', 7: 'r58'},
            64: {0: 'r41', 7: 'r41'},
            65: {17: 's52'},
            66: {17: 'r62'},
            67: {17: 'r36'},
            68: {0: 'r4', 7: 'r4'},
            69: {1: 's71', 4: 'r30'},
            70: {1: 'r29', 4: 'r29'},
            71: {1: 'r54', 2: 's38', 4: 'r54', 5: 's40', 6: 'r54', 10: 's33', 11: 's39', 17: 's41'},
            72: {1: 'r5', 4: 'r5'},
            73: {2: 'r3', 3: 'r3', 20: 'r3'},
            74: {0: 's83'},
            75: {0: 'r22', 2: 's38', 5: 's40', 11: 's39', 16: 'r22', 17: 's41'},
            76: {0: 'r7', 1: 's77', 2: 'r7', 5: 'r7', 11: 'r7', 16: 'r7', 17: 'r7'},
            77: {2: 's38', 5: 's40', 11: 's39', 17: 's41'},
            78: {0: 'r65', 1: 's77', 16: 'r65'},
            79: {0: 'r47', 1: 'r47', 16: 'r47'},
            80: {0: 'r70', 1: 'r70', 16: 'r70'},
            81: {0: 'r61', 1: 'r61', 16: 'r61'},
            82: {0: 'r44', 2: 'r44', 5: 'r44', 11: 'r44', 16: 'r44', 17: 'r44'},
            83: {0: 'r37', 1: 'r37', 2: 'r37', 4: 'r37', 5: 'r37', 6: 'r37', 9: 's87', 11: 'r37', 16: 'r37', 17: 'r37', 19: 's85'},
            84: {0: 'r24', 1: 'r24', 2: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 11: 'r24', 16: 'r24', 17: 'r24'},
            85: {0: 'r6', 1: 'r6', 2: 'r6', 4: 'r6', 5: 'r6', 6: 'r6', 11: 'r6', 16: 'r6', 17: 'r6'},
            86: {0: 'r51', 1: 'r51', 2: 'r51', 4: 'r51', 5: 'r51', 6: 'r51', 11: 'r51', 16: 'r51', 17: 'r51'},
            87: {0: 'r28', 1: 'r28', 2: 'r28', 4: 'r28', 5: 'r28', 6: 'r28', 11: 'r28', 16: 'r28', 17: 'r28'},
            88: {0: 'r16', 1: 'r16', 2: 'r16', 4: 'r16', 5: 'r16', 6: 'r16', 11: 'r16', 16: 'r16', 17: 'r16'},
            89: {16: 's90'},
            90: {0: 'r13', 1: 'r13', 2: 'r13', 4: 'r13', 5: 'r13', 6: 'r13', 11: 'r13', 16: 'r13', 17: 'r13'},
            91: {0: 'r43', 1: 'r43', 2: 'r43', 4: 'r43', 5: 'r43', 6: 'r43', 11: 'r43', 16: 'r43', 17: 'r43'},
            92: {0: 'r21', 1: 'r21', 2: 'r21', 4: 'r21', 5: 'r21', 6: 'r21', 11: 'r21', 16: 'r21', 17: 'r21'},
            93: {0: 'r42', 1: 'r42', 2: 'r42', 4: 'r42', 5: 'r42', 6: 'r42', 11: 'r42', 16: 'r42', 17: 'r42'},
            94: {1: 'r46', 2: 'r46', 4: 'r46', 5: 'r46', 6: 'r46', 11: 'r46', 17: 'r46'},
            95: {2: 'r39', 3: 'r39', 20: 'r39'}
        }
        self.__sparse_goto_table = {
            0: {0: 4, 2: 0, 12: 5, 20: 2, 21: 1, 29: 3},
            1: {0: 4, 12: 5, 20: 95, 29: 3},
            7: {13: 9, 39: 11, 46: 10},
            9: {39: 11, 46: 14},
            15: {4: 35, 5: 42, 25: 43, 28: 37, 36: 44, 42: 34, 44: 36},
            17: {10: 18, 27: 19},
            18: {22: 23, 23: 22},
            25: {31: 26},
            27: {1: 28},
            28: {43: 30},
            34: {4: 94, 28: 37, 44: 36},
            37: {3: 93, 32: 91, 40: 92},
            40: {4: 76, 11: 89, 28: 37, 34: 75, 44: 36},
            41: {4: 76, 11: 74, 28: 37, 34: 75, 44: 36},
            43: {15: 69},
            44: {41: 47, 45: 45},
            46: {30: 49, 33: 48},
            48: {14: 51},
            52: {9: 54, 19: 56, 26: 53},
            56: {47: 57},
            57: {38: 60},
            58: {9: 54, 19: 61, 26: 53},
            62: {6: 63, 16: 65, 18: 64, 37: 66},
            65: {14: 68},
            69: {35: 70},
            71: {4: 35, 25: 72, 28: 37, 36: 44, 42: 34, 44: 36},
            75: {4: 82, 28: 37, 44: 36},
            76: {7: 79, 48: 78},
            77: {4: 81, 28: 37, 44: 36},
            78: {7: 80},
            83: {3: 84, 8: 86, 17: 88}
        }
        self.__sentence_index_grammar_tuple_mapping = {
            65: ('0', '*1'),
            61: ('1',),
            22: ('*0',),
            70: ('*0', '*1'),
            44: ('*0', '1'),
            13: ('1',),
            51: ('1', '*3'),
            37: (),
            16: ('*0',),
            55: ('0',),
            43: ('0', '*1'),
            73: (),
            21: ('*0',),
            58: ('*0', '1', '*2'),
            4: ('*0', '1'),
            71: (),
            41: ('*0',),
            57: (),
            62: ('*0',),
            75: (),
            9: ('*0',),
            18: ('1', '*2'),
            63: ('1',),
            23: (),
            40: ('*0', '*1'),
            34: ('*0',),
            46: ('*0', '1'),
            45: ('0', '*1'),
            31: ('*1', '2'),
            50: (),
            52: ('*0',),
            32: (),
            66: ('*0',),
            30: ('0', '*1'),
            5: ('1',),
            14: (),
            29: ('*0', '*1'),
            3: ('0', '2'),
            56: ('0', '*1'),
            60: ('1',),
            64: (),
            25: ('*0', '*1'),
            48: ('0', '2', '*3', '4'),
            27: ('*2',),
            17: (),
            11: ('*0',),
            2: (),
            35: ('*0',),
            15: ('0', '*1'),
            26: ('*0', '1'),
            39: ('*0', '1'),
            47: ('*0',)
        }
        self.__reduce_symbol_count = [1, 1, 0, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1, 3, 0, 3, 1, 0, 4, 1, 1, 1, 1, 0, 1, 2, 2, 4, 1, 2, 2, 3, 0, 1, 1, 1, 1, 0, 1, 2, 2, 1, 1, 2, 2, 2, 2, 1, 6, 1, 0, 4, 1, 1, 0, 1, 2, 0, 3, 1, 2, 2, 1, 2, 0, 2, 1, 1, 1, 1, 2, 0, 1, 0, 1, 0]
        self.__reduce_non_terminal_index = [24, 39, 10, 0, 18, 35, 3, 34, 20, 26, 36, 23, 4, 44, 15, 29, 8, 23, 14, 20, 13, 32, 11, 47, 17, 1, 13, 22, 3, 15, 5, 41, 33, 30, 36, 10, 37, 8, 28, 21, 47, 6, 40, 4, 34, 25, 42, 48, 12, 27, 45, 44, 45, 42, 36, 28, 31, 16, 19, 21, 43, 7, 16, 38, 1, 11, 33, 9, 2, 39, 48, 6, 46, 32, 20, 26]

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
                elif statement_index in {0, 1, 6, 7, 8, 10, 12, 19, 20, 24, 28, 33, 36, 38, 42, 49, 53, 54, 59, 67, 68, 69, 72, 74}:
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
            15: 'command',
            48: 'lexical_define',
            3: 'reduce',
            58: 'grammar_node',
            43: 'name_closure',
            55: 'literal',
            51: 'complex_closure',
            13: 'complex_optional',
            65: 'select'
        }
        self.__naive_reduce_number_set = {1, 69, 38, 6, 8, 74, 10, 12, 19, 54, 55, 28}
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
