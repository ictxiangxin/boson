class LexicalToken:
    text: str
    line: int
    symbol: str

    def __init__(self, text: str, line: int, symbol: str):
        self.text = text
        self.line = line
        self.symbol = symbol


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
            'greedy': 0,
            'except': 1,
            'brace_l': 2,
            '$': 3,
            'brace_r': 4,
            'name': 5,
            'end': 6,
            'reduce': 7,
            'string': 8,
            'bracket_r': 9,
            'parentheses_r': 10,
            'node': 11,
            'null': 12,
            'bracket_l': 13,
            'parentheses_l': 14,
            'star': 15,
            'assign': 16,
            'or': 17,
            'alphabet': 18,
            'plus': 19,
            'count': 20,
            'comma': 21,
            'command': 22
        }
        self.__action_table = {
            0: {5: 's2', 22: 's4'},
            1: {3: 'r70', 5: 's2', 22: 's4'},
            2: {7: 's11', 16: 's10'},
            3: {3: 'r98', 5: 'r98', 22: 'r98'},
            4: {5: 's16', 8: 's14'},
            5: {3: 'r97', 5: 'r97', 22: 'r97'},
            6: {3: 'r2', 5: 'r2', 22: 'r2'},
            7: {3: 'r96', 5: 'r96', 22: 'r96'},
            8: {3: 'a'},
            9: {3: 'r1', 5: 'r1', 22: 'r1'},
            10: {1: 's20', 5: 'r7', 8: 'r7', 13: 's23', 14: 's19', 18: 'r7'},
            11: {5: 's35', 6: 'r81', 8: 's30', 12: 's34', 13: 's29', 14: 's27', 16: 'r81', 17: 'r81'},
            12: {5: 's16', 6: 's38', 8: 's14'},
            13: {5: 'r38', 6: 'r38', 8: 'r38'},
            14: {5: 'r4', 6: 'r4', 8: 'r4'},
            15: {5: 'r21', 6: 'r21', 8: 'r21'},
            16: {5: 'r3', 6: 'r3', 8: 'r3'},
            17: {6: 's40'},
            18: {5: 'r6', 8: 'r6', 18: 'r6'},
            19: {1: 's20', 5: 'r7', 8: 'r7', 13: 's23', 14: 's19', 18: 'r7'},
            20: {5: 'r5', 8: 'r5', 18: 'r5'},
            21: {5: 's45', 8: 's46', 18: 's47'},
            22: {1: 'r64', 2: 'r64', 5: 'r64', 6: 'r64', 8: 'r64', 13: 'r64', 14: 'r64', 17: 'r64', 18: 'r64'},
            23: {1: 's20', 5: 'r7', 8: 'r7', 13: 's23', 14: 's19', 18: 'r7'},
            24: {1: 's20', 2: 's51', 5: 'r7', 6: 'r69', 8: 'r7', 13: 's23', 14: 's19', 17: 'r69', 18: 'r7'},
            25: {1: 'r89', 2: 'r89', 5: 'r89', 6: 'r89', 8: 'r89', 9: 'r89', 10: 'r89', 13: 'r89', 14: 'r89', 17: 'r89', 18: 'r89'},
            26: {6: 'r62', 17: 'r62'},
            27: {5: 's35', 8: 's30', 13: 's29', 14: 's27'},
            28: {6: 'r35', 16: 's58', 17: 'r35'},
            29: {5: 's35', 8: 's30', 13: 's29', 14: 's27'},
            30: {5: 'r85', 6: 'r85', 8: 'r85', 9: 'r85', 10: 'r85', 13: 'r85', 14: 'r85', 16: 'r85', 17: 'r85'},
            31: {6: 's62'},
            32: {5: 's35', 6: 'r79', 8: 's30', 13: 's29', 14: 's27', 16: 'r79', 17: 'r79'},
            33: {6: 'r29', 17: 'r29'},
            34: {6: 'r80', 16: 'r80', 17: 'r80'},
            35: {5: 'r51', 6: 'r51', 8: 'r51', 9: 'r51', 10: 'r51', 13: 'r51', 14: 'r51', 15: 's65', 16: 'r51', 17: 'r51', 19: 's69'},
            36: {5: 'r83', 6: 'r83', 8: 'r83', 9: 'r83', 10: 'r83', 13: 'r83', 14: 'r83', 16: 'r83', 17: 'r83'},
            37: {5: 'r37', 6: 'r37', 8: 'r37', 13: 'r37', 14: 'r37', 16: 'r37', 17: 'r37'},
            38: {3: 'r73', 5: 'r73', 22: 'r73'},
            39: {5: 'r39', 6: 'r39', 8: 'r39'},
            40: {3: 'r92', 5: 'r92', 22: 'r92'},
            41: {10: 's70'},
            42: {1: 's20', 5: 'r7', 8: 'r7', 9: 'r101', 10: 'r101', 13: 's23', 14: 's19', 18: 'r7'},
            43: {1: 'r19', 5: 'r19', 8: 'r19', 9: 'r19', 10: 'r19', 13: 'r19', 14: 'r19', 17: 's72', 18: 'r19'},
            44: {1: 'r14', 2: 'r14', 5: 'r14', 6: 'r14', 8: 'r14', 9: 'r14', 10: 'r14', 13: 'r14', 14: 'r14', 15: 's65', 17: 'r14', 18: 'r14', 19: 's69', 20: 's76'},
            45: {1: 'r9', 2: 'r9', 5: 'r9', 6: 'r9', 8: 'r9', 9: 'r9', 10: 'r9', 13: 'r9', 14: 'r9', 15: 'r9', 17: 'r9', 18: 'r9', 19: 'r9', 20: 'r9'},
            46: {1: 'r10', 2: 'r10', 5: 'r10', 6: 'r10', 8: 'r10', 9: 'r10', 10: 'r10', 13: 'r10', 14: 'r10', 15: 'r10', 17: 'r10', 18: 'r10', 19: 'r10', 20: 'r10'},
            47: {1: 'r8', 2: 'r8', 5: 'r8', 6: 'r8', 8: 'r8', 9: 'r8', 10: 'r8', 13: 'r8', 14: 'r8', 15: 'r8', 17: 'r8', 18: 'r8', 19: 'r8', 20: 'r8'},
            48: {1: 'r11', 2: 'r11', 5: 'r11', 6: 'r11', 8: 'r11', 9: 'r11', 10: 'r11', 13: 'r11', 14: 'r11', 15: 'r11', 17: 'r11', 18: 'r11', 19: 'r11', 20: 'r11'},
            49: {9: 's80'},
            50: {6: 'r90', 17: 'r90'},
            51: {5: 's81'},
            52: {6: 'r68', 17: 'r68'},
            53: {1: 'r63', 2: 'r63', 5: 'r63', 6: 'r63', 8: 'r63', 13: 'r63', 14: 'r63', 17: 'r63', 18: 'r63'},
            54: {6: 'r91', 17: 's84'},
            55: {5: 's35', 8: 's30', 9: 'r99', 10: 'r99', 13: 's29', 14: 's27'},
            56: {5: 'r57', 8: 'r57', 9: 'r57', 10: 'r57', 13: 'r57', 14: 'r57', 17: 's87'},
            57: {10: 's89'},
            58: {5: 's92', 14: 'r32'},
            59: {6: 'r78', 17: 'r78'},
            60: {6: 'r34', 17: 'r34'},
            61: {9: 's93'},
            62: {3: 'r86', 5: 'r86', 22: 'r86'},
            63: {5: 'r36', 6: 'r36', 8: 'r36', 13: 'r36', 14: 'r36', 16: 'r36', 17: 'r36'},
            64: {6: 'r82', 17: 's95'},
            65: {0: 'r72', 1: 'r72', 2: 'r72', 5: 'r72', 6: 'r72', 8: 'r72', 9: 'r72', 10: 'r72', 13: 'r72', 14: 'r72', 16: 'r72', 17: 'r72', 18: 'r72'},
            66: {5: 'r49', 6: 'r49', 8: 'r49', 9: 'r49', 10: 'r49', 13: 'r49', 14: 'r49', 16: 'r49', 17: 'r49'},
            67: {5: 'r84', 6: 'r84', 8: 'r84', 9: 'r84', 10: 'r84', 13: 'r84', 14: 'r84', 16: 'r84', 17: 'r84'},
            68: {5: 'r50', 6: 'r50', 8: 'r50', 9: 'r50', 10: 'r50', 13: 'r50', 14: 'r50', 16: 'r50', 17: 'r50'},
            69: {0: 'r71', 1: 'r71', 2: 'r71', 5: 'r71', 6: 'r71', 8: 'r71', 9: 'r71', 10: 'r71', 13: 'r71', 14: 'r71', 16: 'r71', 17: 'r71', 18: 'r71'},
            70: {1: 'r17', 2: 'r17', 5: 'r17', 6: 'r17', 8: 'r17', 9: 'r17', 10: 'r17', 13: 'r17', 14: 'r17', 15: 's65', 17: 'r17', 18: 'r17', 19: 's69', 20: 's76'},
            71: {1: 'r18', 5: 'r18', 8: 'r18', 9: 'r18', 10: 'r18', 13: 'r18', 14: 'r18', 18: 'r18'},
            72: {1: 's20', 5: 'r7', 8: 'r7', 13: 's23', 14: 's19', 18: 'r7'},
            73: {9: 'r22', 10: 'r22', 17: 'r22'},
            74: {9: 'r102', 10: 'r102', 17: 's72'},
            75: {1: 'r13', 2: 'r13', 5: 'r13', 6: 'r13', 8: 'r13', 9: 'r13', 10: 'r13', 13: 'r13', 14: 'r13', 17: 'r13', 18: 'r13'},
            76: {1: 'r95', 2: 'r95', 5: 'r95', 6: 'r95', 8: 'r95', 9: 'r95', 10: 'r95', 13: 'r95', 14: 'r95', 17: 'r95', 18: 'r95'},
            77: {0: 's102', 1: 'r26', 2: 'r26', 5: 'r26', 6: 'r26', 8: 'r26', 9: 'r26', 10: 'r26', 13: 'r26', 14: 'r26', 17: 'r26', 18: 'r26'},
            78: {1: 'r88', 2: 'r88', 5: 'r88', 6: 'r88', 8: 'r88', 9: 'r88', 10: 'r88', 13: 'r88', 14: 'r88', 17: 'r88', 18: 'r88'},
            79: {1: 'r12', 2: 'r12', 5: 'r12', 6: 'r12', 8: 'r12', 9: 'r12', 10: 'r12', 13: 'r12', 14: 'r12', 17: 'r12', 18: 'r12'},
            80: {1: 'r76', 2: 'r76', 5: 'r76', 6: 'r76', 8: 'r76', 9: 'r76', 10: 'r76', 13: 'r76', 14: 'r76', 17: 'r76', 18: 'r76'},
            81: {4: 'r66', 5: 'r66'},
            82: {4: 's105', 5: 's104'},
            83: {6: 'r61', 17: 'r61'},
            84: {1: 's20', 5: 'r7', 8: 'r7', 13: 's23', 14: 's19', 18: 'r7'},
            85: {5: 'r56', 8: 'r56', 9: 'r56', 10: 'r56', 13: 'r56', 14: 'r56'},
            86: {9: 'r100', 10: 'r100', 17: 's87'},
            87: {5: 's35', 8: 's30', 13: 's29', 14: 's27'},
            88: {9: 'r59', 10: 'r59', 17: 'r59'},
            89: {5: 'r54', 6: 'r54', 8: 'r54', 9: 'r54', 10: 'r54', 13: 'r54', 14: 'r54', 15: 's65', 16: 'r54', 17: 'r54', 19: 's69'},
            90: {14: 's113'},
            91: {14: 'r31'},
            92: {14: 'r30'},
            93: {5: 'r74', 6: 'r74', 8: 'r74', 9: 'r74', 10: 'r74', 13: 'r74', 14: 'r74', 16: 'r74', 17: 'r74'},
            94: {6: 'r28', 17: 'r28'},
            95: {5: 's35', 6: 'r81', 8: 's30', 12: 's34', 13: 's29', 14: 's27', 16: 'r81', 17: 'r81'},
            96: {1: 'r15', 2: 'r15', 5: 'r15', 6: 'r15', 8: 'r15', 9: 'r15', 10: 'r15', 13: 'r15', 14: 'r15', 17: 'r15', 18: 'r15'},
            97: {1: 'r16', 2: 'r16', 5: 'r16', 6: 'r16', 8: 'r16', 9: 'r16', 10: 'r16', 13: 'r16', 14: 'r16', 17: 'r16', 18: 'r16'},
            98: {1: 'r77', 2: 'r77', 5: 'r77', 6: 'r77', 8: 'r77', 9: 'r77', 10: 'r77', 13: 'r77', 14: 'r77', 17: 'r77', 18: 'r77'},
            99: {9: 'r20', 10: 'r20', 17: 'r20'},
            100: {9: 'r23', 10: 'r23', 17: 'r23'},
            101: {1: 'r94', 2: 'r94', 5: 'r94', 6: 'r94', 8: 'r94', 9: 'r94', 10: 'r94', 13: 'r94', 14: 'r94', 17: 'r94', 18: 'r94'},
            102: {1: 'r24', 2: 'r24', 5: 'r24', 6: 'r24', 8: 'r24', 9: 'r24', 10: 'r24', 13: 'r24', 14: 'r24', 17: 'r24', 18: 'r24'},
            103: {1: 'r25', 2: 'r25', 5: 'r25', 6: 'r25', 8: 'r25', 9: 'r25', 10: 'r25', 13: 'r25', 14: 'r25', 17: 'r25', 18: 'r25'},
            104: {4: 'r65', 5: 'r65'},
            105: {6: 'r67', 17: 'r67'},
            106: {6: 'r55', 17: 'r55'},
            107: {9: 'r60', 10: 'r60', 17: 'r60'},
            108: {9: 'r58', 10: 'r58', 17: 'r58'},
            109: {5: 'r75', 6: 'r75', 8: 'r75', 9: 'r75', 10: 'r75', 13: 'r75', 14: 'r75', 16: 'r75', 17: 'r75'},
            110: {5: 'r52', 6: 'r52', 8: 'r52', 9: 'r52', 10: 'r52', 13: 'r52', 14: 'r52', 16: 'r52', 17: 'r52'},
            111: {5: 'r53', 6: 'r53', 8: 'r53', 9: 'r53', 10: 'r53', 13: 'r53', 14: 'r53', 16: 'r53', 17: 'r53'},
            112: {6: 'r33', 17: 'r33'},
            113: {11: 'r45', 15: 's118'},
            114: {6: 'r27', 17: 'r27'},
            115: {10: 'r42', 21: 'r42'},
            116: {11: 'r44'},
            117: {11: 's120'},
            118: {11: 'r43'},
            119: {10: 's123', 21: 's121'},
            120: {6: 'r48', 10: 'r48', 14: 's113', 17: 'r48', 21: 'r48'},
            121: {11: 'r45', 15: 's118'},
            122: {10: 'r41', 21: 'r41'},
            123: {6: 'r87', 10: 'r87', 17: 'r87', 21: 'r87'},
            124: {6: 'r46', 10: 'r46', 17: 'r46', 21: 'r46'},
            125: {6: 'r47', 10: 'r47', 17: 'r47', 21: 'r47'},
            126: {6: 'r93', 10: 'r93', 17: 'r93', 21: 'r93'},
            127: {10: 'r40', 21: 'r40'}
        }
        self.__goto_table = {
            0: {2: 5, 17: 8, 35: 3, 42: 6, 45: 1, 47: 7},
            1: {2: 5, 35: 3, 42: 9, 47: 7},
            4: {3: 12, 10: 15, 28: 13},
            10: {15: 26, 23: 17, 34: 25, 38: 24, 40: 18, 51: 22, 54: 21},
            11: {20: 36, 24: 37, 25: 32, 32: 33, 37: 31, 49: 28},
            12: {10: 15, 28: 39},
            19: {34: 25, 36: 42, 40: 18, 51: 43, 54: 21, 62: 41},
            21: {12: 48, 16: 44},
            23: {34: 25, 36: 42, 40: 18, 51: 43, 54: 21, 62: 49},
            24: {34: 25, 39: 52, 40: 18, 51: 53, 52: 50, 54: 21},
            26: {5: 54},
            27: {4: 57, 11: 55, 20: 36, 24: 56},
            28: {14: 60, 58: 59},
            29: {4: 61, 11: 55, 20: 36, 24: 56},
            32: {20: 36, 24: 63},
            33: {44: 64},
            35: {22: 68, 30: 67, 41: 66},
            42: {34: 25, 40: 18, 51: 71, 54: 21},
            43: {8: 73, 56: 74},
            44: {13: 75, 18: 79, 41: 77, 48: 78},
            51: {31: 82},
            54: {21: 83},
            55: {20: 36, 24: 85},
            56: {33: 86, 55: 88},
            58: {26: 90, 57: 91},
            64: {60: 94},
            70: {18: 96, 27: 97, 41: 77, 59: 98},
            72: {34: 25, 40: 18, 51: 99, 54: 21},
            74: {8: 100},
            77: {29: 103, 53: 101},
            84: {15: 106, 34: 25, 38: 24, 40: 18, 51: 22, 54: 21},
            86: {55: 107},
            87: {20: 36, 24: 108},
            89: {41: 110, 43: 111, 46: 109},
            90: {19: 112},
            95: {20: 36, 24: 37, 25: 32, 32: 114, 49: 28},
            113: {1: 116, 6: 115, 61: 117},
            115: {50: 119},
            119: {7: 122},
            120: {0: 126, 19: 124, 63: 125},
            121: {1: 116, 6: 127, 61: 117}
        }
        self.__node_table = {
            0: ('*0', '1'),
            38: ('*0', '1'),
            72: ('0', ('*1', ('?',))),
            91: ('0', '2'),
            60: ('*0', '1'),
            61: (),
            90: ('0', ('*1', ('1',))),
            62: ('*0', '1'),
            64: ('*0', '1'),
            68: (),
            89: ('0', ('*1', ('1',))),
            6: (),
            13: (),
            87: (('*0', ('?',)), ('*1', ('?',)), ('2', ('?',))),
            16: (),
            76: ('1', ('*3', ('?',))),
            75: ('1',),
            17: ('*0', '1'),
            22: ('*0', '1'),
            100: ('*0',),
            101: ('0', ('*1', ('1',))),
            25: (),
            93: ('0', ('*1', ('?',))),
            85: ('0', '2'),
            27: ('*0', '1'),
            28: (),
            81: ('0', ('*1', ('1',))),
            31: (),
            34: (),
            77: ('0', ('*1', (('*1', ('?',)), '2'))),
            35: ('*0', '1'),
            78: ('*0',),
            40: ('*0', '1'),
            41: (),
            86: ('1', ('*2', ('1',))),
            44: (),
            47: (),
            92: (('*0', ('?',)), '1', ('*2', ('?',))),
            50: (),
            83: ('0', ('*1', ('?',))),
            84: ('0',),
            53: (),
            74: ('1', ('*3', ('?',))),
            73: ('1',),
            55: ('*0', '1'),
            59: ('*0', '1'),
            98: ('*0',),
            99: ('0', ('*1', ('1',)))
        }
        self.__reduce_symbol_sum = [2, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 2, 1, 2, 1, 1, 2, 1, 1, 0, 2, 2, 0, 1, 1, 0, 3, 1, 0, 2, 1, 1, 2, 2, 2, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 2, 2, 1, 2, 1, 2, 2, 0, 2, 1, 2, 1, 3, 1, 0, 1, 1, 1, 3, 3, 4, 3, 4, 2, 1, 1, 0, 2, 1, 2, 1, 4, 4, 3, 1, 2, 2, 4, 3, 2, 1, 1, 1, 1, 1, 2, 1, 2]
        self.__reduce_to_non_terminal_index = [45, 45, 10, 10, 40, 54, 54, 12, 12, 12, 16, 13, 48, 48, 27, 59, 59, 36, 36, 8, 28, 56, 56, 29, 53, 53, 60, 44, 44, 57, 26, 26, 14, 58, 58, 25, 25, 3, 3, 7, 50, 50, 1, 61, 61, 63, 0, 0, 22, 30, 30, 43, 46, 46, 21, 11, 11, 55, 33, 33, 5, 5, 38, 38, 31, 31, 39, 52, 52, 17, 41, 41, 47, 20, 20, 34, 34, 32, 49, 49, 49, 37, 24, 24, 24, 2, 19, 51, 51, 15, 23, 35, 6, 18, 18, 42, 42, 42, 4, 4, 62, 62]

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
                elif statement_index in [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14, 15, 18, 19, 20, 21, 23, 24, 26, 29, 30, 32, 33, 36, 37, 39, 42, 43, 45, 46, 48, 49, 51, 52, 54, 56, 57, 58, 63, 65, 66, 67, 69, 70, 71, 79, 80, 82, 88, 94, 95, 96, 97]:
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
            72: 'command',
            91: 'lexical_define',
            76: 'lexical_closure',
            75: 'lexical_optional',
            101: 'lexical_select',
            85: 'reduce',
            92: 'grammar_node',
            83: 'name_closure',
            84: 'literal',
            74: 'complex_closure',
            73: 'complex_optional',
            99: 'select'
        }
        self.__reduce_number_to_grammar_number = {
            69: 0,
            95: 1,
            97: 2,
            96: 3,
            90: 6,
            89: 7,
            88: 8,
            87: 9,
            100: 12,
            93: 14,
            94: 15,
            81: 17,
            77: 18,
            78: 19,
            79: 20,
            80: 21,
            86: 22,
            82: 24,
            98: 29,
            70: 31,
            71: 32
        }
        self.__naive_reduce_number = {96, 97, 2, 3, 70, 71, 7, 9, 8, 79, 80, 82, 84, 88, 94, 95}
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
