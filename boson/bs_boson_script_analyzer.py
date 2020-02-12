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
                [False, {')'}, [], 2],
                [False, {'%'}, [], 3],
                [False, {'|'}, [], 4],
                [False, {' ', '\t'}, [], 5],
                [False, {'}'}, [], 6],
                [False, {';'}, [], 7],
                [False, {':'}, [], 8],
                [False, {']'}, [], 9],
                [False, {','}, [], 10],
                [False, {'@'}, [], 11],
                [False, {'='}, [], 12],
                [False, {"'"}, [], 32],
                [False, {'"'}, [], 29],
                [False, {'$'}, [], 13],
                [False, {'+'}, [], 14],
                [False, {'['}, [], 15],
                [False, {'*'}, [], 16],
                [False, {'\n'}, [], 17],
                [False, {'~'}, [], 18],
                [False, {'<'}, [], 19],
                [False, {'#'}, [], 20],
                [False, {'('}, [], 21],
                [False, {'{'}, [], 22]
            ],
            20: [
                [True, {'\r', '\n'}, [], 20]
            ],
            19: [
                [True, {'\\'}, [], 23],
                [False, {'\\'}, [], 19]
            ],
            23: [
                [True, {'>', '\\'}, [], 23],
                [False, {'>'}, [], 24],
                [False, {'\\'}, [], 19]
            ],
            24: [
                [True, {'>', '\\'}, [], 23],
                [False, {'>'}, [], 24],
                [False, {'\\'}, [], 19]
            ],
            17: [
                [False, {'\r'}, [], 25]
            ],
            13: [
                [False, set(), [('0', '9')], 26],
                [False, {'$', '@', '?'}, [], 27]
            ],
            26: [
                [False, set(), [('0', '9')], 26],
                [False, {'*'}, [], 27]
            ],
            29: [
                [True, {'\\'}, [], 28],
                [False, {'\\'}, [], 29]
            ],
            28: [
                [True, {'"', '\\'}, [], 28],
                [False, {'\\'}, [], 29],
                [False, {'"'}, [], 30]
            ],
            30: [
                [True, {'"', '\\'}, [], 28],
                [False, {'\\'}, [], 29],
                [False, {'"'}, [], 30]
            ],
            32: [
                [True, {'\\'}, [], 31],
                [False, {'\\'}, [], 32]
            ],
            31: [
                [True, {'\\', "'"}, [], 31],
                [False, {'\\'}, [], 32],
                [False, {"'"}, [], 33]
            ],
            33: [
                [True, {'\\', "'"}, [], 31],
                [False, {'\\'}, [], 32],
                [False, {"'"}, [], 33]
            ],
            5: [
                [False, {' ', '\t'}, [], 5]
            ],
            3: [
                [False, {'_'}, [('A', 'Z'), ('a', 'z')], 34]
            ],
            34: [
                [False, {'_'}, [('A', 'Z'), ('a', 'z')], 34]
            ],
            1: [
                [False, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 1]
            ]
        }
        self.__character_set = {'y', 'a', '>', 'e', 'Y', 'o', 'N', ')', 'X', 'p', 'i', '5', '%', 'C', 'q', 'B', '|', 'D', 'Z', 'M', '1', 'J', '0', '9', ' ', 'k', '4', 'E', '_', 'K', 'u', 'H', '?', '}', 'b', 'G', 'l', ';', ':', ']', '\\', 'W', ',', '@', '=', "'", 'd', 'n', 'P', 'I', 'Q', '"', '$', '6', '7', '3', '\t', 'v', '+', 'F', '[', 'f', 'w', '\r', 't', 'm', 'r', 'S', '*', '2', 'z', 'x', 'V', 'R', 's', 'j', 'h', 'U', '8', 'A', 'T', 'g', 'O', 'c', '\n', '~', '<', '#', '(', 'L', '{'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 20, 21, 22, 24, 25, 26, 27, 30, 33, 34}
        self.__lexical_symbol_mapping = {
            1: 'name',
            2: 'parentheses_r',
            4: 'or',
            5: 'skip',
            6: 'brace_r',
            7: 'end',
            8: 'reduce',
            9: 'bracket_r',
            10: 'comma',
            11: 'at',
            12: 'assign',
            14: 'plus',
            15: 'bracket_l',
            16: 'star',
            17: 'newline',
            18: 'null',
            20: 'comment',
            21: 'parentheses_l',
            22: 'brace_l',
            24: 'regular_expression',
            25: 'newline',
            26: 'node',
            27: 'node',
            30: 'string',
            33: 'string',
            34: 'command'
        }
        self.__symbol_function_mapping = {
            'skip': ['!skip'],
            'newline': ['!skip', '!newline']
        }
        self.__lexical_function = {
            '!skip': self._lexical_function_skip,
            '!newline': self._lexical_function_newline,
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
                        if True in character_set and condition not in self.__character_set:
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
            'end': 0,
            'reduce': 1,
            '$': 2,
            'node': 3,
            'brace_r': 4,
            'assign': 5,
            'at': 6,
            'or': 7,
            'bracket_r': 8,
            'command': 9,
            'star': 10,
            'comma': 11,
            'regular_expression': 12,
            'parentheses_r': 13,
            'plus': 14,
            'parentheses_l': 15,
            'name': 16,
            'null': 17,
            'brace_l': 18,
            'string': 19,
            'bracket_l': 20
        }
        self.__action_table = {
            0: {9: 's6', 16: 's5'},
            1: {2: 'r91', 9: 'r91', 16: 'r91'},
            2: {2: 'r64', 9: 's6', 16: 's5'},
            3: {2: 'r92', 9: 'r92', 16: 'r92'},
            4: {2: 'r93', 9: 'r93', 16: 'r93'},
            5: {1: 's11', 5: 's10'},
            6: {16: 's15', 19: 's16'},
            7: {2: 'r2', 9: 'r2', 16: 'r2'},
            8: {2: 'a'},
            9: {2: 'r1', 9: 'r1', 16: 'r1'},
            10: {12: 's25', 15: 's27', 16: 's18', 20: 's19'},
            11: {0: 'r75', 5: 'r75', 7: 'r75', 15: 's30', 16: 's37', 17: 's34', 19: 's31', 20: 's33'},
            12: {0: 'r37', 16: 'r37', 19: 'r37'},
            13: {0: 'r21', 16: 'r21', 19: 'r21'},
            14: {0: 's41', 16: 's15', 19: 's16'},
            15: {0: 'r3', 16: 'r3', 19: 'r3'},
            16: {0: 'r4', 16: 'r4', 19: 'r4'},
            17: {0: 'r7', 6: 's42', 7: 'r7'},
            18: {0: 'r12', 6: 'r12', 7: 'r12', 8: 'r12', 10: 's48', 13: 'r12', 14: 's49', 15: 'r12', 16: 'r12', 20: 'r12'},
            19: {15: 's27', 16: 's18', 20: 's19'},
            20: {0: 'r87', 6: 'r87', 7: 'r87', 15: 's27', 16: 's18', 20: 's19'},
            21: {0: 'r83'},
            22: {0: 's54'},
            23: {0: 'r81', 6: 'r81', 7: 'r81', 8: 'r81', 13: 'r81', 15: 'r81', 16: 'r81', 20: 'r81'},
            24: {0: 'r60', 7: 'r60'},
            25: {0: 'r57', 6: 's57'},
            26: {0: 'r9', 6: 'r9', 7: 'r9', 15: 'r9', 16: 'r9', 20: 'r9'},
            27: {15: 's27', 16: 's18', 20: 's19'},
            28: {0: 'r30', 5: 's60', 7: 'r30'},
            29: {0: 'r73', 5: 'r73', 7: 'r73', 15: 's30', 16: 's37', 19: 's31', 20: 's33'},
            30: {15: 's30', 16: 's37', 19: 's31', 20: 's33'},
            31: {0: 'r99', 5: 'r99', 7: 'r99', 8: 'r99', 10: 'r99', 13: 'r99', 14: 'r99', 15: 'r99', 16: 'r99', 19: 'r99', 20: 'r99'},
            32: {0: 'r77', 5: 'r77', 7: 'r77', 8: 'r77', 13: 'r77', 15: 'r77', 16: 'r77', 19: 'r77', 20: 'r77'},
            33: {15: 's30', 16: 's37', 19: 's31', 20: 's33'},
            34: {0: 'r74', 5: 'r74', 7: 'r74'},
            35: {0: 's68'},
            36: {0: 'r46', 5: 'r46', 7: 'r46', 8: 'r46', 10: 's48', 13: 'r46', 14: 's49', 15: 'r46', 16: 'r46', 19: 'r46', 20: 'r46'},
            37: {0: 'r98', 5: 'r98', 7: 'r98', 8: 'r98', 10: 'r98', 13: 'r98', 14: 'r98', 15: 'r98', 16: 'r98', 19: 'r98', 20: 'r98'},
            38: {0: 'r24', 7: 'r24'},
            39: {0: 'r32', 5: 'r32', 7: 'r32', 15: 'r32', 16: 'r32', 19: 'r32', 20: 'r32'},
            40: {0: 'r38', 16: 'r38', 19: 'r38'},
            41: {2: 'r67', 9: 'r67', 16: 'r67'},
            42: {18: 's73'},
            43: {0: 'r86', 7: 'r86'},
            44: {0: 'r6', 7: 'r6'},
            45: {0: 'r82', 6: 'r82', 7: 'r82', 8: 'r82', 13: 'r82', 15: 'r82', 16: 'r82', 20: 'r82'},
            46: {0: 'r11', 6: 'r11', 7: 'r11', 8: 'r11', 13: 'r11', 15: 'r11', 16: 'r11', 20: 'r11'},
            47: {0: 'r10', 6: 'r10', 7: 'r10', 8: 'r10', 13: 'r10', 15: 'r10', 16: 'r10', 20: 'r10'},
            48: {0: 'r66', 5: 'r66', 6: 'r66', 7: 'r66', 8: 'r66', 13: 'r66', 15: 'r66', 16: 'r66', 19: 'r66', 20: 'r66'},
            49: {0: 'r65', 5: 'r65', 6: 'r65', 7: 'r65', 8: 'r65', 13: 'r65', 15: 'r65', 16: 'r65', 19: 'r65', 20: 'r65'},
            50: {7: 's75', 8: 'r17', 13: 'r17', 15: 'r17', 16: 'r17', 20: 'r17'},
            51: {8: 'r96', 13: 'r96', 15: 's27', 16: 's18', 20: 's19'},
            52: {8: 's78'},
            53: {0: 'r8', 6: 'r8', 7: 'r8', 15: 'r8', 16: 'r8', 20: 'r8'},
            54: {2: 'r89', 9: 'r89', 16: 'r89'},
            55: {0: 'r88', 7: 's79'},
            56: {0: 'r56'},
            57: {18: 's81'},
            58: {0: 'r84'},
            59: {13: 's82'},
            60: {15: 'r27', 16: 's84'},
            61: {0: 'r72', 7: 'r72'},
            62: {0: 'r29', 7: 'r29'},
            63: {0: 'r31', 5: 'r31', 7: 'r31', 15: 'r31', 16: 'r31', 19: 'r31', 20: 'r31'},
            64: {13: 's86'},
            65: {7: 's87', 8: 'r51', 13: 'r51', 15: 'r51', 16: 'r51', 19: 'r51', 20: 'r51'},
            66: {8: 'r94', 13: 'r94', 15: 's30', 16: 's37', 19: 's31', 20: 's33'},
            67: {8: 's91'},
            68: {2: 'r79', 9: 'r79', 16: 'r79'},
            69: {0: 'r78', 5: 'r78', 7: 'r78', 8: 'r78', 13: 'r78', 15: 'r78', 16: 'r78', 19: 'r78', 20: 'r78'},
            70: {0: 'r44', 5: 'r44', 7: 'r44', 8: 'r44', 13: 'r44', 15: 'r44', 16: 'r44', 19: 'r44', 20: 'r44'},
            71: {0: 'r45', 5: 'r45', 7: 'r45', 8: 'r45', 13: 'r45', 15: 'r45', 16: 'r45', 19: 'r45', 20: 'r45'},
            72: {0: 'r76', 7: 's93'},
            73: {16: 's95'},
            74: {7: 's75', 8: 'r97', 13: 'r97'},
            75: {15: 's27', 16: 's18', 20: 's19'},
            76: {7: 'r19', 8: 'r19', 13: 'r19'},
            77: {8: 'r16', 13: 'r16', 15: 'r16', 16: 'r16', 20: 'r16'},
            78: {0: 'r70', 6: 'r70', 7: 'r70', 8: 'r70', 13: 'r70', 15: 'r70', 16: 'r70', 20: 'r70'},
            79: {15: 's27', 16: 's18', 20: 's19'},
            80: {0: 'r59', 7: 'r59'},
            81: {16: 's95'},
            82: {0: 'r15', 6: 'r15', 7: 'r15', 8: 'r15', 10: 's48', 13: 'r15', 14: 's49', 15: 'r15', 16: 'r15', 20: 'r15'},
            83: {15: 'r26'},
            84: {15: 'r25'},
            85: {15: 's104'},
            86: {0: 'r49', 5: 'r49', 7: 'r49', 8: 'r49', 10: 's48', 13: 'r49', 14: 's49', 15: 'r49', 16: 'r49', 19: 'r49', 20: 'r49'},
            87: {15: 's30', 16: 's37', 19: 's31', 20: 's33'},
            88: {7: 's87', 8: 'r95', 13: 'r95'},
            89: {7: 'r53', 8: 'r53', 13: 'r53'},
            90: {8: 'r50', 13: 'r50', 15: 'r50', 16: 'r50', 19: 'r50', 20: 'r50'},
            91: {0: 'r68', 5: 'r68', 7: 'r68', 8: 'r68', 13: 'r68', 15: 'r68', 16: 'r68', 19: 'r68', 20: 'r68'},
            92: {0: 'r23', 7: 'r23'},
            93: {0: 'r75', 5: 'r75', 7: 'r75', 15: 's30', 16: 's37', 17: 's34', 19: 's31', 20: 's33'},
            94: {4: 's111'},
            95: {4: 'r63', 11: 'r63'},
            96: {7: 'r20', 8: 'r20', 13: 'r20'},
            97: {7: 'r18', 8: 'r18', 13: 'r18'},
            98: {0: 'r58', 7: 'r58'},
            99: {4: 's113'},
            100: {0: 'r13', 6: 'r13', 7: 'r13', 8: 'r13', 13: 'r13', 15: 'r13', 16: 'r13', 20: 'r13'},
            101: {0: 'r71', 6: 'r71', 7: 'r71', 8: 'r71', 13: 'r71', 15: 'r71', 16: 'r71', 20: 'r71'},
            102: {0: 'r14', 6: 'r14', 7: 'r14', 8: 'r14', 13: 'r14', 15: 'r14', 16: 'r14', 20: 'r14'},
            103: {0: 'r28', 7: 'r28'},
            104: {3: 'r40', 10: 's114'},
            105: {0: 'r69', 5: 'r69', 7: 'r69', 8: 'r69', 13: 'r69', 15: 'r69', 16: 'r69', 19: 'r69', 20: 'r69'},
            106: {0: 'r47', 5: 'r47', 7: 'r47', 8: 'r47', 13: 'r47', 15: 'r47', 16: 'r47', 19: 'r47', 20: 'r47'},
            107: {0: 'r48', 5: 'r48', 7: 'r48', 8: 'r48', 13: 'r48', 15: 'r48', 16: 'r48', 19: 'r48', 20: 'r48'},
            108: {7: 'r52', 8: 'r52', 13: 'r52'},
            109: {7: 'r54', 8: 'r54', 13: 'r54'},
            110: {0: 'r22', 7: 'r22'},
            111: {0: 'r5', 7: 'r5'},
            112: {4: 'r85', 11: 's118'},
            113: {0: 'r55'},
            114: {3: 'r36'},
            115: {11: 'r35', 13: 'r35'},
            116: {3: 'r39'},
            117: {3: 's121'},
            118: {16: 's122'},
            119: {4: 'r62', 11: 'r62'},
            120: {11: 's124', 13: 's123'},
            121: {0: 'r43', 7: 'r43', 11: 'r43', 13: 'r43', 15: 's104'},
            122: {4: 'r61', 11: 'r61'},
            123: {0: 'r80', 7: 'r80', 11: 'r80', 13: 'r80'},
            124: {3: 'r40', 10: 's114'},
            125: {11: 'r34', 13: 'r34'},
            126: {0: 'r42', 7: 'r42', 11: 'r42', 13: 'r42'},
            127: {0: 'r90', 7: 'r90', 11: 'r90', 13: 'r90'},
            128: {0: 'r41', 7: 'r41', 11: 'r41', 13: 'r41'},
            129: {11: 'r33', 13: 'r33'}
        }
        self.__goto_table = {
            0: {23: 7, 27: 1, 30: 4, 44: 2, 46: 3, 53: 8},
            2: {23: 9, 27: 1, 30: 4, 46: 3},
            6: {6: 12, 18: 14, 33: 13},
            10: {1: 26, 4: 22, 24: 23, 31: 24, 41: 20, 56: 17, 59: 21},
            11: {0: 36, 10: 38, 12: 32, 14: 39, 28: 29, 42: 28, 55: 35},
            14: {6: 40, 33: 13},
            17: {26: 44, 39: 43},
            18: {9: 47, 11: 46, 52: 45},
            19: {1: 50, 24: 23, 32: 51, 62: 52},
            20: {1: 53, 24: 23},
            24: {58: 55},
            25: {20: 58, 60: 56},
            27: {1: 50, 24: 23, 32: 51, 62: 59},
            28: {8: 61, 25: 62},
            29: {0: 36, 12: 32, 14: 63},
            30: {0: 36, 7: 64, 12: 32, 14: 65, 15: 66},
            33: {0: 36, 7: 67, 12: 32, 14: 65, 15: 66},
            36: {9: 70, 19: 71, 38: 69},
            38: {54: 72},
            50: {34: 76, 43: 74},
            51: {1: 77, 24: 23},
            55: {21: 80},
            60: {22: 85, 35: 83},
            65: {47: 89, 63: 88},
            66: {0: 36, 12: 32, 14: 90},
            72: {37: 92},
            73: {49: 94},
            74: {34: 96},
            75: {1: 97, 24: 23},
            79: {1: 26, 24: 23, 31: 98, 41: 20, 56: 17},
            81: {49: 99},
            82: {9: 100, 16: 102, 57: 101},
            85: {45: 103},
            86: {2: 105, 9: 106, 17: 107},
            87: {0: 36, 12: 32, 14: 108},
            88: {47: 109},
            93: {0: 36, 10: 110, 12: 32, 14: 39, 28: 29, 42: 28},
            95: {51: 112},
            104: {29: 115, 36: 117, 40: 116},
            112: {48: 119},
            115: {50: 120},
            120: {61: 125},
            121: {3: 126, 5: 127, 45: 128},
            124: {29: 129, 36: 117, 40: 116}
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
        self.__reduce_to_non_terminal_index = [44, 44, 33, 33, 26, 39, 39, 41, 41, 11, 52, 52, 16, 57, 57, 32, 32, 34, 43, 43, 6, 37, 54, 54, 35, 22, 22, 25, 8, 8, 28, 28, 61, 50, 50, 40, 18, 18, 36, 36, 3, 5, 5, 19, 38, 38, 17, 2, 2, 15, 15, 47, 63, 63, 60, 20, 20, 21, 58, 58, 48, 51, 51, 53, 9, 9, 27, 12, 12, 24, 24, 10, 42, 42, 42, 55, 14, 14, 46, 45, 1, 1, 4, 4, 49, 31, 56, 59, 30, 29, 23, 23, 23, 7, 7, 62, 62, 0, 0]

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
            64: 34,
            65: 35
        }
        self.__naive_reduce_number = {64, 97, 2, 3, 65, 98, 73, 74, 76, 80, 82, 90, 91, 92}
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
