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
                [2, {'\\', "'"}, [], 29],
                [0, {"'"}, [], 31],
                [0, {'\\'}, [], 30]
            ],
            31: [
                [2, {'\\', "'"}, [], 29],
                [0, {"'"}, [], 31],
                [0, {'\\'}, [], 30]
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
        self.__character_set = {'V', 'Q', ')', '2', '_', 'd', '6', 'g', ' ', 'y', 'e', 'u', 'a', 'z', 'J', '4', ';', 'S', '(', 'X', '8', '0', '9', 'F', '+', 'c', 'l', 't', "'", 'h', 'q', 'W', 'T', 'N', 'k', 'Z', 'f', 'm', '%', '<', 'b', 'n', 'E', '7', 'A', '3', 'G', 'D', 'Y', '"', '>', ',', '5', 's', 'I', '1', ']', 'O', '}', 'x', '{', '\\', 'r', 'B', '#', '=', 'M', 'R', 'v', 'K', 'L', 'w', '\n', 'i', '\r', 'j', '@', '$', 'p', '[', 'H', '|', 'U', 'o', 'C', '~', '*', ':', 'P', '!', '\t'}
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
            '!symbol_7': 0,
            '!symbol_1': 1,
            '!symbol_13': 2,
            'node': 3,
            '!symbol_5': 4,
            'command': 5,
            'string': 6,
            '!symbol_16': 7,
            '$': 8,
            '!symbol_14': 9,
            'regular': 10,
            '!symbol_10': 11,
            '!symbol_6': 12,
            '!symbol_9': 13,
            'name': 14,
            '!symbol_15': 15,
            '!symbol_2': 16,
            '!symbol_4': 17,
            '!symbol_8': 18,
            '!symbol_3': 19,
            '!symbol_12': 20,
            '!symbol_11': 21
        }
        self.__sparse_action_table = {
            0: {5: 's7', 14: 's8'},
            1: {8: 'a'},
            2: {5: 's7', 8: 'r70', 14: 's8'},
            3: {5: 'r23', 8: 'r23', 14: 'r23'},
            4: {5: 'r6', 8: 'r6', 14: 'r6'},
            5: {5: 'r16', 8: 'r16', 14: 'r16'},
            6: {5: 'r35', 8: 'r35', 14: 'r35'},
            7: {6: 's92', 14: 's93'},
            8: {16: 's9', 18: 's10'},
            9: {10: 's73'},
            10: {1: 'r36', 6: 's16', 9: 's13', 11: 's20', 13: 'r36', 14: 's17', 16: 'r36', 21: 's14'},
            11: {1: 'r37', 2: 's58', 6: 'r37', 7: 's59', 9: 'r37', 13: 'r37', 14: 'r37', 15: 'r37', 16: 'r37', 20: 'r37', 21: 'r37'},
            12: {1: 'r65', 6: 'r65', 9: 'r65', 13: 'r65', 14: 'r65', 15: 'r65', 16: 'r65', 20: 'r65', 21: 'r65'},
            13: {6: 's16', 9: 's13', 14: 's17', 21: 's14'},
            14: {6: 's16', 9: 's13', 14: 's17', 21: 's14'},
            15: {1: 's72'},
            16: {1: 'r68', 2: 'r68', 6: 'r68', 7: 'r68', 9: 'r68', 13: 'r68', 14: 'r68', 15: 'r68', 16: 'r68', 20: 'r68', 21: 'r68'},
            17: {1: 'r71', 2: 'r71', 6: 'r71', 7: 'r71', 9: 'r71', 13: 'r71', 14: 'r71', 15: 'r71', 16: 'r71', 20: 'r71', 21: 'r71'},
            18: {1: 'r38', 13: 'r38'},
            19: {1: 'r50', 13: 'r50', 16: 's26'},
            20: {1: 'r47', 13: 'r47', 16: 'r47'},
            21: {1: 'r67', 6: 's16', 9: 's13', 13: 'r67', 14: 's17', 16: 'r67', 21: 's14'},
            22: {1: 'r3', 6: 'r3', 9: 'r3', 13: 'r3', 14: 'r3', 16: 'r3', 21: 'r3'},
            23: {1: 'r13', 6: 'r13', 9: 'r13', 13: 'r13', 14: 'r13', 16: 'r13', 21: 'r13'},
            24: {1: 'r54', 13: 'r54'},
            25: {1: 'r51', 13: 'r51'},
            26: {14: 's28', 21: 'r14'},
            27: {21: 'r41'},
            28: {21: 'r64'},
            29: {21: 's30'},
            30: {2: 's33', 3: 'r7'},
            31: {1: 'r55', 13: 'r55'},
            32: {3: 'r40'},
            33: {3: 'r21'},
            34: {0: 'r52', 20: 'r52'},
            35: {3: 's36'},
            36: {0: 'r48', 2: 's41', 20: 'r48', 21: 'r19'},
            37: {0: 'r49', 20: 'r49'},
            38: {0: 'r75', 20: 'r75'},
            39: {21: 's30'},
            40: {21: 'r61'},
            41: {21: 'r69'},
            42: {0: 'r10', 20: 'r10'},
            43: {0: 's45', 20: 's46'},
            44: {0: 'r56', 20: 'r56'},
            45: {2: 's33', 3: 'r7'},
            46: {0: 'r39', 1: 'r39', 13: 'r39', 20: 'r39'},
            47: {0: 'r34', 20: 'r34'},
            48: {1: 'r31', 13: 's49'},
            49: {1: 'r36', 6: 's16', 9: 's13', 11: 's20', 13: 'r36', 14: 's17', 16: 'r36', 21: 's14'},
            50: {1: 'r60', 13: 'r60'},
            51: {1: 'r25', 13: 'r25'},
            52: {20: 's56'},
            53: {6: 'r18', 9: 'r18', 13: 's69', 14: 'r18', 15: 'r18', 20: 'r18', 21: 'r18'},
            54: {6: 's16', 9: 's13', 14: 's17', 15: 'r59', 20: 'r59', 21: 's14'},
            55: {6: 'r2', 9: 'r2', 14: 'r2', 15: 'r2', 20: 'r2', 21: 'r2'},
            56: {1: 'r33', 2: 's58', 6: 'r33', 7: 's59', 9: 'r33', 13: 'r33', 14: 'r33', 15: 'r33', 16: 'r33', 20: 'r33', 21: 'r33'},
            57: {1: 'r5', 6: 'r5', 9: 'r5', 13: 'r5', 14: 'r5', 15: 'r5', 16: 'r5', 20: 'r5', 21: 'r5'},
            58: {1: 'r29', 6: 'r29', 9: 'r29', 13: 'r29', 14: 'r29', 15: 'r29', 16: 'r29', 20: 'r29', 21: 'r29'},
            59: {1: 'r46', 6: 'r46', 9: 'r46', 13: 'r46', 14: 'r46', 15: 'r46', 16: 'r46', 20: 'r46', 21: 'r46'},
            60: {1: 'r57', 6: 'r57', 9: 'r57', 13: 'r57', 14: 'r57', 15: 'r57', 16: 'r57', 20: 'r57', 21: 'r57'},
            61: {1: 'r26', 6: 'r26', 9: 'r26', 13: 'r26', 14: 'r26', 15: 'r26', 16: 'r26', 20: 'r26', 21: 'r26'},
            62: {15: 's63'},
            63: {1: 'r27', 6: 'r27', 9: 'r27', 13: 'r27', 14: 'r27', 15: 'r27', 16: 'r27', 20: 'r27', 21: 'r27'},
            64: {1: 'r24', 6: 'r24', 9: 'r24', 13: 'r24', 14: 'r24', 15: 'r24', 16: 'r24', 20: 'r24', 21: 'r24'},
            65: {1: 'r32', 6: 'r32', 9: 'r32', 13: 'r32', 14: 'r32', 15: 'r32', 16: 'r32', 20: 'r32', 21: 'r32'},
            66: {1: 'r66', 6: 'r66', 9: 'r66', 13: 'r66', 14: 'r66', 15: 'r66', 16: 'r66', 20: 'r66', 21: 'r66'},
            67: {13: 's69', 15: 'r53', 20: 'r53'},
            68: {13: 'r62', 15: 'r62', 20: 'r62'},
            69: {6: 's16', 9: 's13', 14: 's17', 21: 's14'},
            70: {13: 'r1', 15: 'r1', 20: 'r1'},
            71: {13: 'r9', 15: 'r9', 20: 'r9'},
            72: {5: 'r58', 8: 'r58', 14: 'r58'},
            73: {1: 'r42', 17: 'r42', 19: 's74'},
            74: {1: 'r22', 17: 'r22'},
            75: {1: 'r20', 17: 's78'},
            76: {1: 'r45', 17: 'r45'},
            77: {1: 'r72'},
            78: {4: 's81'},
            79: {1: 's80'},
            80: {5: 'r15', 8: 'r15', 14: 'r15'},
            81: {14: 's83'},
            82: {12: 's88'},
            83: {0: 'r74', 12: 'r74'},
            84: {0: 's85', 12: 'r44'},
            85: {14: 's87'},
            86: {0: 'r11', 12: 'r11'},
            87: {0: 'r63', 12: 'r63'},
            88: {1: 'r43'},
            89: {1: 's94', 6: 's92', 14: 's93'},
            90: {1: 'r17', 6: 'r17', 14: 'r17'},
            91: {1: 'r30', 6: 'r30', 14: 'r30'},
            92: {1: 'r8', 6: 'r8', 14: 'r8'},
            93: {1: 'r12', 6: 'r12', 14: 'r12'},
            94: {5: 'r28', 8: 'r28', 14: 'r28'},
            95: {1: 'r4', 6: 'r4', 14: 'r4'},
            96: {5: 'r73', 8: 'r73', 14: 'r73'}
        }
        self.__sparse_goto_table = {
            0: {2: 4, 11: 5, 13: 2, 33: 3, 35: 6, 41: 1},
            2: {2: 4, 11: 5, 33: 96, 35: 6},
            7: {10: 91, 14: 90, 31: 89},
            10: {0: 21, 5: 19, 15: 15, 18: 18, 23: 11, 25: 12, 43: 22},
            11: {36: 64, 39: 65, 45: 66},
            13: {7: 62, 12: 54, 23: 11, 25: 12, 43: 53},
            14: {7: 52, 12: 54, 23: 11, 25: 12, 43: 53},
            18: {44: 48},
            19: {19: 25, 22: 24},
            21: {23: 11, 25: 12, 43: 23},
            26: {8: 27, 32: 29},
            29: {1: 31},
            30: {3: 32, 26: 34, 29: 35},
            34: {17: 43},
            36: {6: 38, 34: 40, 37: 37, 40: 39},
            39: {1: 42},
            43: {21: 44},
            45: {3: 32, 26: 47, 29: 35},
            48: {48: 50},
            49: {0: 21, 5: 19, 18: 51, 23: 11, 25: 12, 43: 22},
            53: {24: 67, 42: 68},
            54: {23: 11, 25: 12, 43: 55},
            56: {27: 61, 45: 57, 47: 60},
            67: {42: 71},
            69: {23: 11, 25: 12, 43: 70},
            73: {30: 75, 38: 76},
            75: {4: 79, 28: 77},
            81: {16: 82},
            83: {9: 84},
            84: {20: 86},
            89: {10: 91, 14: 95}
        }
        self.__sentence_index_grammar_tuple_mapping = {
            53: ('0', '*1'),
            1: ('1',),
            59: ('*0',),
            9: ('*0', '*1'),
            2: ('*0', '1'),
            27: ('1',),
            57: ('1', '*3'),
            33: (),
            26: ('*0',),
            68: ('0',),
            24: ('0', '*1'),
            37: (),
            32: ('*0',),
            49: ('*0', '1', '*2'),
            10: ('*0', '1'),
            48: (),
            75: ('*0',),
            19: (),
            61: ('*0',),
            7: (),
            40: ('*0',),
            39: ('1', '*2'),
            34: ('1',),
            52: (),
            56: ('*0', '*1'),
            67: ('*0',),
            13: ('*0', '1'),
            54: ('0', '*1'),
            55: ('*1', '2'),
            50: (),
            51: ('*0',),
            14: (),
            41: ('*0',),
            31: ('0', '*1'),
            25: ('1',),
            38: (),
            60: ('*0', '*1'),
            58: ('0', '2'),
            44: ('0', '*1'),
            63: ('1',),
            74: (),
            11: ('*0', '*1'),
            15: ('0', '2', '*3', '4'),
            43: ('*2',),
            20: (),
            72: ('*0',),
            42: (),
            45: ('*0',),
            28: ('0', '*1'),
            4: ('*0', '1'),
            73: ('*0', '1'),
            62: ('*0',)
        }
        self.__reduce_symbol_count = [1, 2, 2, 1, 2, 1, 1, 0, 1, 2, 2, 2, 1, 2, 0, 6, 1, 1, 1, 0, 0, 1, 1, 1, 2, 2, 1, 3, 3, 1, 1, 2, 1, 0, 2, 1, 0, 0, 0, 4, 1, 1, 0, 4, 2, 1, 1, 1, 0, 3, 0, 1, 0, 2, 2, 3, 2, 4, 4, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 1]
        self.__reduce_non_terminal_index = [46, 42, 12, 0, 31, 27, 33, 29, 10, 24, 6, 9, 10, 0, 32, 11, 33, 31, 12, 40, 4, 3, 38, 13, 43, 48, 47, 25, 35, 45, 14, 15, 36, 47, 21, 33, 5, 36, 44, 1, 29, 32, 30, 28, 16, 30, 45, 5, 37, 26, 22, 22, 17, 7, 18, 19, 17, 25, 2, 7, 44, 40, 24, 20, 8, 43, 39, 5, 23, 34, 41, 23, 4, 13, 9, 37]

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
                elif statement_index in {0, 3, 5, 6, 8, 12, 16, 17, 18, 21, 22, 23, 29, 30, 35, 36, 46, 47, 64, 65, 66, 69, 70, 71}:
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
            28: 'command',
            15: 'lexical_define',
            58: 'reduce',
            49: 'grammar_node',
            24: 'name_closure',
            68: 'literal',
            57: 'complex_closure',
            27: 'complex_optional',
            53: 'select'
        }
        self.__naive_reduce_number_set = {65, 35, 68, 36, 6, 71, 8, 12, 46, 47, 16, 29}
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
