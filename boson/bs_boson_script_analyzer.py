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
        self.__move_table = {
            0: [
                [False, {'_'}, [('A', 'Z'), ('a', 'z')], 1],
                [False, {'\n'}, [], 2],
                [False, {'#'}, [], 33],
                [False, {':'}, [], 3],
                [False, {"'"}, [], 4],
                [False, {'+'}, [], 5],
                [False, {'\t', ' '}, [], 8],
                [False, {']'}, [], 6],
                [False, {'@'}, [], 7],
                [False, {'['}, [], 9],
                [False, {'{'}, [], 10],
                [False, {'"'}, [], 29],
                [False, {'$'}, [], 11],
                [False, {'~'}, [], 12],
                [False, {'}'}, [], 13],
                [False, {'*'}, [], 14],
                [False, {'='}, [], 15],
                [False, {','}, [], 16],
                [False, {'<'}, [], 24],
                [False, {';'}, [], 17],
                [False, {'('}, [], 18],
                [False, {'|'}, [], 19],
                [False, {'%'}, [], 20],
                [False, {')'}, [], 21]
            ],
            20: [
                [False, {'_'}, [('A', 'Z'), ('a', 'z')], 22]
            ],
            22: [
                [False, {'_'}, [('A', 'Z'), ('a', 'z')], 22]
            ],
            24: [
                [True, {'\\'}, [], 23],
                [False, {'\\'}, [], 24]
            ],
            23: [
                [True, {'\\', '>'}, [], 23],
                [False, {'>'}, [], 25],
                [False, {'\\'}, [], 24]
            ],
            25: [
                [True, {'\\', '>'}, [], 23],
                [False, {'>'}, [], 25],
                [False, {'\\'}, [], 24]
            ],
            11: [
                [False, set(), [('0', '9')], 26],
                [False, {'$', '?', '@'}, [], 27]
            ],
            26: [
                [False, set(), [('0', '9')], 26]
            ],
            29: [
                [True, {'\\'}, [], 28],
                [False, {'\\'}, [], 29]
            ],
            28: [
                [True, {'\\', '"'}, [], 28],
                [False, {'"'}, [], 30],
                [False, {'\\'}, [], 29]
            ],
            30: [
                [True, {'\\', '"'}, [], 28],
                [False, {'"'}, [], 30],
                [False, {'\\'}, [], 29]
            ],
            8: [
                [False, {'\t', ' '}, [], 8]
            ],
            4: [
                [True, {'\\'}, [], 31],
                [False, {'\\'}, [], 4]
            ],
            31: [
                [True, {'\\', "'"}, [], 31],
                [False, {"'"}, [], 32],
                [False, {'\\'}, [], 4]
            ],
            32: [
                [True, {'\\', "'"}, [], 31],
                [False, {"'"}, [], 32],
                [False, {'\\'}, [], 4]
            ],
            33: [
                [True, {'\r', '\n'}, [], 33]
            ],
            2: [
                [False, {'\r'}, [], 34]
            ],
            1: [
                [False, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 1]
            ]
        }
        self.__character_set = {'m', 'Q', 'C', '\n', '#', ':', 'o', "'", '_', '+', 'h', 'P', 'T', '\t', ']', 'j', 'u', '7', '2', '0', '5', 'q', '@', 'U', 'H', 'S', 'X', ' ', '4', 'O', '[', '1', '{', 'n', 'L', 'x', 'Z', 'z', 'v', 'l', 'J', 'B', 'p', 'i', '"', 'N', '$', 'd', 'F', 'A', 'r', '>', '9', 'a', '~', '}', '*', 't', 'e', 'M', '\r', 'V', 'c', 'G', 'b', 'w', 'K', '3', '=', 'I', 'R', '?', ',', '<', 'W', 'g', '\\', '8', 'k', 'y', 'E', 'Y', ';', '(', 'D', '|', '%', ')', 'f', 's', '6'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 25, 26, 27, 30, 32, 33, 34}
        self.__lexical_symbol_mapping = {
            1: 'name',
            2: 'newline',
            3: '!symbol_12',
            5: '!symbol_15',
            6: '!symbol_11',
            7: '!symbol_3',
            8: 'skip',
            9: '!symbol_10',
            10: '!symbol_4',
            12: '!symbol_13',
            13: '!symbol_5',
            14: '!symbol_14',
            15: '!symbol_2',
            16: '!symbol_7',
            17: '!symbol_1',
            18: '!symbol_8',
            19: '!symbol_6',
            21: '!symbol_9',
            22: 'command',
            25: 'regular',
            26: 'node',
            27: 'node',
            30: 'string',
            32: 'string',
            33: 'comment',
            34: 'newline'
        }
        self.__symbol_function_mapping = {
            'comment': ['skip'],
            'skip': ['skip'],
            'newline': ['skip', 'newline']
        }
        self.__lexical_function = {
            'skip': self._lexical_function_skip,
            'newline': self._lexical_function_newline,
        }
        self.__line = 0

    def _lexical_function_skip(self, token_string):
        return None

    def _lexical_function_newline(self, token_string):
        self.__line += 1
        return token_string

    def invoke_lexical_function(self, symbol: str, token):
        if symbol in self.__symbol_function_mapping:
            for function in self.__symbol_function_mapping[symbol]:
                if function in self.__lexical_function:
                    token = self.__lexical_function[function](token)
        return token

    def tokenize(self, text: str):
        token_list = []
        self.__line = 0
        state = self.__start_state
        token_string = ''
        index = 0
        while index < len(text):
            character = text[index]
            index += 1
            generate_token = False
            if state in self.__move_table:
                for reverse, character_set, range_list, next_state in self.__move_table[state]:
                    if reverse:
                        condition = character not in character_set
                        for min_character, max_character in range_list:
                            condition &= character < min_character or character > max_character
                    else:
                        condition = character in character_set
                        if True in character_set and character not in self.__character_set:
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
                        raise ValueError('[Line: {}] Invalid character: {}[{}]'.format(self.__line, token_string, character))
            else:
                if state in self.__end_state_set:
                    generate_token = True
                else:
                    raise ValueError('Invalid state: state={}'.format(state))
            if generate_token:
                symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
                token_string = self.invoke_lexical_function(symbol, token_string)
                if token_string is not None:
                    token_list.append(LexicalToken(token_string, self.__line, symbol))
                token_string = ''
                state = self.__start_state
                index -= 1
        if state in self.__end_state_set:
            symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
            token_string = self.invoke_lexical_function(symbol, token_string)
            if token_string is not None:
                token_list.append(LexicalToken(token_string, self.__line, symbol))
        else:
            raise ValueError('Invalid state: state={}'.format(state))
        token_list.append(LexicalToken('', self.__line, '$'))
        return token_list

    def lexical_function(self, function_name):
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
            '!symbol_2': 0,
            '!symbol_6': 1,
            '$': 2,
            '!symbol_1': 3,
            '!symbol_10': 4,
            'node': 5,
            '!symbol_5': 6,
            '!symbol_3': 7,
            '!symbol_8': 8,
            '!symbol_12': 9,
            'command': 10,
            '!symbol_7': 11,
            '!symbol_11': 12,
            '!symbol_4': 13,
            'regular': 14,
            '!symbol_9': 15,
            '!symbol_15': 16,
            '!symbol_13': 17,
            '!symbol_14': 18,
            'name': 19,
            'string': 20
        }
        self.__action_table = {
            0: {10: 's8', 19: 's4'},
            1: {2: 'r2', 10: 'r2', 19: 'r2'},
            2: {2: 'r64', 10: 's8', 19: 's4'},
            3: {2: 'r91', 10: 'r91', 19: 'r91'},
            4: {0: 's10', 9: 's11'},
            5: {2: 'r93', 10: 'r93', 19: 'r93'},
            6: {2: 'r92', 10: 'r92', 19: 'r92'},
            7: {2: 'a'},
            8: {19: 's14', 20: 's12'},
            9: {2: 'r1', 10: 'r1', 19: 'r1'},
            10: {4: 's17', 8: 's26', 14: 's23', 19: 's19'},
            11: {0: 'r75', 1: 'r75', 3: 'r75', 4: 's33', 8: 's29', 17: 's37', 19: 's30', 20: 's28'},
            12: {3: 'r4', 19: 'r4', 20: 'r4'},
            13: {3: 's40', 19: 's14', 20: 's12'},
            14: {3: 'r3', 19: 'r3', 20: 'r3'},
            15: {3: 'r37', 19: 'r37', 20: 'r37'},
            16: {3: 'r21', 19: 'r21', 20: 'r21'},
            17: {4: 's17', 8: 's26', 19: 's19'},
            18: {3: 's45'},
            19: {1: 'r12', 3: 'r12', 4: 'r12', 7: 'r12', 8: 'r12', 12: 'r12', 15: 'r12', 16: 's48', 18: 's50', 19: 'r12'},
            20: {1: 'r87', 3: 'r87', 4: 's17', 7: 'r87', 8: 's26', 19: 's19'},
            21: {1: 'r9', 3: 'r9', 4: 'r9', 7: 'r9', 8: 'r9', 19: 'r9'},
            22: {1: 'r60', 3: 'r60'},
            23: {3: 'r57', 7: 's55'},
            24: {1: 'r7', 3: 'r7', 7: 's57'},
            25: {1: 'r81', 3: 'r81', 4: 'r81', 7: 'r81', 8: 'r81', 12: 'r81', 15: 'r81', 19: 'r81'},
            26: {4: 's17', 8: 's26', 19: 's19'},
            27: {3: 'r83'},
            28: {0: 'r99', 1: 'r99', 3: 'r99', 4: 'r99', 8: 'r99', 12: 'r99', 15: 'r99', 16: 'r99', 18: 'r99', 19: 'r99', 20: 'r99'},
            29: {4: 's33', 8: 's29', 19: 's30', 20: 's28'},
            30: {0: 'r98', 1: 'r98', 3: 'r98', 4: 'r98', 8: 'r98', 12: 'r98', 15: 'r98', 16: 'r98', 18: 'r98', 19: 'r98', 20: 'r98'},
            31: {0: 's63', 1: 'r30', 3: 'r30'},
            32: {0: 'r46', 1: 'r46', 3: 'r46', 4: 'r46', 8: 'r46', 12: 'r46', 15: 'r46', 16: 's48', 18: 's50', 19: 'r46', 20: 'r46'},
            33: {4: 's33', 8: 's29', 19: 's30', 20: 's28'},
            34: {0: 'r32', 1: 'r32', 3: 'r32', 4: 'r32', 8: 'r32', 19: 'r32', 20: 'r32'},
            35: {0: 'r73', 1: 'r73', 3: 'r73', 4: 's33', 8: 's29', 19: 's30', 20: 's28'},
            36: {1: 'r24', 3: 'r24'},
            37: {0: 'r74', 1: 'r74', 3: 'r74'},
            38: {0: 'r77', 1: 'r77', 3: 'r77', 4: 'r77', 8: 'r77', 12: 'r77', 15: 'r77', 19: 'r77', 20: 'r77'},
            39: {3: 's72'},
            40: {2: 'r67', 10: 'r67', 19: 'r67'},
            41: {3: 'r38', 19: 'r38', 20: 'r38'},
            42: {4: 's17', 8: 's26', 12: 'r96', 15: 'r96', 19: 's19'},
            43: {12: 's74'},
            44: {1: 's77', 4: 'r17', 8: 'r17', 12: 'r17', 15: 'r17', 19: 'r17'},
            45: {2: 'r89', 10: 'r89', 19: 'r89'},
            46: {1: 'r82', 3: 'r82', 4: 'r82', 7: 'r82', 8: 'r82', 12: 'r82', 15: 'r82', 19: 'r82'},
            47: {1: 'r10', 3: 'r10', 4: 'r10', 7: 'r10', 8: 'r10', 12: 'r10', 15: 'r10', 19: 'r10'},
            48: {0: 'r66', 1: 'r66', 3: 'r66', 4: 'r66', 7: 'r66', 8: 'r66', 12: 'r66', 15: 'r66', 19: 'r66', 20: 'r66'},
            49: {1: 'r11', 3: 'r11', 4: 'r11', 7: 'r11', 8: 'r11', 12: 'r11', 15: 'r11', 19: 'r11'},
            50: {0: 'r65', 1: 'r65', 3: 'r65', 4: 'r65', 7: 'r65', 8: 'r65', 12: 'r65', 15: 'r65', 19: 'r65', 20: 'r65'},
            51: {1: 'r8', 3: 'r8', 4: 'r8', 7: 'r8', 8: 'r8', 19: 'r8'},
            52: {1: 's78', 3: 'r88'},
            53: {3: 'r56'},
            54: {3: 'r84'},
            55: {13: 's80'},
            56: {1: 'r86', 3: 'r86'},
            57: {13: 's81'},
            58: {1: 'r6', 3: 'r6'},
            59: {15: 's82'},
            60: {15: 's83'},
            61: {4: 's33', 8: 's29', 12: 'r94', 15: 'r94', 19: 's30', 20: 's28'},
            62: {1: 's85', 4: 'r51', 8: 'r51', 12: 'r51', 15: 'r51', 19: 'r51', 20: 'r51'},
            63: {8: 'r27', 19: 's88'},
            64: {1: 'r29', 3: 'r29'},
            65: {1: 'r72', 3: 'r72'},
            66: {0: 'r45', 1: 'r45', 3: 'r45', 4: 'r45', 8: 'r45', 12: 'r45', 15: 'r45', 19: 'r45', 20: 'r45'},
            67: {0: 'r44', 1: 'r44', 3: 'r44', 4: 'r44', 8: 'r44', 12: 'r44', 15: 'r44', 19: 'r44', 20: 'r44'},
            68: {0: 'r78', 1: 'r78', 3: 'r78', 4: 'r78', 8: 'r78', 12: 'r78', 15: 'r78', 19: 'r78', 20: 'r78'},
            69: {12: 's91'},
            70: {0: 'r31', 1: 'r31', 3: 'r31', 4: 'r31', 8: 'r31', 19: 'r31', 20: 'r31'},
            71: {1: 's92', 3: 'r76'},
            72: {2: 'r79', 10: 'r79', 19: 'r79'},
            73: {4: 'r16', 8: 'r16', 12: 'r16', 15: 'r16', 19: 'r16'},
            74: {1: 'r70', 3: 'r70', 4: 'r70', 7: 'r70', 8: 'r70', 12: 'r70', 15: 'r70', 19: 'r70'},
            75: {1: 's77', 12: 'r97', 15: 'r97'},
            76: {1: 'r19', 12: 'r19', 15: 'r19'},
            77: {4: 's17', 8: 's26', 19: 's19'},
            78: {4: 's17', 8: 's26', 19: 's19'},
            79: {1: 'r59', 3: 'r59'},
            80: {19: 's97'},
            81: {19: 's97'},
            82: {1: 'r15', 3: 'r15', 4: 'r15', 7: 'r15', 8: 'r15', 12: 'r15', 15: 'r15', 16: 's48', 18: 's50', 19: 'r15'},
            83: {0: 'r49', 1: 'r49', 3: 'r49', 4: 'r49', 8: 'r49', 12: 'r49', 15: 'r49', 16: 's48', 18: 's50', 19: 'r49', 20: 'r49'},
            84: {4: 'r50', 8: 'r50', 12: 'r50', 15: 'r50', 19: 'r50', 20: 'r50'},
            85: {4: 's33', 8: 's29', 19: 's30', 20: 's28'},
            86: {1: 's85', 12: 'r95', 15: 'r95'},
            87: {1: 'r53', 12: 'r53', 15: 'r53'},
            88: {8: 'r25'},
            89: {8: 's109'},
            90: {8: 'r26'},
            91: {0: 'r68', 1: 'r68', 3: 'r68', 4: 'r68', 8: 'r68', 12: 'r68', 15: 'r68', 19: 'r68', 20: 'r68'},
            92: {0: 'r75', 1: 'r75', 3: 'r75', 4: 's33', 8: 's29', 17: 's37', 19: 's30', 20: 's28'},
            93: {1: 'r23', 3: 'r23'},
            94: {1: 'r20', 12: 'r20', 15: 'r20'},
            95: {1: 'r18', 12: 'r18', 15: 'r18'},
            96: {1: 'r58', 3: 'r58'},
            97: {6: 'r63', 11: 'r63'},
            98: {6: 's112'},
            99: {6: 's113'},
            100: {1: 'r71', 3: 'r71', 4: 'r71', 7: 'r71', 8: 'r71', 12: 'r71', 15: 'r71', 19: 'r71'},
            101: {1: 'r13', 3: 'r13', 4: 'r13', 7: 'r13', 8: 'r13', 12: 'r13', 15: 'r13', 19: 'r13'},
            102: {1: 'r14', 3: 'r14', 4: 'r14', 7: 'r14', 8: 'r14', 12: 'r14', 15: 'r14', 19: 'r14'},
            103: {0: 'r47', 1: 'r47', 3: 'r47', 4: 'r47', 8: 'r47', 12: 'r47', 15: 'r47', 19: 'r47', 20: 'r47'},
            104: {0: 'r69', 1: 'r69', 3: 'r69', 4: 'r69', 8: 'r69', 12: 'r69', 15: 'r69', 19: 'r69', 20: 'r69'},
            105: {0: 'r48', 1: 'r48', 3: 'r48', 4: 'r48', 8: 'r48', 12: 'r48', 15: 'r48', 19: 'r48', 20: 'r48'},
            106: {1: 'r52', 12: 'r52', 15: 'r52'},
            107: {1: 'r54', 12: 'r54', 15: 'r54'},
            108: {1: 'r28', 3: 'r28'},
            109: {5: 'r40', 18: 's114'},
            110: {1: 'r22', 3: 'r22'},
            111: {6: 'r85', 11: 's119'},
            112: {3: 'r55'},
            113: {1: 'r5', 3: 'r5'},
            114: {5: 'r36'},
            115: {11: 'r35', 15: 'r35'},
            116: {5: 's121'},
            117: {5: 'r39'},
            118: {6: 'r62', 11: 'r62'},
            119: {19: 's122'},
            120: {11: 's123', 15: 's125'},
            121: {1: 'r43', 3: 'r43', 8: 's109', 11: 'r43', 15: 'r43'},
            122: {6: 'r61', 11: 'r61'},
            123: {5: 'r40', 18: 's114'},
            124: {11: 'r34', 15: 'r34'},
            125: {1: 'r80', 3: 'r80', 11: 'r80', 15: 'r80'},
            126: {1: 'r41', 3: 'r41', 11: 'r41', 15: 'r41'},
            127: {1: 'r42', 3: 'r42', 11: 'r42', 15: 'r42'},
            128: {1: 'r90', 3: 'r90', 11: 'r90', 15: 'r90'},
            129: {11: 'r33', 15: 'r33'}
        }
        self.__goto_table = {
            0: {42: 5, 44: 7, 47: 3, 48: 6, 49: 2, 62: 1},
            2: {42: 5, 47: 3, 48: 6, 62: 9},
            8: {12: 15, 15: 16, 21: 13},
            10: {13: 21, 30: 18, 40: 27, 57: 22, 58: 20, 59: 25, 63: 24},
            11: {6: 38, 29: 32, 34: 35, 43: 31, 45: 39, 52: 36, 60: 34},
            13: {12: 41, 15: 16},
            17: {8: 42, 13: 44, 14: 43, 59: 25},
            19: {2: 49, 22: 47, 26: 46},
            20: {13: 51, 59: 25},
            22: {9: 52},
            23: {16: 54, 36: 53},
            24: {10: 56, 18: 58},
            26: {8: 42, 13: 44, 14: 59, 59: 25},
            29: {6: 38, 27: 60, 29: 32, 50: 61, 60: 62},
            31: {4: 65, 41: 64},
            32: {22: 67, 24: 66, 33: 68},
            33: {6: 38, 27: 69, 29: 32, 50: 61, 60: 62},
            35: {6: 38, 29: 32, 60: 70},
            36: {61: 71},
            42: {13: 73, 59: 25},
            44: {1: 75, 17: 76},
            52: {20: 79},
            61: {6: 38, 29: 32, 60: 84},
            62: {28: 87, 39: 86},
            63: {5: 90, 53: 89},
            71: {38: 93},
            75: {17: 94},
            77: {13: 95, 59: 25},
            78: {13: 21, 57: 96, 58: 20, 59: 25, 63: 24},
            80: {19: 98},
            81: {19: 99},
            82: {0: 100, 7: 102, 22: 101},
            83: {22: 103, 32: 105, 37: 104},
            85: {6: 38, 29: 32, 60: 106},
            86: {28: 107},
            89: {25: 108},
            92: {6: 38, 29: 32, 34: 35, 43: 31, 52: 110, 60: 34},
            97: {51: 111},
            109: {11: 115, 31: 116, 35: 117},
            111: {3: 118},
            115: {23: 120},
            120: {54: 124},
            121: {25: 126, 46: 128, 56: 127},
            123: {11: 129, 31: 116, 35: 117}
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
        self.__reduce_to_non_terminal_index = [49, 49, 15, 15, 18, 10, 10, 58, 58, 2, 26, 26, 7, 0, 0, 8, 8, 17, 1, 1, 12, 38, 61, 61, 5, 53, 53, 41, 4, 4, 34, 34, 54, 23, 23, 35, 21, 21, 31, 31, 56, 46, 46, 24, 33, 33, 32, 37, 37, 50, 50, 28, 39, 39, 36, 16, 16, 20, 9, 9, 3, 51, 51, 44, 22, 22, 47, 6, 6, 59, 59, 52, 43, 43, 43, 45, 60, 60, 48, 25, 13, 13, 30, 30, 19, 57, 63, 40, 42, 11, 62, 62, 62, 27, 27, 14, 14, 29, 29]

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
