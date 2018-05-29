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
            'bracket_r': 0,
            '$': 1,
            'name': 2,
            'except': 3,
            'brace_l': 4,
            'plus': 5,
            'node': 6,
            'end': 7,
            'parentheses_r': 8,
            'parentheses_l': 9,
            'reduce': 10,
            'count': 11,
            'string': 12,
            'greedy': 13,
            'comma': 14,
            'assign': 15,
            'brace_r': 16,
            'null': 17,
            'alphabet': 18,
            'bracket_l': 19,
            'star': 20,
            'or': 21,
            'command': 22
        }
        self.__action_table = {
            0: {2: 's5', 22: 's8'},
            1: {1: 'r70', 2: 's5', 22: 's8'},
            2: {1: 'r97', 2: 'r97', 22: 'r97'},
            3: {1: 'a'},
            4: {1: 'r98', 2: 'r98', 22: 'r98'},
            5: {10: 's10', 15: 's11'},
            6: {1: 'r96', 2: 'r96', 22: 'r96'},
            7: {1: 'r2', 2: 'r2', 22: 'r2'},
            8: {2: 's14', 12: 's13'},
            9: {1: 'r1', 2: 'r1', 22: 'r1'},
            10: {2: 's19', 7: 'r81', 9: 's18', 12: 's17', 15: 'r81', 17: 's23', 19: 's21', 21: 'r81'},
            11: {2: 'r7', 3: 's36', 9: 's37', 12: 'r7', 18: 'r7', 19: 's35'},
            12: {2: 's14', 7: 's39', 12: 's13'},
            13: {2: 'r4', 7: 'r4', 12: 'r4'},
            14: {2: 'r3', 7: 'r3', 12: 'r3'},
            15: {2: 'r38', 7: 'r38', 12: 'r38'},
            16: {2: 'r21', 7: 'r21', 12: 'r21'},
            17: {0: 'r85', 2: 'r85', 7: 'r85', 8: 'r85', 9: 'r85', 12: 'r85', 15: 'r85', 19: 'r85', 21: 'r85'},
            18: {2: 's19', 9: 's18', 12: 's17', 19: 's21'},
            19: {0: 'r51', 2: 'r51', 5: 's45', 7: 'r51', 8: 'r51', 9: 'r51', 12: 'r51', 15: 'r51', 19: 'r51', 20: 's44', 21: 'r51'},
            20: {2: 's19', 7: 'r79', 9: 's18', 12: 's17', 15: 'r79', 19: 's21', 21: 'r79'},
            21: {2: 's19', 9: 's18', 12: 's17', 19: 's21'},
            22: {7: 'r35', 15: 's50', 21: 'r35'},
            23: {7: 'r80', 15: 'r80', 21: 'r80'},
            24: {7: 's53'},
            25: {2: 'r37', 7: 'r37', 9: 'r37', 12: 'r37', 15: 'r37', 19: 'r37', 21: 'r37'},
            26: {7: 'r29', 21: 'r29'},
            27: {0: 'r83', 2: 'r83', 7: 'r83', 8: 'r83', 9: 'r83', 12: 'r83', 15: 'r83', 19: 'r83', 21: 'r83'},
            28: {0: 'r89', 2: 'r89', 3: 'r89', 4: 'r89', 7: 'r89', 8: 'r89', 9: 'r89', 12: 'r89', 18: 'r89', 19: 'r89', 21: 'r89'},
            29: {7: 'r62', 21: 'r62'},
            30: {2: 'r64', 3: 'r64', 4: 'r64', 7: 'r64', 9: 'r64', 12: 'r64', 18: 'r64', 19: 'r64', 21: 'r64'},
            31: {2: 's58', 12: 's59', 18: 's60'},
            32: {2: 'r7', 3: 's36', 4: 's61', 7: 'r69', 9: 's37', 12: 'r7', 18: 'r7', 19: 's35', 21: 'r69'},
            33: {7: 's65'},
            34: {2: 'r6', 12: 'r6', 18: 'r6'},
            35: {2: 'r7', 3: 's36', 9: 's37', 12: 'r7', 18: 'r7', 19: 's35'},
            36: {2: 'r5', 12: 'r5', 18: 'r5'},
            37: {2: 'r7', 3: 's36', 9: 's37', 12: 'r7', 18: 'r7', 19: 's35'},
            38: {2: 'r39', 7: 'r39', 12: 'r39'},
            39: {1: 'r73', 2: 'r73', 22: 'r73'},
            40: {0: 'r57', 2: 'r57', 8: 'r57', 9: 'r57', 12: 'r57', 19: 'r57', 21: 's71'},
            41: {0: 'r99', 2: 's19', 8: 'r99', 9: 's18', 12: 's17', 19: 's21'},
            42: {8: 's74'},
            43: {0: 'r50', 2: 'r50', 7: 'r50', 8: 'r50', 9: 'r50', 12: 'r50', 15: 'r50', 19: 'r50', 21: 'r50'},
            44: {0: 'r72', 2: 'r72', 3: 'r72', 4: 'r72', 7: 'r72', 8: 'r72', 9: 'r72', 12: 'r72', 13: 'r72', 15: 'r72', 18: 'r72', 19: 'r72', 21: 'r72'},
            45: {0: 'r71', 2: 'r71', 3: 'r71', 4: 'r71', 7: 'r71', 8: 'r71', 9: 'r71', 12: 'r71', 13: 'r71', 15: 'r71', 18: 'r71', 19: 'r71', 21: 'r71'},
            46: {0: 'r84', 2: 'r84', 7: 'r84', 8: 'r84', 9: 'r84', 12: 'r84', 15: 'r84', 19: 'r84', 21: 'r84'},
            47: {0: 'r49', 2: 'r49', 7: 'r49', 8: 'r49', 9: 'r49', 12: 'r49', 15: 'r49', 19: 'r49', 21: 'r49'},
            48: {2: 'r36', 7: 'r36', 9: 'r36', 12: 'r36', 15: 'r36', 19: 'r36', 21: 'r36'},
            49: {0: 's75'},
            50: {2: 's78', 9: 'r32'},
            51: {7: 'r34', 21: 'r34'},
            52: {7: 'r78', 21: 'r78'},
            53: {1: 'r86', 2: 'r86', 22: 'r86'},
            54: {7: 'r82', 21: 's80'},
            55: {7: 'r91', 21: 's82'},
            56: {0: 'r14', 2: 'r14', 3: 'r14', 4: 'r14', 5: 's45', 7: 'r14', 8: 'r14', 9: 'r14', 11: 's85', 12: 'r14', 18: 'r14', 19: 'r14', 20: 's44', 21: 'r14'},
            57: {0: 'r11', 2: 'r11', 3: 'r11', 4: 'r11', 5: 'r11', 7: 'r11', 8: 'r11', 9: 'r11', 11: 'r11', 12: 'r11', 18: 'r11', 19: 'r11', 20: 'r11', 21: 'r11'},
            58: {0: 'r9', 2: 'r9', 3: 'r9', 4: 'r9', 5: 'r9', 7: 'r9', 8: 'r9', 9: 'r9', 11: 'r9', 12: 'r9', 18: 'r9', 19: 'r9', 20: 'r9', 21: 'r9'},
            59: {0: 'r10', 2: 'r10', 3: 'r10', 4: 'r10', 5: 'r10', 7: 'r10', 8: 'r10', 9: 'r10', 11: 'r10', 12: 'r10', 18: 'r10', 19: 'r10', 20: 'r10', 21: 'r10'},
            60: {0: 'r8', 2: 'r8', 3: 'r8', 4: 'r8', 5: 'r8', 7: 'r8', 8: 'r8', 9: 'r8', 11: 'r8', 12: 'r8', 18: 'r8', 19: 'r8', 20: 'r8', 21: 'r8'},
            61: {2: 's89'},
            62: {2: 'r63', 3: 'r63', 4: 'r63', 7: 'r63', 9: 'r63', 12: 'r63', 18: 'r63', 19: 'r63', 21: 'r63'},
            63: {7: 'r90', 21: 'r90'},
            64: {7: 'r68', 21: 'r68'},
            65: {1: 'r92', 2: 'r92', 22: 'r92'},
            66: {0: 's90'},
            67: {0: 'r19', 2: 'r19', 3: 'r19', 8: 'r19', 9: 'r19', 12: 'r19', 18: 'r19', 19: 'r19', 21: 's91'},
            68: {0: 'r101', 2: 'r7', 3: 's36', 8: 'r101', 9: 's37', 12: 'r7', 18: 'r7', 19: 's35'},
            69: {8: 's95'},
            70: {0: 'r100', 8: 'r100', 21: 's71'},
            71: {2: 's19', 9: 's18', 12: 's17', 19: 's21'},
            72: {0: 'r59', 8: 'r59', 21: 'r59'},
            73: {0: 'r56', 2: 'r56', 8: 'r56', 9: 'r56', 12: 'r56', 19: 'r56'},
            74: {0: 'r54', 2: 'r54', 5: 's45', 7: 'r54', 8: 'r54', 9: 'r54', 12: 'r54', 15: 'r54', 19: 'r54', 20: 's44', 21: 'r54'},
            75: {0: 'r74', 2: 'r74', 7: 'r74', 8: 'r74', 9: 'r74', 12: 'r74', 15: 'r74', 19: 'r74', 21: 'r74'},
            76: {9: 's101'},
            77: {9: 'r31'},
            78: {9: 'r30'},
            79: {7: 'r28', 21: 'r28'},
            80: {2: 's19', 7: 'r81', 9: 's18', 12: 's17', 15: 'r81', 17: 's23', 19: 's21', 21: 'r81'},
            81: {7: 'r61', 21: 'r61'},
            82: {2: 'r7', 3: 's36', 9: 's37', 12: 'r7', 18: 'r7', 19: 's35'},
            83: {0: 'r12', 2: 'r12', 3: 'r12', 4: 'r12', 7: 'r12', 8: 'r12', 9: 'r12', 12: 'r12', 18: 'r12', 19: 'r12', 21: 'r12'},
            84: {0: 'r88', 2: 'r88', 3: 'r88', 4: 'r88', 7: 'r88', 8: 'r88', 9: 'r88', 12: 'r88', 18: 'r88', 19: 'r88', 21: 'r88'},
            85: {0: 'r95', 2: 'r95', 3: 'r95', 4: 'r95', 7: 'r95', 8: 'r95', 9: 'r95', 12: 'r95', 18: 'r95', 19: 'r95', 21: 'r95'},
            86: {0: 'r26', 2: 'r26', 3: 'r26', 4: 'r26', 7: 'r26', 8: 'r26', 9: 'r26', 12: 'r26', 13: 's107', 18: 'r26', 19: 'r26', 21: 'r26'},
            87: {0: 'r13', 2: 'r13', 3: 'r13', 4: 'r13', 7: 'r13', 8: 'r13', 9: 'r13', 12: 'r13', 18: 'r13', 19: 'r13', 21: 'r13'},
            88: {2: 's109', 16: 's108'},
            89: {2: 'r66', 16: 'r66'},
            90: {0: 'r76', 2: 'r76', 3: 'r76', 4: 'r76', 7: 'r76', 8: 'r76', 9: 'r76', 12: 'r76', 18: 'r76', 19: 'r76', 21: 'r76'},
            91: {2: 'r7', 3: 's36', 9: 's37', 12: 'r7', 18: 'r7', 19: 's35'},
            92: {0: 'r102', 8: 'r102', 21: 's91'},
            93: {0: 'r22', 8: 'r22', 21: 'r22'},
            94: {0: 'r18', 2: 'r18', 3: 'r18', 8: 'r18', 9: 'r18', 12: 'r18', 18: 'r18', 19: 'r18'},
            95: {0: 'r17', 2: 'r17', 3: 'r17', 4: 'r17', 5: 's45', 7: 'r17', 8: 'r17', 9: 'r17', 11: 's85', 12: 'r17', 18: 'r17', 19: 'r17', 20: 's44', 21: 'r17'},
            96: {0: 'r60', 8: 'r60', 21: 'r60'},
            97: {0: 'r58', 8: 'r58', 21: 'r58'},
            98: {0: 'r75', 2: 'r75', 7: 'r75', 8: 'r75', 9: 'r75', 12: 'r75', 15: 'r75', 19: 'r75', 21: 'r75'},
            99: {0: 'r53', 2: 'r53', 7: 'r53', 8: 'r53', 9: 'r53', 12: 'r53', 15: 'r53', 19: 'r53', 21: 'r53'},
            100: {0: 'r52', 2: 'r52', 7: 'r52', 8: 'r52', 9: 'r52', 12: 'r52', 15: 'r52', 19: 'r52', 21: 'r52'},
            101: {6: 'r45', 20: 's118'},
            102: {7: 'r33', 21: 'r33'},
            103: {7: 'r27', 21: 'r27'},
            104: {7: 'r55', 21: 'r55'},
            105: {0: 'r25', 2: 'r25', 3: 'r25', 4: 'r25', 7: 'r25', 8: 'r25', 9: 'r25', 12: 'r25', 18: 'r25', 19: 'r25', 21: 'r25'},
            106: {0: 'r94', 2: 'r94', 3: 'r94', 4: 'r94', 7: 'r94', 8: 'r94', 9: 'r94', 12: 'r94', 18: 'r94', 19: 'r94', 21: 'r94'},
            107: {0: 'r24', 2: 'r24', 3: 'r24', 4: 'r24', 7: 'r24', 8: 'r24', 9: 'r24', 12: 'r24', 18: 'r24', 19: 'r24', 21: 'r24'},
            108: {7: 'r67', 21: 'r67'},
            109: {2: 'r65', 16: 'r65'},
            110: {0: 'r20', 8: 'r20', 21: 'r20'},
            111: {0: 'r23', 8: 'r23', 21: 'r23'},
            112: {0: 'r16', 2: 'r16', 3: 'r16', 4: 'r16', 7: 'r16', 8: 'r16', 9: 'r16', 12: 'r16', 18: 'r16', 19: 'r16', 21: 'r16'},
            113: {0: 'r77', 2: 'r77', 3: 'r77', 4: 'r77', 7: 'r77', 8: 'r77', 9: 'r77', 12: 'r77', 18: 'r77', 19: 'r77', 21: 'r77'},
            114: {0: 'r15', 2: 'r15', 3: 'r15', 4: 'r15', 7: 'r15', 8: 'r15', 9: 'r15', 12: 'r15', 18: 'r15', 19: 'r15', 21: 'r15'},
            115: {6: 's119'},
            116: {6: 'r44'},
            117: {8: 'r42', 14: 'r42'},
            118: {6: 'r43'},
            119: {7: 'r48', 8: 'r48', 9: 's101', 14: 'r48', 21: 'r48'},
            120: {8: 's126', 14: 's125'},
            121: {7: 'r47', 8: 'r47', 14: 'r47', 21: 'r47'},
            122: {7: 'r46', 8: 'r46', 14: 'r46', 21: 'r46'},
            123: {7: 'r93', 8: 'r93', 14: 'r93', 21: 'r93'},
            124: {8: 'r41', 14: 'r41'},
            125: {6: 'r45', 20: 's118'},
            126: {7: 'r87', 8: 'r87', 14: 'r87', 21: 'r87'},
            127: {8: 'r40', 14: 'r40'}
        }
        self.__goto_table = {
            0: {2: 3, 43: 2, 46: 6, 49: 1, 53: 4, 61: 7},
            1: {43: 2, 46: 6, 53: 4, 61: 9},
            8: {6: 15, 33: 12, 51: 16},
            10: {0: 20, 8: 27, 16: 22, 25: 25, 35: 26, 56: 24},
            11: {4: 33, 10: 28, 18: 31, 23: 29, 31: 32, 32: 34, 52: 30},
            12: {6: 38, 51: 16},
            18: {8: 27, 25: 40, 39: 41, 44: 42},
            19: {24: 43, 50: 47, 59: 46},
            20: {8: 27, 25: 48},
            21: {8: 27, 25: 40, 39: 41, 44: 49},
            22: {14: 52, 62: 51},
            26: {28: 54},
            29: {48: 55},
            31: {9: 56, 11: 57},
            32: {10: 28, 13: 63, 18: 31, 20: 64, 32: 34, 52: 62},
            35: {5: 68, 10: 28, 12: 66, 18: 31, 32: 34, 52: 67},
            37: {5: 68, 10: 28, 12: 69, 18: 31, 32: 34, 52: 67},
            40: {19: 70, 42: 72},
            41: {8: 27, 25: 73},
            50: {37: 76, 41: 77},
            54: {26: 79},
            55: {60: 81},
            56: {21: 83, 29: 84, 36: 87, 50: 86},
            61: {38: 88},
            67: {17: 93, 55: 92},
            68: {10: 28, 18: 31, 32: 34, 52: 94},
            70: {42: 96},
            71: {8: 27, 25: 97},
            74: {40: 99, 50: 100, 54: 98},
            76: {15: 102},
            80: {0: 20, 8: 27, 16: 22, 25: 25, 35: 103},
            82: {10: 28, 18: 31, 23: 104, 31: 32, 32: 34, 52: 30},
            86: {7: 105, 45: 106},
            91: {10: 28, 18: 31, 32: 34, 52: 110},
            92: {17: 111},
            95: {21: 114, 47: 112, 50: 86, 58: 113},
            101: {22: 117, 34: 116, 57: 115},
            117: {27: 120},
            119: {15: 122, 30: 121, 63: 123},
            120: {1: 124},
            125: {22: 127, 34: 116, 57: 115}
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
        self.__reduce_to_non_terminal_index = [49, 49, 51, 51, 32, 18, 18, 11, 11, 11, 9, 36, 29, 29, 47, 58, 58, 5, 5, 17, 6, 55, 55, 7, 45, 45, 26, 28, 28, 41, 37, 37, 62, 14, 14, 0, 0, 33, 33, 1, 27, 27, 34, 57, 57, 30, 63, 63, 24, 59, 59, 40, 54, 54, 60, 39, 39, 42, 19, 19, 48, 48, 31, 31, 38, 38, 20, 13, 13, 2, 50, 50, 46, 8, 8, 10, 10, 35, 16, 16, 16, 56, 25, 25, 25, 43, 15, 52, 52, 23, 4, 53, 22, 21, 21, 61, 61, 61, 44, 44, 12, 12]

    def __generate_grammar_tuple(self, statement_index, symbol_package):
        grammar_node = BosonGrammarNode()
        if isinstance(statement_index, int):
            node_tuple = self.__node_table[statement_index]
        else:
            node_tuple = statement_index
            statement_index = -1
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
                            grammar_node += self.__generate_grammar_tuple(i[1], node)
                    else:
                        for node in symbol_package[int(i[0])]:
                            grammar_node.append(self.__generate_grammar_tuple(i[1], node))
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
                    symbol_stack.append(self.__generate_grammar_tuple(statement_index, symbol_package))
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
        self.__naive_reduce_number = {96, 97, 2, 3, 70, 7, 8, 71, 9, 79, 80, 82, 84, 88, 94, 95}
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
            grammar_name = '!grammar_{}'.format('hidden')
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
