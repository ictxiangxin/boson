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
                [0, {'"'}, [], 1],
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 2],
                [0, {'%'}, [], 3],
                [0, {'@'}, [], 4],
                [0, {','}, [], 5],
                [0, {"'"}, [], 31],
                [0, {'#'}, [], 6],
                [0, {'~'}, [], 7],
                [0, {'{'}, [], 8],
                [0, {'['}, [], 9],
                [0, {'='}, [], 10],
                [0, {'\t', ' '}, [], 11],
                [0, {'$'}, [], 12],
                [0, {'\n'}, [], 13],
                [0, {'}'}, [], 14],
                [0, {':'}, [], 15],
                [0, {'!'}, [], 16],
                [0, {';'}, [], 17],
                [0, {'*'}, [], 18],
                [0, {'|'}, [], 19],
                [0, {')'}, [], 20],
                [0, {'+'}, [], 21],
                [0, {'('}, [], 22],
                [0, {']'}, [], 23],
                [0, {'<'}, [], 25]
            ],
            25: [
                [2, {'\\'}, [], 24],
                [0, {'\\'}, [], 25]
            ],
            24: [
                [2, {'\\', '>'}, [], 24],
                [0, {'\\'}, [], 25],
                [0, {'>'}, [], 26]
            ],
            26: [
                [2, {'\\', '>'}, [], 24],
                [0, {'\\'}, [], 25],
                [0, {'>'}, [], 26]
            ],
            13: [
                [0, {'\r'}, [], 27]
            ],
            12: [
                [0, set(), [('0', '9')], 28],
                [0, {'?', '$', '@'}, [], 29]
            ],
            28: [
                [0, set(), [('0', '9')], 28]
            ],
            11: [
                [0, {'\t', ' '}, [], 11]
            ],
            6: [
                [2, {'\n', '\r'}, [], 6]
            ],
            31: [
                [2, {'\\'}, [], 30],
                [0, {'\\'}, [], 31]
            ],
            30: [
                [2, {'\\', "'"}, [], 30],
                [0, {'\\'}, [], 31],
                [0, {"'"}, [], 32]
            ],
            32: [
                [2, {'\\', "'"}, [], 30],
                [0, {'\\'}, [], 31],
                [0, {"'"}, [], 32]
            ],
            3: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 33]
            ],
            33: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 33]
            ],
            2: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 2]
            ],
            1: [
                [2, {'\\'}, [], 34],
                [0, {'\\'}, [], 1]
            ],
            34: [
                [2, {'"', '\\'}, [], 34],
                [0, {'"'}, [], 35],
                [0, {'\\'}, [], 1]
            ],
            35: [
                [2, {'"', '\\'}, [], 34],
                [0, {'"'}, [], 35],
                [0, {'\\'}, [], 1]
            ]
        }
        self.__character_set = {'"', 'Q', 'r', '@', '%', ',', 'e', 'i', 'M', '\\', 'w', 'W', 'q', 'v', 'L', '\r', 'k', 'd', "'", '>', 'x', 'I', 'N', '#', '~', 'O', 'Y', '{', '8', 'y', 'J', '[', 'H', '3', 'T', '=', '7', 'U', '?', ' ', 'X', 'z', 'R', 'o', '9', 'c', 'A', 'Z', 'a', 'b', 'g', 'B', 'P', '$', 'E', '_', 'f', '\n', 'l', 'h', '}', '2', '5', 'C', ':', 'j', 'p', 't', 'S', '6', '!', '1', ';', 'm', '*', '|', 'K', ')', '\t', 'V', 'u', 'n', 's', '+', 'F', 'G', '(', '4', ']', 'D', '0', '<'}
        self.__start_state = 0
        self.__end_state_set = {2, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 26, 27, 28, 29, 32, 33, 35}
        self.__lexical_symbol_mapping = {
            2: 'name',
            4: '!symbol_4',
            5: '!symbol_8',
            6: 'comment',
            7: '!symbol_14',
            8: '!symbol_5',
            9: '!symbol_11',
            10: '!symbol_2',
            11: 'skip',
            13: 'newline',
            14: '!symbol_6',
            15: '!symbol_13',
            16: '!symbol_3',
            17: '!symbol_1',
            18: '!symbol_15',
            19: '!symbol_7',
            20: '!symbol_10',
            21: '!symbol_16',
            22: '!symbol_9',
            23: '!symbol_12',
            26: 'regular',
            27: 'newline',
            28: 'node',
            29: 'node',
            32: 'string',
            33: 'command',
            35: 'string'
        }
        self.__non_greedy_state_set = {32, 26, 35}
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
            '!symbol_5': 0,
            '!symbol_14': 1,
            '!symbol_9': 2,
            '!symbol_7': 3,
            '!symbol_3': 4,
            '$': 5,
            '!symbol_12': 6,
            '!symbol_16': 7,
            '!symbol_2': 8,
            'string': 9,
            'regular': 10,
            '!symbol_15': 11,
            'command': 12,
            '!symbol_8': 13,
            'node': 14,
            '!symbol_11': 15,
            '!symbol_4': 16,
            '!symbol_6': 17,
            '!symbol_1': 18,
            '!symbol_13': 19,
            '!symbol_10': 20,
            'name': 21
        }
        self.__action_table = {
            0: {12: 's3', 21: 's4'},
            1: {5: 'r2', 12: 'r2', 21: 'r2'},
            2: {5: 'r95', 12: 'r95', 21: 'r95'},
            3: {9: 's12', 21: 's11'},
            4: {8: 's15', 19: 's14'},
            5: {5: 'r67', 12: 's3', 21: 's4'},
            6: {5: 'r96', 12: 'r96', 21: 'r96'},
            7: {5: 'a'},
            8: {5: 'r94', 12: 'r94', 21: 'r94'},
            9: {9: 's12', 18: 's18', 21: 's11'},
            10: {9: 'r21', 18: 'r21', 21: 'r21'},
            11: {9: 'r3', 18: 'r3', 21: 'r3'},
            12: {9: 'r4', 18: 'r4', 21: 'r4'},
            13: {9: 'r37', 18: 'r37', 21: 'r37'},
            14: {1: 's30', 2: 's19', 3: 'r78', 8: 'r78', 9: 's20', 15: 's29', 18: 'r78', 21: 's27'},
            15: {2: 's37', 10: 's34', 15: 's35', 21: 's39'},
            16: {5: 'r1', 12: 'r1', 21: 'r1'},
            17: {9: 'r38', 18: 'r38', 21: 'r38'},
            18: {5: 'r70', 12: 'r70', 21: 'r70'},
            19: {2: 's19', 9: 's20', 15: 's29', 21: 's27'},
            20: {2: 'r102', 3: 'r102', 6: 'r102', 7: 'r102', 8: 'r102', 9: 'r102', 11: 'r102', 15: 'r102', 18: 'r102', 20: 'r102', 21: 'r102'},
            21: {3: 'r33', 8: 's46', 18: 'r33'},
            22: {2: 's19', 3: 'r76', 8: 'r76', 9: 's20', 15: 's29', 18: 'r76', 21: 's27'},
            23: {3: 'r27', 18: 'r27'},
            24: {2: 'r35', 3: 'r35', 8: 'r35', 9: 'r35', 15: 'r35', 18: 'r35', 21: 'r35'},
            25: {2: 'r80', 3: 'r80', 6: 'r80', 8: 'r80', 9: 'r80', 15: 'r80', 18: 'r80', 20: 'r80', 21: 'r80'},
            26: {2: 'r49', 3: 'r49', 6: 'r49', 7: 's52', 8: 'r49', 9: 'r49', 11: 's53', 15: 'r49', 18: 'r49', 20: 'r49', 21: 'r49'},
            27: {2: 'r101', 3: 'r101', 6: 'r101', 7: 'r101', 8: 'r101', 9: 'r101', 11: 'r101', 15: 'r101', 18: 'r101', 20: 'r101', 21: 'r101'},
            28: {18: 's55'},
            29: {2: 's19', 9: 's20', 15: 's29', 21: 's27'},
            30: {3: 'r77', 8: 'r77', 18: 'r77'},
            31: {2: 's37', 3: 'r90', 15: 's35', 16: 'r90', 18: 'r90', 21: 's39'},
            32: {2: 'r84', 3: 'r84', 6: 'r84', 15: 'r84', 16: 'r84', 18: 'r84', 20: 'r84', 21: 'r84'},
            33: {18: 'r86'},
            34: {4: 's60', 16: 'r60', 18: 'r60'},
            35: {2: 's37', 15: 's35', 21: 's39'},
            36: {18: 's64'},
            37: {2: 's37', 15: 's35', 21: 's39'},
            38: {3: 'r10', 16: 's66', 18: 'r10'},
            39: {2: 'r15', 3: 'r15', 6: 'r15', 7: 's52', 11: 's53', 15: 'r15', 16: 'r15', 18: 'r15', 20: 'r15', 21: 'r15'},
            40: {3: 'r66', 18: 'r66'},
            41: {2: 'r12', 3: 'r12', 15: 'r12', 16: 'r12', 18: 'r12', 21: 'r12'},
            42: {2: 's19', 6: 'r97', 9: 's20', 15: 's29', 20: 'r97', 21: 's27'},
            43: {2: 'r54', 3: 's74', 6: 'r54', 9: 'r54', 15: 'r54', 20: 'r54', 21: 'r54'},
            44: {20: 's77'},
            45: {3: 'r75', 18: 'r75'},
            46: {2: 'r30', 21: 's78'},
            47: {3: 'r32', 18: 'r32'},
            48: {2: 'r34', 3: 'r34', 8: 'r34', 9: 'r34', 15: 'r34', 18: 'r34', 21: 'r34'},
            49: {3: 's82', 18: 'r79'},
            50: {2: 'r47', 3: 'r47', 6: 'r47', 8: 'r47', 9: 'r47', 15: 'r47', 18: 'r47', 20: 'r47', 21: 'r47'},
            51: {2: 'r81', 3: 'r81', 6: 'r81', 8: 'r81', 9: 'r81', 15: 'r81', 18: 'r81', 20: 'r81', 21: 'r81'},
            52: {2: 'r69', 3: 'r69', 6: 'r69', 8: 'r69', 9: 'r69', 15: 'r69', 16: 'r69', 18: 'r69', 20: 'r69', 21: 'r69'},
            53: {2: 'r68', 3: 'r68', 6: 'r68', 8: 'r68', 9: 'r68', 15: 'r68', 16: 'r68', 18: 'r68', 20: 'r68', 21: 'r68'},
            54: {2: 'r48', 3: 'r48', 6: 'r48', 8: 'r48', 9: 'r48', 15: 'r48', 18: 'r48', 20: 'r48', 21: 'r48'},
            55: {5: 'r82', 12: 'r82', 21: 'r82'},
            56: {6: 's83'},
            57: {2: 'r11', 3: 'r11', 15: 'r11', 16: 'r11', 18: 'r11', 21: 'r11'},
            58: {16: 's84', 18: 'r63'},
            59: {16: 'r59', 18: 'r59'},
            60: {16: 'r55', 18: 'r55'},
            61: {2: 's37', 6: 'r99', 15: 's35', 20: 'r99', 21: 's39'},
            62: {6: 's88'},
            63: {2: 'r20', 3: 's89', 6: 'r20', 15: 'r20', 20: 'r20', 21: 'r20'},
            64: {5: 'r92', 12: 'r92', 21: 'r92'},
            65: {20: 's92'},
            66: {0: 's93'},
            67: {3: 'r89', 18: 'r89'},
            68: {3: 'r9', 18: 'r9'},
            69: {2: 'r85', 3: 'r85', 6: 'r85', 15: 'r85', 16: 'r85', 18: 'r85', 20: 'r85', 21: 'r85'},
            70: {2: 'r14', 3: 'r14', 6: 'r14', 15: 'r14', 16: 'r14', 18: 'r14', 20: 'r14', 21: 'r14'},
            71: {2: 'r13', 3: 'r13', 6: 'r13', 15: 'r13', 16: 'r13', 18: 'r13', 20: 'r13', 21: 'r13'},
            72: {3: 's95', 18: 'r91'},
            73: {2: 'r53', 6: 'r53', 9: 'r53', 15: 'r53', 20: 'r53', 21: 'r53'},
            74: {2: 's19', 9: 's20', 15: 's29', 21: 's27'},
            75: {3: 's74', 6: 'r98', 20: 'r98'},
            76: {3: 'r57', 6: 'r57', 20: 'r57'},
            77: {2: 'r52', 3: 'r52', 6: 'r52', 7: 's52', 8: 'r52', 9: 'r52', 11: 's53', 15: 'r52', 18: 'r52', 20: 'r52', 21: 'r52'},
            78: {2: 'r28'},
            79: {2: 'r29'},
            80: {2: 's102'},
            81: {3: 'r26', 18: 'r26'},
            82: {1: 's30', 2: 's19', 3: 'r78', 8: 'r78', 9: 's20', 15: 's29', 18: 'r78', 21: 's27'},
            83: {2: 'r71', 3: 'r71', 6: 'r71', 8: 'r71', 9: 'r71', 15: 'r71', 18: 'r71', 20: 'r71', 21: 'r71'},
            84: {0: 's104'},
            85: {18: 'r62'},
            86: {18: 'r87'},
            87: {2: 'r19', 6: 'r19', 15: 'r19', 20: 'r19', 21: 'r19'},
            88: {2: 'r73', 3: 'r73', 6: 'r73', 15: 'r73', 16: 'r73', 18: 'r73', 20: 'r73', 21: 'r73'},
            89: {2: 's37', 15: 's35', 21: 's39'},
            90: {3: 'r23', 6: 'r23', 20: 'r23'},
            91: {3: 's89', 6: 'r100', 20: 'r100'},
            92: {2: 'r18', 3: 'r18', 6: 'r18', 7: 's52', 11: 's53', 15: 'r18', 16: 'r18', 18: 'r18', 20: 'r18', 21: 'r18'},
            93: {21: 's111'},
            94: {3: 'r65', 18: 'r65'},
            95: {2: 's37', 15: 's35', 21: 's39'},
            96: {3: 'r56', 6: 'r56', 20: 'r56'},
            97: {3: 'r58', 6: 'r58', 20: 'r58'},
            98: {2: 'r72', 3: 'r72', 6: 'r72', 8: 'r72', 9: 'r72', 15: 'r72', 18: 'r72', 20: 'r72', 21: 'r72'},
            99: {2: 'r51', 3: 'r51', 6: 'r51', 8: 'r51', 9: 'r51', 15: 'r51', 18: 'r51', 20: 'r51', 21: 'r51'},
            100: {2: 'r50', 3: 'r50', 6: 'r50', 8: 'r50', 9: 'r50', 15: 'r50', 18: 'r50', 20: 'r50', 21: 'r50'},
            101: {3: 'r31', 18: 'r31'},
            102: {11: 's115', 14: 'r43'},
            103: {3: 'r25', 18: 'r25'},
            104: {21: 's111'},
            105: {3: 'r22', 6: 'r22', 20: 'r22'},
            106: {3: 'r24', 6: 'r24', 20: 'r24'},
            107: {2: 'r74', 3: 'r74', 6: 'r74', 15: 'r74', 16: 'r74', 18: 'r74', 20: 'r74', 21: 'r74'},
            108: {2: 'r17', 3: 'r17', 6: 'r17', 15: 'r17', 16: 'r17', 18: 'r17', 20: 'r17', 21: 'r17'},
            109: {2: 'r16', 3: 'r16', 6: 'r16', 15: 'r16', 16: 'r16', 18: 'r16', 20: 'r16', 21: 'r16'},
            110: {17: 's118'},
            111: {13: 'r7', 17: 'r7'},
            112: {3: 'r64', 18: 'r64'},
            113: {14: 's120'},
            114: {14: 'r42'},
            115: {14: 'r41'},
            116: {13: 'r40', 20: 'r40'},
            117: {17: 's122'},
            118: {3: 'r8', 18: 'r8'},
            119: {13: 's124', 17: 'r88'},
            120: {2: 's102', 3: 'r46', 13: 'r46', 18: 'r46', 20: 'r46'},
            121: {13: 's130', 20: 's128'},
            122: {18: 'r61'},
            123: {13: 'r6', 17: 'r6'},
            124: {21: 's131'},
            125: {3: 'r45', 13: 'r45', 18: 'r45', 20: 'r45'},
            126: {3: 'r93', 13: 'r93', 18: 'r93', 20: 'r93'},
            127: {3: 'r44', 13: 'r44', 18: 'r44', 20: 'r44'},
            128: {3: 'r83', 13: 'r83', 18: 'r83', 20: 'r83'},
            129: {13: 'r39', 20: 'r39'},
            130: {11: 's115', 14: 'r43'},
            131: {13: 'r5', 17: 'r5'},
            132: {13: 'r36', 20: 'r36'}
        }
        self.__goto_table = {
            0: {31: 1, 45: 7, 53: 8, 56: 6, 61: 5, 63: 2},
            3: {6: 9, 11: 13, 30: 10},
            5: {31: 16, 53: 8, 56: 6, 63: 2},
            9: {11: 17, 30: 10},
            14: {3: 28, 15: 25, 29: 23, 32: 24, 35: 26, 38: 21, 40: 22},
            15: {2: 36, 4: 31, 18: 41, 20: 33, 24: 40, 41: 38, 46: 32},
            19: {15: 25, 21: 42, 32: 43, 35: 26, 54: 44},
            21: {33: 47, 65: 45},
            22: {15: 25, 32: 48, 35: 26},
            23: {39: 49},
            26: {9: 50, 22: 54, 44: 51},
            29: {15: 25, 21: 42, 32: 43, 35: 26, 54: 56},
            31: {18: 57, 46: 32},
            34: {8: 59, 52: 58},
            35: {17: 62, 18: 63, 26: 61, 46: 32},
            37: {17: 65, 18: 63, 26: 61, 46: 32},
            38: {7: 67, 16: 68},
            39: {9: 71, 10: 69, 13: 70},
            40: {55: 72},
            42: {15: 25, 32: 73, 35: 26},
            43: {57: 76, 60: 75},
            46: {5: 79, 48: 80},
            49: {23: 81},
            58: {34: 85, 49: 86},
            61: {18: 87, 46: 32},
            63: {36: 90, 51: 91},
            72: {50: 94},
            74: {15: 25, 32: 96, 35: 26},
            75: {57: 97},
            77: {9: 100, 42: 99, 59: 98},
            80: {64: 101},
            82: {15: 25, 29: 103, 32: 24, 35: 26, 38: 21, 40: 22},
            89: {18: 105, 46: 32},
            91: {36: 106},
            92: {9: 109, 14: 107, 27: 108},
            93: {37: 110},
            95: {4: 31, 18: 41, 24: 112, 41: 38, 46: 32},
            102: {0: 113, 12: 114, 28: 116},
            104: {37: 117},
            111: {58: 119},
            116: {43: 121},
            119: {1: 123},
            120: {19: 126, 62: 125, 64: 127},
            121: {47: 129},
            130: {0: 113, 12: 114, 28: 132}
        }
        self.__node_table = {
            0: ('*0', '1'),
            37: ('*0', '1'),
            69: ('0', ('*1', ('?',))),
            91: ('0', '2'),
            59: (),
            62: (),
            86: ('0', ('*1', ('?',)), ('2', ('*2',))),
            64: ('*0', '1'),
            65: (),
            90: ('0', ('*1', ('1',))),
            5: ('*0', '1'),
            6: (),
            87: ('0', ('*1', ('1',))),
            9: (),
            88: ('0', ('1', ('*2',))),
            10: ('*0', '1'),
            89: ('*0',),
            14: (),
            84: ('0', ('*1', ('?',))),
            17: (),
            73: ('1', ('*3', ('?',))),
            72: ('1',),
            18: ('*0', '1'),
            23: ('*0', '1'),
            98: ('*0',),
            99: ('0', ('*1', ('1',))),
            81: ('0', '2'),
            25: ('*0', '1'),
            26: (),
            78: ('0', ('*1', ('1',))),
            29: (),
            32: (),
            74: ('0', ('*1', (('*1', ('?',)), '2'))),
            33: ('*0', '1'),
            75: ('*0',),
            38: ('*0', '1'),
            39: (),
            82: ('1', ('*2', ('1',))),
            42: (),
            45: (),
            92: (('*0', ('?',)), '1', ('*2', ('?',))),
            48: (),
            80: ('0', ('*1', ('?',))),
            101: ('0',),
            51: (),
            71: ('1', ('*3', ('?',))),
            70: ('1',),
            52: ('*0', '1'),
            57: ('*0', '1'),
            96: ('*0',),
            97: ('0', ('*1', ('1',)))
        }
        self.__reduce_symbol_sum = [2, 1, 1, 1, 2, 2, 0, 4, 1, 0, 2, 1, 1, 1, 0, 1, 1, 0, 2, 1, 1, 2, 1, 2, 2, 2, 0, 1, 1, 0, 3, 1, 0, 2, 1, 2, 1, 2, 2, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 2, 1, 1, 2, 1, 2, 1, 0, 4, 1, 0, 2, 2, 0, 1, 1, 1, 3, 3, 4, 3, 4, 2, 1, 1, 0, 2, 1, 2, 4, 4, 1, 2, 1, 3, 2, 2, 1, 2, 4, 3, 1, 1, 1, 1, 2, 1, 2, 1, 1]
        self.__reduce_to_non_terminal_index = [61, 61, 30, 30, 1, 58, 58, 16, 7, 7, 4, 4, 13, 10, 10, 27, 14, 14, 26, 26, 11, 36, 51, 51, 23, 39, 39, 5, 48, 48, 33, 65, 65, 40, 40, 47, 6, 6, 43, 43, 12, 0, 0, 62, 19, 19, 22, 44, 44, 42, 59, 59, 21, 21, 8, 57, 60, 60, 52, 52, 34, 49, 49, 50, 55, 55, 45, 9, 9, 53, 15, 15, 46, 46, 29, 38, 38, 38, 3, 32, 32, 63, 64, 18, 18, 2, 2, 37, 24, 41, 20, 56, 28, 31, 31, 31, 54, 54, 17, 17, 35, 35]

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
                elif statement_index in [1, 2, 3, 4, 7, 8, 11, 12, 13, 15, 16, 19, 20, 21, 22, 24, 27, 28, 30, 31, 34, 35, 36, 40, 41, 43, 44, 46, 47, 49, 50, 53, 54, 55, 56, 58, 60, 61, 63, 66, 67, 68, 76, 77, 79, 83, 85, 93, 94, 95, 100]:
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
            69: 'command',
            91: 'lexical_define',
            84: 'lexical_name_closure',
            73: 'lexical_closure',
            72: 'lexical_optional',
            99: 'lexical_select',
            81: 'reduce',
            92: 'grammar_node',
            80: 'name_closure',
            101: 'literal',
            71: 'complex_closure',
            70: 'complex_optional',
            97: 'select'
        }
        self.__reduce_number_to_grammar_number = {
            66: 0,
            93: 1,
            95: 2,
            94: 3,
            85: 6,
            86: 7,
            90: 8,
            87: 9,
            88: 10,
            89: 11,
            83: 12,
            98: 16,
            78: 19,
            74: 20,
            75: 21,
            76: 22,
            77: 23,
            82: 24,
            79: 26,
            100: 28,
            96: 32,
            68: 34,
            67: 35
        }
        self.__naive_reduce_number = {2, 67, 68, 101, 3, 100, 76, 77, 79, 83, 85, 93, 94, 95}
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
