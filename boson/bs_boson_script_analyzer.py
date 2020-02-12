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
        self.__move_table = {
            0: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 1],
                [0, {'<'}, [], 33],
                [0, {'\n'}, [], 2],
                [0, {'\t', ' '}, [], 3],
                [0, {'$'}, [], 4],
                [0, {"'"}, [], 5],
                [0, {')'}, [], 6],
                [0, {'|'}, [], 7],
                [0, {'%'}, [], 8],
                [0, {'{'}, [], 9],
                [0, {']'}, [], 10],
                [0, {'~'}, [], 11],
                [0, {'*'}, [], 12],
                [0, {'+'}, [], 13],
                [0, {','}, [], 14],
                [0, {'}'}, [], 15],
                [0, {'='}, [], 16],
                [0, {':'}, [], 17],
                [0, {';'}, [], 18],
                [0, {'('}, [], 19],
                [0, {'@'}, [], 20],
                [0, {'#'}, [], 25],
                [0, {'"'}, [], 21],
                [0, {'['}, [], 22]
            ],
            21: [
                [2, {'\\'}, [], 23],
                [0, {'\\'}, [], 21]
            ],
            23: [
                [2, {'\\', '"'}, [], 23],
                [0, {'\\'}, [], 21],
                [0, {'"'}, [], 24]
            ],
            24: [
                [2, {'\\', '"'}, [], 23],
                [0, {'\\'}, [], 21],
                [0, {'"'}, [], 24]
            ],
            25: [
                [2, {'\r', '\n'}, [], 25]
            ],
            8: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 26]
            ],
            26: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 26]
            ],
            5: [
                [2, {'\\'}, [], 27],
                [0, {'\\'}, [], 5]
            ],
            27: [
                [2, {'\\', "'"}, [], 27],
                [0, {"'"}, [], 28],
                [0, {'\\'}, [], 5]
            ],
            28: [
                [2, {'\\', "'"}, [], 27],
                [0, {"'"}, [], 28],
                [0, {'\\'}, [], 5]
            ],
            4: [
                [0, set(), [('0', '9')], 29],
                [0, {'?', '@', '$'}, [], 30]
            ],
            29: [
                [0, set(), [('0', '9')], 29]
            ],
            3: [
                [0, {'\t', ' '}, [], 3]
            ],
            2: [
                [0, {'\r'}, [], 31]
            ],
            33: [
                [2, {'\\'}, [], 32],
                [0, {'\\'}, [], 33]
            ],
            32: [
                [2, {'>', '\\'}, [], 32],
                [0, {'>'}, [], 34],
                [0, {'\\'}, [], 33]
            ],
            34: [
                [2, {'>', '\\'}, [], 32],
                [0, {'>'}, [], 34],
                [0, {'\\'}, [], 33]
            ],
            1: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 1]
            ]
        }
        self.__character_set = {'N', 'Q', '<', 'q', 'p', 'g', '\n', 'W', 'S', 'y', 'i', 'E', 'T', 'V', '>', 'l', '\t', 'j', '$', 'e', '1', "'", 'H', ')', 'b', 'c', 'R', '7', 'F', 'L', 'a', '|', ' ', 't', '8', '%', '6', 'A', '2', '{', ']', '~', 's', 'z', 'M', '*', 'D', '+', '4', 'Y', '3', ',', 'o', 'u', '0', 'X', '?', 'h', 'w', '}', '=', ':', 'd', 'f', 'r', ';', 'K', '5', 'I', '_', '\\', '\r', '(', 'G', '9', '@', 'Z', 'k', 'O', 'm', 'n', '#', 'v', 'x', 'C', '"', 'P', '[', 'B', 'U', 'J'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 3, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 25, 26, 28, 29, 30, 31, 34}
        self.__lexical_symbol_mapping = {
            1: 'name',
            2: 'newline',
            3: 'skip',
            6: '!symbol_9',
            7: '!symbol_6',
            9: '!symbol_4',
            10: '!symbol_11',
            11: '!symbol_13',
            12: '!symbol_14',
            13: '!symbol_15',
            14: '!symbol_7',
            15: '!symbol_5',
            16: '!symbol_2',
            17: '!symbol_12',
            18: '!symbol_1',
            19: '!symbol_8',
            20: '!symbol_3',
            22: '!symbol_10',
            24: 'string',
            25: 'comment',
            26: 'command',
            28: 'string',
            29: 'node',
            30: 'node',
            31: 'newline',
            34: 'regular'
        }
        self.__symbol_function_mapping = {
            'comment': ['skip'],
            'skip': ['skip'],
            'newline': ['skip', 'newline']
        }
        self.__lexical_function = {}

    def _invoke_lexical_function(self, symbol: str, token_string):
        if symbol in self.__symbol_function_mapping:
            for function in self.__symbol_function_mapping[symbol]:
                if function in self.__lexical_function:
                    token_string = self.__lexical_function[function](token_string)
                elif function == 'skip':
                    token_string = None
                elif function == 'newline':
                    self.__line += 1
        return token_string

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
            generate_token = False
            if state in self.__move_table:
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
                        if state in self.__end_state_set and next_state not in self.__end_state_set:
                            generate_token = True
                            break
                        token_string += character
                        state = next_state
                        break
                else:
                    if state in self.__end_state_set:
                        generate_token = True
                    else:
                        self.__error_line = self.__line
                        return self.__error_line
            else:
                if state in self.__end_state_set:
                    generate_token = True
                else:
                    raise ValueError('Invalid state: state={}'.format(state))
            if generate_token:
                symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
                token_string = self._invoke_lexical_function(symbol, token_string)
                if token_string is not None:
                    self.__token_list.append(LexicalToken(token_string, self.__line, symbol))
                token_string = ''
                state = self.__start_state
                index -= 1
        if state in self.__end_state_set:
            symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
            token_string = self._invoke_lexical_function(symbol, token_string)
            if token_string is not None:
                self.__token_list.append(LexicalToken(token_string, self.__line, symbol))
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
        self.__error_index = None

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
            'name': 0,
            '!symbol_5': 1,
            '!symbol_15': 2,
            '!symbol_7': 3,
            'string': 4,
            '!symbol_3': 5,
            '!symbol_2': 6,
            'node': 7,
            '!symbol_11': 8,
            '!symbol_12': 9,
            'command': 10,
            '!symbol_14': 11,
            'regular': 12,
            '!symbol_9': 13,
            '!symbol_10': 14,
            '!symbol_8': 15,
            '!symbol_6': 16,
            '!symbol_4': 17,
            '!symbol_1': 18,
            '!symbol_13': 19,
            '$': 20
        }
        self.__action_table = {
            0: {0: 's3', 10: 's7'},
            1: {0: 's3', 10: 's7', 20: 'r64'},
            2: {0: 'r91', 10: 'r91', 20: 'r91'},
            3: {6: 's10', 9: 's11'},
            4: {0: 'r2', 10: 'r2', 20: 'r2'},
            5: {0: 'r93', 10: 'r93', 20: 'r93'},
            6: {0: 'r92', 10: 'r92', 20: 'r92'},
            7: {0: 's13', 4: 's14'},
            8: {20: 'a'},
            9: {0: 'r1', 10: 'r1', 20: 'r1'},
            10: {0: 's18', 12: 's20', 14: 's25', 15: 's19'},
            11: {0: 's32', 4: 's33', 6: 'r75', 14: 's30', 15: 's36', 16: 'r75', 18: 'r75', 19: 's35'},
            12: {0: 'r37', 4: 'r37', 18: 'r37'},
            13: {0: 'r3', 4: 'r3', 18: 'r3'},
            14: {0: 'r4', 4: 'r4', 18: 'r4'},
            15: {0: 'r21', 4: 'r21', 18: 'r21'},
            16: {0: 's13', 4: 's14', 18: 's41'},
            17: {0: 's18', 5: 'r87', 14: 's25', 15: 's19', 16: 'r87', 18: 'r87'},
            18: {0: 'r12', 2: 's47', 5: 'r12', 8: 'r12', 11: 's45', 13: 'r12', 14: 'r12', 15: 'r12', 16: 'r12', 18: 'r12'},
            19: {0: 's18', 14: 's25', 15: 's19'},
            20: {5: 's52', 18: 'r57'},
            21: {16: 'r60', 18: 'r60'},
            22: {18: 'r83'},
            23: {0: 'r9', 5: 'r9', 14: 'r9', 15: 'r9', 16: 'r9', 18: 'r9'},
            24: {5: 's55', 16: 'r7', 18: 'r7'},
            25: {0: 's18', 14: 's25', 15: 's19'},
            26: {18: 's59'},
            27: {0: 'r81', 5: 'r81', 8: 'r81', 13: 'r81', 14: 'r81', 15: 'r81', 16: 'r81', 18: 'r81'},
            28: {0: 's32', 4: 's33', 6: 'r73', 14: 's30', 15: 's36', 16: 'r73', 18: 'r73'},
            29: {6: 's63', 16: 'r30', 18: 'r30'},
            30: {0: 's32', 4: 's33', 14: 's30', 15: 's36'},
            31: {0: 'r77', 4: 'r77', 6: 'r77', 8: 'r77', 13: 'r77', 14: 'r77', 15: 'r77', 16: 'r77', 18: 'r77'},
            32: {0: 'r98', 2: 'r98', 4: 'r98', 6: 'r98', 8: 'r98', 11: 'r98', 13: 'r98', 14: 'r98', 15: 'r98', 16: 'r98', 18: 'r98'},
            33: {0: 'r99', 2: 'r99', 4: 'r99', 6: 'r99', 8: 'r99', 11: 'r99', 13: 'r99', 14: 'r99', 15: 'r99', 16: 'r99', 18: 'r99'},
            34: {18: 's67'},
            35: {6: 'r74', 16: 'r74', 18: 'r74'},
            36: {0: 's32', 4: 's33', 14: 's30', 15: 's36'},
            37: {16: 'r24', 18: 'r24'},
            38: {0: 'r32', 4: 'r32', 6: 'r32', 14: 'r32', 15: 'r32', 16: 'r32', 18: 'r32'},
            39: {0: 'r46', 2: 's47', 4: 'r46', 6: 'r46', 8: 'r46', 11: 's45', 13: 'r46', 14: 'r46', 15: 'r46', 16: 'r46', 18: 'r46'},
            40: {0: 'r38', 4: 'r38', 18: 'r38'},
            41: {0: 'r67', 10: 'r67', 20: 'r67'},
            42: {0: 'r8', 5: 'r8', 14: 'r8', 15: 'r8', 16: 'r8', 18: 'r8'},
            43: {0: 'r10', 5: 'r10', 8: 'r10', 13: 'r10', 14: 'r10', 15: 'r10', 16: 'r10', 18: 'r10'},
            44: {0: 'r82', 5: 'r82', 8: 'r82', 13: 'r82', 14: 'r82', 15: 'r82', 16: 'r82', 18: 'r82'},
            45: {0: 'r65', 4: 'r65', 5: 'r65', 6: 'r65', 8: 'r65', 13: 'r65', 14: 'r65', 15: 'r65', 16: 'r65', 18: 'r65'},
            46: {0: 'r11', 5: 'r11', 8: 'r11', 13: 'r11', 14: 'r11', 15: 'r11', 16: 'r11', 18: 'r11'},
            47: {0: 'r66', 4: 'r66', 5: 'r66', 6: 'r66', 8: 'r66', 13: 'r66', 14: 'r66', 15: 'r66', 16: 'r66', 18: 'r66'},
            48: {0: 'r17', 8: 'r17', 13: 'r17', 14: 'r17', 15: 'r17', 16: 's75'},
            49: {0: 's18', 8: 'r96', 13: 'r96', 14: 's25', 15: 's19'},
            50: {13: 's77'},
            51: {18: 'r84'},
            52: {17: 's78'},
            53: {18: 'r56'},
            54: {16: 's79', 18: 'r88'},
            55: {17: 's81'},
            56: {16: 'r6', 18: 'r6'},
            57: {16: 'r86', 18: 'r86'},
            58: {8: 's82'},
            59: {0: 'r89', 10: 'r89', 20: 'r89'},
            60: {0: 'r31', 4: 'r31', 6: 'r31', 14: 'r31', 15: 'r31', 16: 'r31', 18: 'r31'},
            61: {16: 'r72', 18: 'r72'},
            62: {16: 'r29', 18: 'r29'},
            63: {0: 's84', 15: 'r27'},
            64: {8: 's86'},
            65: {0: 'r51', 4: 'r51', 8: 'r51', 13: 'r51', 14: 'r51', 15: 'r51', 16: 's88'},
            66: {0: 's32', 4: 's33', 8: 'r94', 13: 'r94', 14: 's30', 15: 's36'},
            67: {0: 'r79', 10: 'r79', 20: 'r79'},
            68: {13: 's91'},
            69: {16: 's93', 18: 'r76'},
            70: {0: 'r78', 4: 'r78', 6: 'r78', 8: 'r78', 13: 'r78', 14: 'r78', 15: 'r78', 16: 'r78', 18: 'r78'},
            71: {0: 'r44', 4: 'r44', 6: 'r44', 8: 'r44', 13: 'r44', 14: 'r44', 15: 'r44', 16: 'r44', 18: 'r44'},
            72: {0: 'r45', 4: 'r45', 6: 'r45', 8: 'r45', 13: 'r45', 14: 'r45', 15: 'r45', 16: 'r45', 18: 'r45'},
            73: {8: 'r19', 13: 'r19', 16: 'r19'},
            74: {8: 'r97', 13: 'r97', 16: 's75'},
            75: {0: 's18', 14: 's25', 15: 's19'},
            76: {0: 'r16', 8: 'r16', 13: 'r16', 14: 'r16', 15: 'r16'},
            77: {0: 'r15', 2: 's47', 5: 'r15', 8: 'r15', 11: 's45', 13: 'r15', 14: 'r15', 15: 'r15', 16: 'r15', 18: 'r15'},
            78: {0: 's99'},
            79: {0: 's18', 14: 's25', 15: 's19'},
            80: {16: 'r59', 18: 'r59'},
            81: {0: 's99'},
            82: {0: 'r70', 5: 'r70', 8: 'r70', 13: 'r70', 14: 'r70', 15: 'r70', 16: 'r70', 18: 'r70'},
            83: {15: 's104'},
            84: {15: 'r25'},
            85: {15: 'r26'},
            86: {0: 'r68', 4: 'r68', 6: 'r68', 8: 'r68', 13: 'r68', 14: 'r68', 15: 'r68', 16: 'r68', 18: 'r68'},
            87: {8: 'r95', 13: 'r95', 16: 's88'},
            88: {0: 's32', 4: 's33', 14: 's30', 15: 's36'},
            89: {8: 'r53', 13: 'r53', 16: 'r53'},
            90: {0: 'r50', 4: 'r50', 8: 'r50', 13: 'r50', 14: 'r50', 15: 'r50'},
            91: {0: 'r49', 2: 's47', 4: 'r49', 6: 'r49', 8: 'r49', 11: 's45', 13: 'r49', 14: 'r49', 15: 'r49', 16: 'r49', 18: 'r49'},
            92: {16: 'r23', 18: 'r23'},
            93: {0: 's32', 4: 's33', 6: 'r75', 14: 's30', 15: 's36', 16: 'r75', 18: 'r75', 19: 's35'},
            94: {8: 'r20', 13: 'r20', 16: 'r20'},
            95: {8: 'r18', 13: 'r18', 16: 'r18'},
            96: {0: 'r71', 5: 'r71', 8: 'r71', 13: 'r71', 14: 'r71', 15: 'r71', 16: 'r71', 18: 'r71'},
            97: {0: 'r14', 5: 'r14', 8: 'r14', 13: 'r14', 14: 'r14', 15: 'r14', 16: 'r14', 18: 'r14'},
            98: {0: 'r13', 5: 'r13', 8: 'r13', 13: 'r13', 14: 'r13', 15: 'r13', 16: 'r13', 18: 'r13'},
            99: {1: 'r63', 3: 'r63'},
            100: {1: 's112'},
            101: {16: 'r58', 18: 'r58'},
            102: {1: 's113'},
            103: {16: 'r28', 18: 'r28'},
            104: {7: 'r40', 11: 's117'},
            105: {8: 'r54', 13: 'r54', 16: 'r54'},
            106: {8: 'r52', 13: 'r52', 16: 'r52'},
            107: {0: 'r47', 4: 'r47', 6: 'r47', 8: 'r47', 13: 'r47', 14: 'r47', 15: 'r47', 16: 'r47', 18: 'r47'},
            108: {0: 'r69', 4: 'r69', 6: 'r69', 8: 'r69', 13: 'r69', 14: 'r69', 15: 'r69', 16: 'r69', 18: 'r69'},
            109: {0: 'r48', 4: 'r48', 6: 'r48', 8: 'r48', 13: 'r48', 14: 'r48', 15: 'r48', 16: 'r48', 18: 'r48'},
            110: {16: 'r22', 18: 'r22'},
            111: {1: 'r85', 3: 's118'},
            112: {18: 'r55'},
            113: {16: 'r5', 18: 'r5'},
            114: {7: 'r39'},
            115: {7: 's120'},
            116: {3: 'r35', 13: 'r35'},
            117: {7: 'r36'},
            118: {0: 's122'},
            119: {1: 'r62', 3: 'r62'},
            120: {3: 'r43', 13: 'r43', 15: 's104', 16: 'r43', 18: 'r43'},
            121: {3: 's126', 13: 's128'},
            122: {1: 'r61', 3: 'r61'},
            123: {3: 'r42', 13: 'r42', 16: 'r42', 18: 'r42'},
            124: {3: 'r41', 13: 'r41', 16: 'r41', 18: 'r41'},
            125: {3: 'r90', 13: 'r90', 16: 'r90', 18: 'r90'},
            126: {7: 'r40', 11: 's117'},
            127: {3: 'r34', 13: 'r34'},
            128: {3: 'r80', 13: 'r80', 16: 'r80', 18: 'r80'},
            129: {3: 'r33', 13: 'r33'}
        }
        self.__goto_table = {
            0: {14: 5, 18: 1, 21: 4, 24: 8, 36: 2, 42: 6},
            1: {14: 5, 21: 9, 36: 2, 42: 6},
            7: {4: 12, 29: 15, 50: 16},
            10: {13: 22, 15: 26, 23: 27, 34: 21, 51: 24, 60: 17, 61: 23},
            11: {6: 38, 26: 37, 37: 31, 45: 28, 49: 29, 56: 34, 62: 39},
            16: {4: 40, 29: 15},
            17: {23: 27, 61: 42},
            18: {7: 44, 39: 46, 46: 43},
            19: {22: 49, 23: 27, 59: 50, 61: 48},
            20: {8: 51, 28: 53},
            21: {0: 54},
            24: {12: 56, 32: 57},
            25: {22: 49, 23: 27, 59: 58, 61: 48},
            28: {6: 60, 37: 31, 62: 39},
            29: {19: 62, 20: 61},
            30: {2: 66, 6: 65, 37: 31, 47: 64, 62: 39},
            36: {2: 66, 6: 65, 37: 31, 47: 68, 62: 39},
            37: {11: 69},
            39: {25: 70, 35: 72, 46: 71},
            48: {40: 73, 43: 74},
            49: {23: 27, 61: 76},
            54: {48: 80},
            63: {53: 83, 55: 85},
            65: {1: 89, 5: 87},
            66: {6: 90, 37: 31, 62: 39},
            69: {33: 92},
            74: {40: 94},
            75: {23: 27, 61: 95},
            77: {17: 97, 46: 98, 57: 96},
            78: {52: 100},
            79: {23: 27, 34: 101, 51: 24, 60: 17, 61: 23},
            81: {52: 102},
            83: {31: 103},
            87: {1: 105},
            88: {6: 106, 37: 31, 62: 39},
            91: {10: 109, 46: 107, 58: 108},
            93: {6: 38, 26: 110, 37: 31, 45: 28, 49: 29, 62: 39},
            99: {9: 111},
            104: {27: 114, 54: 115, 63: 116},
            111: {3: 119},
            116: {44: 121},
            120: {30: 123, 31: 124, 38: 125},
            121: {16: 127},
            126: {27: 114, 54: 115, 63: 129}
        }
        self.__node_table = {
            0: ('*0', '1'),
            37: ('*0', '1'),
            66: ('0', ('*1', ('?',))),
            88: ('0', '2'),
            56: (),
            83: ('0', ('1', ('*2',))),
            58: ('*0', '1'),
            59: (),
            87: ('0', ('*1', ('1',))),
            61: ('*0', '1'),
            62: (),
            84: ('0', ('*1', ('1',))),
            6: (),
            85: ('0', ('1', ('*2',))),
            7: ('*0', '1'),
            86: ('*0',),
            11: (),
            81: ('0', ('*1', ('?',))),
            14: (),
            70: ('1', ('*3', ('?',))),
            69: ('1',),
            15: ('*0', '1'),
            19: ('*0', '1'),
            95: ('*0',),
            96: ('0', ('*1', ('1',))),
            78: ('0', '2'),
            22: ('*0', '1'),
            23: (),
            75: ('0', ('*1', ('1',))),
            26: (),
            29: (),
            71: ('0', ('*1', (('*1', ('?',)), '2'))),
            30: ('*0', '1'),
            72: ('*0',),
            33: ('*0', '1'),
            34: (),
            79: ('1', ('*2', ('1',))),
            39: (),
            42: (),
            89: (('*0', ('?',)), '1', ('*2', ('?',))),
            45: (),
            77: ('0', ('*1', ('?',))),
            98: ('0',),
            48: (),
            68: ('1', ('*3', ('?',))),
            67: ('1',),
            49: ('*0', '1'),
            53: ('*0', '1'),
            93: ('*0',),
            94: ('0', ('*1', ('1',)))
        }
        self.__reduce_symbol_sum = [2, 1, 1, 1, 4, 1, 0, 2, 1, 1, 1, 0, 1, 1, 0, 2, 1, 2, 1, 2, 1, 2, 2, 0, 1, 1, 0, 3, 1, 0, 2, 1, 2, 2, 0, 1, 1, 2, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 2, 1, 2, 1, 2, 4, 1, 0, 2, 2, 0, 2, 2, 0, 1, 1, 1, 3, 3, 4, 3, 4, 2, 1, 1, 0, 2, 1, 2, 4, 4, 1, 2, 1, 2, 2, 2, 1, 2, 4, 3, 1, 1, 1, 1, 2, 1, 2, 1, 1]
        self.__reduce_to_non_terminal_index = [18, 18, 29, 29, 12, 32, 32, 60, 60, 39, 7, 7, 17, 57, 57, 22, 22, 40, 43, 43, 4, 33, 11, 11, 55, 53, 53, 19, 20, 20, 45, 45, 16, 44, 44, 27, 50, 50, 54, 54, 30, 38, 38, 35, 25, 25, 10, 58, 58, 2, 2, 1, 5, 5, 28, 8, 8, 48, 0, 0, 3, 9, 9, 24, 46, 46, 36, 37, 37, 23, 23, 26, 49, 49, 49, 56, 6, 6, 42, 31, 61, 61, 15, 15, 52, 34, 51, 13, 14, 63, 21, 21, 21, 47, 47, 59, 59, 62, 62]

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
                elif statement_index in [1, 2, 3, 4, 5, 8, 9, 10, 12, 13, 16, 17, 18, 20, 21, 24, 25, 27, 28, 31, 32, 35, 36, 38, 40, 41, 43, 44, 46, 47, 50, 51, 52, 54, 55, 57, 60, 63, 64, 65, 73, 74, 76, 80, 82, 90, 91, 92, 97]:
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
            66: 'command',
            88: 'lexical_define',
            81: 'lexical_name_closure',
            70: 'lexical_closure',
            69: 'lexical_optional',
            96: 'lexical_select',
            78: 'reduce',
            89: 'grammar_node',
            77: 'name_closure',
            98: 'literal',
            68: 'complex_closure',
            67: 'complex_optional',
            94: 'select'
        }
        self.__reduce_number_to_grammar_number = {
            63: 0,
            90: 1,
            92: 2,
            91: 3,
            82: 6,
            83: 7,
            87: 8,
            84: 9,
            85: 10,
            86: 11,
            80: 12,
            95: 16,
            75: 19,
            71: 20,
            72: 21,
            73: 22,
            74: 23,
            79: 24,
            76: 26,
            97: 28,
            93: 32,
            65: 34,
            64: 35
        }
        self.__naive_reduce_number = {64, 97, 98, 3, 2, 65, 73, 74, 76, 80, 82, 90, 91, 92}
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
