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
                [2, {'\\', "'"}, [], 29],
                [0, {'\\'}, [], 30],
                [0, {"'"}, [], 31]
            ],
            31: [
                [2, {'\\', "'"}, [], 29],
                [0, {'\\'}, [], 30],
                [0, {"'"}, [], 31]
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
        self.__character_set = {'c', 'K', 'T', ' ', 'g', ';', 't', 'p', '+', 'b', '@', '5', '~', 'N', 'G', '_', 'u', 'J', '\\', '=', 'C', '\t', 'A', 'F', 'S', 'v', 'D', 'E', 'P', 'O', '\n', ']', 'W', '8', '9', '|', "'", 'w', 'i', '6', 'z', 'Z', 'R', 'o', '!', '1', '}', '"', 'k', ',', 'U', '4', 'a', 'x', 'n', 'V', 'Y', 'y', 'd', 'X', 'f', 'B', 'H', '{', 'I', '<', 'L', '2', '(', '[', 'r', 'j', '>', 'e', 'Q', 'h', '3', ')', 's', '%', '7', ':', '0', '$', '\r', 'M', '#', 'm', 'l', '*', 'q'}
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
            'command': 0,
            '!symbol_12': 1,
            'node': 2,
            'regular': 3,
            '!symbol_8': 4,
            '!symbol_9': 5,
            '!symbol_3': 6,
            'string': 7,
            '!symbol_14': 8,
            '!symbol_13': 9,
            '!symbol_4': 10,
            '!symbol_10': 11,
            '!symbol_11': 12,
            '!symbol_5': 13,
            '$': 14,
            '!symbol_6': 15,
            '!symbol_16': 16,
            '!symbol_1': 17,
            'name': 18,
            '!symbol_2': 19,
            '!symbol_15': 20,
            '!symbol_7': 21
        }
        self.__sparse_action_table = {
            0: {0: 's8', 18: 's7'},
            1: {14: 'a'},
            2: {0: 's8', 14: 'r10', 18: 's7'},
            3: {0: 'r27', 14: 'r27', 18: 'r27'},
            4: {0: 'r2', 14: 'r2', 18: 'r2'},
            5: {0: 'r26', 14: 'r26', 18: 'r26'},
            6: {0: 'r34', 14: 'r34', 18: 'r34'},
            7: {4: 's17', 19: 's16'},
            8: {7: 's11', 18: 's10'},
            9: {7: 'r48', 17: 'r48', 18: 'r48'},
            10: {7: 'r52', 17: 'r52', 18: 'r52'},
            11: {7: 'r58', 17: 'r58', 18: 'r58'},
            12: {7: 's11', 17: 's15', 18: 's10'},
            13: {7: 'r8', 17: 'r8', 18: 'r8'},
            14: {7: 'r6', 17: 'r6', 18: 'r6'},
            15: {0: 'r66', 14: 'r66', 18: 'r66'},
            16: {3: 's80'},
            17: {5: 'r70', 7: 's27', 8: 's29', 11: 's22', 12: 's28', 17: 'r70', 18: 's26', 19: 'r70'},
            18: {17: 's79'},
            19: {5: 'r45', 17: 'r45'},
            20: {5: 'r59', 17: 'r59', 19: 's53'},
            21: {5: 'r65', 7: 's27', 8: 's29', 12: 's28', 17: 'r65', 18: 's26', 19: 'r65'},
            22: {5: 'r68', 17: 'r68', 19: 'r68'},
            23: {5: 'r9', 7: 'r9', 8: 'r9', 12: 'r9', 17: 'r9', 18: 'r9', 19: 'r9'},
            24: {1: 'r42', 5: 'r42', 7: 'r42', 8: 'r42', 12: 'r42', 17: 'r42', 18: 'r42', 19: 'r42', 20: 'r42'},
            25: {1: 'r50', 5: 'r50', 7: 'r50', 8: 'r50', 9: 's42', 12: 'r50', 16: 's43', 17: 'r50', 18: 'r50', 19: 'r50', 20: 'r50'},
            26: {1: 'r47', 5: 'r47', 7: 'r47', 8: 'r47', 9: 'r47', 12: 'r47', 16: 'r47', 17: 'r47', 18: 'r47', 19: 'r47', 20: 'r47'},
            27: {1: 'r55', 5: 'r55', 7: 'r55', 8: 'r55', 9: 'r55', 12: 'r55', 16: 'r55', 17: 'r55', 18: 'r55', 19: 'r55', 20: 'r55'},
            28: {7: 's27', 8: 's29', 12: 's28', 18: 's26'},
            29: {7: 's27', 8: 's29', 12: 's28', 18: 's26'},
            30: {1: 'r5', 7: 's27', 8: 's29', 12: 's28', 18: 's26', 20: 'r5'},
            31: {1: 'r73', 5: 's36', 7: 'r73', 8: 'r73', 12: 'r73', 18: 'r73', 20: 'r73'},
            32: {20: 's33'},
            33: {1: 'r57', 5: 'r57', 7: 'r57', 8: 'r57', 12: 'r57', 17: 'r57', 18: 'r57', 19: 'r57', 20: 'r57'},
            34: {1: 'r18', 5: 's36', 20: 'r18'},
            35: {1: 'r64', 5: 'r64', 20: 'r64'},
            36: {7: 's27', 8: 's29', 12: 's28', 18: 's26'},
            37: {1: 'r15', 5: 'r15', 20: 'r15'},
            38: {1: 'r54', 5: 'r54', 20: 'r54'},
            39: {1: 'r35', 7: 'r35', 8: 'r35', 12: 'r35', 18: 'r35', 20: 'r35'},
            40: {1: 's41'},
            41: {1: 'r24', 5: 'r24', 7: 'r24', 8: 'r24', 9: 's42', 12: 'r24', 16: 's43', 17: 'r24', 18: 'r24', 19: 'r24', 20: 'r24'},
            42: {1: 'r20', 5: 'r20', 7: 'r20', 8: 'r20', 12: 'r20', 17: 'r20', 18: 'r20', 19: 'r20', 20: 'r20'},
            43: {1: 'r56', 5: 'r56', 7: 'r56', 8: 'r56', 12: 'r56', 17: 'r56', 18: 'r56', 19: 'r56', 20: 'r56'},
            44: {1: 'r3', 5: 'r3', 7: 'r3', 8: 'r3', 12: 'r3', 17: 'r3', 18: 'r3', 19: 'r3', 20: 'r3'},
            45: {1: 'r14', 5: 'r14', 7: 'r14', 8: 'r14', 12: 'r14', 17: 'r14', 18: 'r14', 19: 'r14', 20: 'r14'},
            46: {1: 'r63', 5: 'r63', 7: 'r63', 8: 'r63', 12: 'r63', 17: 'r63', 18: 'r63', 19: 'r63', 20: 'r63'},
            47: {1: 'r71', 5: 'r71', 7: 'r71', 8: 'r71', 12: 'r71', 17: 'r71', 18: 'r71', 19: 'r71', 20: 'r71'},
            48: {1: 'r53', 5: 'r53', 7: 'r53', 8: 'r53', 12: 'r53', 17: 'r53', 18: 'r53', 19: 'r53', 20: 'r53'},
            49: {1: 'r17', 5: 'r17', 7: 'r17', 8: 'r17', 12: 'r17', 17: 'r17', 18: 'r17', 19: 'r17', 20: 'r17'},
            50: {5: 'r12', 7: 'r12', 8: 'r12', 12: 'r12', 17: 'r12', 18: 'r12', 19: 'r12'},
            51: {5: 'r39', 17: 'r39'},
            52: {5: 'r25', 17: 'r25'},
            53: {12: 'r46', 18: 's56'},
            54: {12: 's58'},
            55: {12: 'r1'},
            56: {12: 'r61'},
            57: {5: 'r44', 17: 'r44'},
            58: {2: 'r7', 9: 's62'},
            59: {1: 'r49', 21: 'r49'},
            60: {2: 's63'},
            61: {2: 'r21'},
            62: {2: 'r32'},
            63: {1: 'r13', 9: 's67', 12: 'r33', 21: 'r13'},
            64: {1: 'r67', 21: 'r67'},
            65: {12: 's58'},
            66: {12: 'r29'},
            67: {12: 'r69'},
            68: {1: 'r23', 21: 'r23'},
            69: {1: 'r37', 21: 'r37'},
            70: {1: 's71', 21: 's73'},
            71: {1: 'r22', 5: 'r22', 17: 'r22', 21: 'r22'},
            72: {1: 'r41', 21: 'r41'},
            73: {2: 'r7', 9: 's62'},
            74: {1: 'r74', 21: 'r74'},
            75: {5: 's76', 17: 'r11'},
            76: {5: 'r70', 7: 's27', 8: 's29', 11: 's22', 12: 's28', 17: 'r70', 18: 's26', 19: 'r70'},
            77: {5: 'r62', 17: 'r62'},
            78: {5: 'r28', 17: 'r28'},
            79: {0: 'r36', 14: 'r36', 18: 'r36'},
            80: {6: 's83', 10: 'r16', 17: 'r16'},
            81: {10: 's84', 17: 'r40'},
            82: {10: 'r43', 17: 'r43'},
            83: {10: 'r51', 17: 'r51'},
            84: {13: 's88'},
            85: {17: 's87'},
            86: {17: 'r38'},
            87: {0: 'r31', 14: 'r31', 18: 'r31'},
            88: {18: 's89'},
            89: {15: 'r60', 21: 'r60'},
            90: {15: 's91'},
            91: {17: 'r4'},
            92: {15: 'r75', 21: 's93'},
            93: {18: 's95'},
            94: {15: 'r30', 21: 'r30'},
            95: {15: 'r19', 21: 'r19'},
            96: {0: 'r72', 14: 'r72', 18: 'r72'}
        }
        self.__sparse_goto_table = {
            0: {7: 1, 8: 6, 13: 4, 16: 5, 21: 3, 41: 2},
            2: {8: 6, 13: 4, 16: 5, 21: 96},
            8: {10: 12, 20: 9, 38: 13},
            12: {20: 9, 38: 14},
            17: {4: 24, 5: 21, 9: 25, 24: 20, 26: 23, 31: 19, 36: 18},
            19: {0: 75},
            20: {35: 52, 40: 51},
            21: {4: 24, 9: 25, 26: 50},
            25: {34: 48, 37: 47, 39: 49},
            28: {3: 40, 4: 24, 9: 25, 18: 30, 26: 31},
            29: {3: 32, 4: 24, 9: 25, 18: 30, 26: 31},
            30: {4: 24, 9: 25, 26: 39},
            31: {29: 35, 30: 34},
            34: {29: 38},
            36: {4: 24, 9: 25, 26: 37},
            41: {32: 45, 39: 46, 48: 44},
            53: {19: 55, 46: 54},
            54: {25: 57},
            58: {2: 61, 28: 60, 45: 59},
            59: {15: 70},
            63: {22: 68, 23: 66, 42: 64, 47: 65},
            65: {25: 69},
            70: {11: 72},
            73: {2: 61, 28: 60, 45: 74},
            75: {43: 77},
            76: {4: 24, 5: 21, 9: 25, 24: 20, 26: 23, 31: 78},
            80: {1: 82, 33: 81},
            81: {14: 86, 44: 85},
            88: {12: 90},
            89: {17: 92},
            92: {6: 94}
        }
        self.__sentence_index_grammar_tuple_mapping = {
            18: ('0', '*1'),
            15: ('1',),
            5: ('*0',),
            54: ('*0', '*1'),
            35: ('*0', '1'),
            57: ('1',),
            3: ('1', '*3'),
            24: (),
            14: ('*0',),
            55: ('0',),
            71: ('0', '*1'),
            50: (),
            53: ('*0',),
            23: ('*0', '1', '*2'),
            37: ('*0', '1'),
            13: (),
            67: ('*0',),
            33: (),
            29: ('*0',),
            7: (),
            21: ('*0',),
            22: ('1', '*2'),
            74: ('1',),
            49: (),
            41: ('*0', '*1'),
            65: ('*0',),
            12: ('*0', '1'),
            25: ('0', '*1'),
            44: ('*1', '2'),
            59: (),
            39: ('*0',),
            46: (),
            1: ('*0',),
            11: ('0', '*1'),
            28: ('1',),
            45: (),
            62: ('*0', '*1'),
            36: ('0', '2'),
            75: ('0', '*1'),
            19: ('1',),
            60: (),
            30: ('*0', '*1'),
            31: ('0', '2', '*3', '4'),
            4: ('*2',),
            40: (),
            38: ('*0',),
            16: (),
            43: ('*0',),
            66: ('0', '*1'),
            6: ('*0', '1'),
            72: ('*0', '1'),
            64: ('*0',)
        }
        self.__reduce_symbol_count = [1, 1, 1, 4, 4, 1, 2, 0, 1, 1, 1, 2, 2, 0, 1, 2, 0, 1, 2, 2, 1, 1, 4, 3, 0, 2, 1, 1, 2, 1, 2, 6, 1, 0, 1, 2, 4, 2, 1, 1, 0, 2, 1, 1, 3, 0, 0, 1, 1, 0, 0, 1, 1, 1, 2, 1, 1, 3, 1, 0, 0, 1, 2, 1, 1, 1, 3, 1, 1, 1, 0, 2, 2, 1, 2, 2]
        self.__reduce_non_terminal_index = [27, 46, 21, 4, 14, 3, 10, 28, 10, 5, 7, 36, 5, 22, 48, 29, 33, 34, 3, 6, 39, 28, 25, 45, 48, 31, 21, 41, 43, 47, 17, 8, 2, 47, 21, 18, 13, 42, 44, 35, 44, 15, 26, 33, 40, 0, 46, 9, 38, 15, 37, 1, 20, 37, 30, 9, 39, 4, 20, 35, 17, 19, 0, 32, 30, 24, 16, 22, 24, 23, 24, 26, 41, 18, 11, 12]

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
                elif statement_index in {0, 2, 8, 9, 10, 17, 20, 26, 27, 32, 34, 42, 47, 48, 51, 52, 56, 58, 61, 63, 68, 69, 70, 73}:
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
            66: 'command',
            31: 'lexical_define',
            36: 'reduce',
            23: 'grammar_node',
            71: 'name_closure',
            55: 'literal',
            3: 'complex_closure',
            57: 'complex_optional',
            18: 'select'
        }
        self.__naive_reduce_number_set = {2, 34, 68, 26, 70, 42, 47, 20, 52, 55, 56, 58}
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
