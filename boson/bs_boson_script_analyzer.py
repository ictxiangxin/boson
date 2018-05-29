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


class BosonEBNFAnalyzer:
    def __init__(self):
        self.__terminal_index = {
            'bracket_r': 0,
            'plus': 1,
            'node': 2,
            'brace_r': 3,
            'count': 4,
            'star': 5,
            'or': 6,
            'assign': 7,
            'alphabet': 8,
            'end': 9,
            'command': 10,
            'string': 11,
            'comma': 12,
            'parentheses_l': 13,
            'reduce': 14,
            'name': 15,
            'greedy': 16,
            'except': 17,
            '$': 18,
            'parentheses_r': 19,
            'brace_l': 20,
            'null': 21,
            'bracket_l': 22
        }
        self.__action_table = {
            0: {10: 's8', 15: 's3'},
            1: {10: 'r96', 15: 'r96', 18: 'r96'},
            2: {10: 's8', 15: 's3', 18: 'r70'},
            3: {7: 's10', 14: 's11'},
            4: {10: 'r2', 15: 'r2', 18: 'r2'},
            5: {10: 'r97', 15: 'r97', 18: 'r97'},
            6: {18: 'a'},
            7: {10: 'r98', 15: 'r98', 18: 'r98'},
            8: {11: 's14', 15: 's15'},
            9: {10: 'r1', 15: 'r1', 18: 'r1'},
            10: {8: 'r7', 11: 'r7', 13: 's18', 15: 'r7', 17: 's19', 22: 's25'},
            11: {6: 'r81', 7: 'r81', 9: 'r81', 11: 's28', 13: 's31', 15: 's33', 21: 's36', 22: 's34'},
            12: {9: 'r38', 11: 'r38', 15: 'r38'},
            13: {9: 's38', 11: 's14', 15: 's15'},
            14: {9: 'r4', 11: 'r4', 15: 'r4'},
            15: {9: 'r3', 11: 'r3', 15: 'r3'},
            16: {9: 'r21', 11: 'r21', 15: 'r21'},
            17: {0: 'r89', 6: 'r89', 8: 'r89', 9: 'r89', 11: 'r89', 13: 'r89', 15: 'r89', 17: 'r89', 19: 'r89', 20: 'r89', 22: 'r89'},
            18: {8: 'r7', 11: 'r7', 13: 's18', 15: 'r7', 17: 's19', 22: 's25'},
            19: {8: 'r5', 11: 'r5', 15: 'r5'},
            20: {8: 'r6', 11: 'r6', 15: 'r6'},
            21: {9: 's43'},
            22: {8: 's45', 11: 's47', 15: 's48'},
            23: {6: 'r62', 9: 'r62'},
            24: {6: 'r69', 8: 'r7', 9: 'r69', 11: 'r7', 13: 's18', 15: 'r7', 17: 's19', 20: 's52', 22: 's25'},
            25: {8: 'r7', 11: 'r7', 13: 's18', 15: 'r7', 17: 's19', 22: 's25'},
            26: {6: 'r64', 8: 'r64', 9: 'r64', 11: 'r64', 13: 'r64', 15: 'r64', 17: 'r64', 20: 'r64', 22: 'r64'},
            27: {0: 'r83', 6: 'r83', 7: 'r83', 9: 'r83', 11: 'r83', 13: 'r83', 15: 'r83', 19: 'r83', 22: 'r83'},
            28: {0: 'r85', 6: 'r85', 7: 'r85', 9: 'r85', 11: 'r85', 13: 'r85', 15: 'r85', 19: 'r85', 22: 'r85'},
            29: {6: 'r35', 7: 's56', 9: 'r35'},
            30: {6: 'r37', 7: 'r37', 9: 'r37', 11: 'r37', 13: 'r37', 15: 'r37', 22: 'r37'},
            31: {11: 's28', 13: 's31', 15: 's33', 22: 's34'},
            32: {6: 'r29', 9: 'r29'},
            33: {0: 'r51', 1: 's65', 5: 's62', 6: 'r51', 7: 'r51', 9: 'r51', 11: 'r51', 13: 'r51', 15: 'r51', 19: 'r51', 22: 'r51'},
            34: {11: 's28', 13: 's31', 15: 's33', 22: 's34'},
            35: {6: 'r79', 7: 'r79', 9: 'r79', 11: 's28', 13: 's31', 15: 's33', 22: 's34'},
            36: {6: 'r80', 7: 'r80', 9: 'r80'},
            37: {9: 's69'},
            38: {10: 'r73', 15: 'r73', 18: 'r73'},
            39: {9: 'r39', 11: 'r39', 15: 'r39'},
            40: {0: 'r101', 8: 'r7', 11: 'r7', 13: 's18', 15: 'r7', 17: 's19', 19: 'r101', 22: 's25'},
            41: {0: 'r19', 6: 's72', 8: 'r19', 11: 'r19', 13: 'r19', 15: 'r19', 17: 'r19', 19: 'r19', 22: 'r19'},
            42: {19: 's74'},
            43: {10: 'r92', 15: 'r92', 18: 'r92'},
            44: {0: 'r14', 1: 's65', 4: 's75', 5: 's62', 6: 'r14', 8: 'r14', 9: 'r14', 11: 'r14', 13: 'r14', 15: 'r14', 17: 'r14', 19: 'r14', 20: 'r14', 22: 'r14'},
            45: {0: 'r8', 1: 'r8', 4: 'r8', 5: 'r8', 6: 'r8', 8: 'r8', 9: 'r8', 11: 'r8', 13: 'r8', 15: 'r8', 17: 'r8', 19: 'r8', 20: 'r8', 22: 'r8'},
            46: {0: 'r11', 1: 'r11', 4: 'r11', 5: 'r11', 6: 'r11', 8: 'r11', 9: 'r11', 11: 'r11', 13: 'r11', 15: 'r11', 17: 'r11', 19: 'r11', 20: 'r11', 22: 'r11'},
            47: {0: 'r10', 1: 'r10', 4: 'r10', 5: 'r10', 6: 'r10', 8: 'r10', 9: 'r10', 11: 'r10', 13: 'r10', 15: 'r10', 17: 'r10', 19: 'r10', 20: 'r10', 22: 'r10'},
            48: {0: 'r9', 1: 'r9', 4: 'r9', 5: 'r9', 6: 'r9', 8: 'r9', 9: 'r9', 11: 'r9', 13: 'r9', 15: 'r9', 17: 'r9', 19: 'r9', 20: 'r9', 22: 'r9'},
            49: {6: 's80', 9: 'r91'},
            50: {6: 'r63', 8: 'r63', 9: 'r63', 11: 'r63', 13: 'r63', 15: 'r63', 17: 'r63', 20: 'r63', 22: 'r63'},
            51: {6: 'r90', 9: 'r90'},
            52: {15: 's82'},
            53: {6: 'r68', 9: 'r68'},
            54: {0: 's84'},
            55: {6: 'r78', 9: 'r78'},
            56: {13: 'r32', 15: 's86'},
            57: {6: 'r34', 9: 'r34'},
            58: {19: 's88'},
            59: {0: 'r99', 11: 's28', 13: 's31', 15: 's33', 19: 'r99', 22: 's34'},
            60: {0: 'r57', 6: 's90', 11: 'r57', 13: 'r57', 15: 'r57', 19: 'r57', 22: 'r57'},
            61: {6: 's94', 9: 'r82'},
            62: {0: 'r72', 6: 'r72', 7: 'r72', 8: 'r72', 9: 'r72', 11: 'r72', 13: 'r72', 15: 'r72', 16: 'r72', 17: 'r72', 19: 'r72', 20: 'r72', 22: 'r72'},
            63: {0: 'r50', 6: 'r50', 7: 'r50', 9: 'r50', 11: 'r50', 13: 'r50', 15: 'r50', 19: 'r50', 22: 'r50'},
            64: {0: 'r49', 6: 'r49', 7: 'r49', 9: 'r49', 11: 'r49', 13: 'r49', 15: 'r49', 19: 'r49', 22: 'r49'},
            65: {0: 'r71', 6: 'r71', 7: 'r71', 8: 'r71', 9: 'r71', 11: 'r71', 13: 'r71', 15: 'r71', 16: 'r71', 17: 'r71', 19: 'r71', 20: 'r71', 22: 'r71'},
            66: {0: 'r84', 6: 'r84', 7: 'r84', 9: 'r84', 11: 'r84', 13: 'r84', 15: 'r84', 19: 'r84', 22: 'r84'},
            67: {0: 's95'},
            68: {6: 'r36', 7: 'r36', 9: 'r36', 11: 'r36', 13: 'r36', 15: 'r36', 22: 'r36'},
            69: {10: 'r86', 15: 'r86', 18: 'r86'},
            70: {0: 'r18', 8: 'r18', 11: 'r18', 13: 'r18', 15: 'r18', 17: 'r18', 19: 'r18', 22: 'r18'},
            71: {0: 'r22', 6: 'r22', 19: 'r22'},
            72: {8: 'r7', 11: 'r7', 13: 's18', 15: 'r7', 17: 's19', 22: 's25'},
            73: {0: 'r102', 6: 's72', 19: 'r102'},
            74: {0: 'r17', 1: 's65', 4: 's75', 5: 's62', 6: 'r17', 8: 'r17', 9: 'r17', 11: 'r17', 13: 'r17', 15: 'r17', 17: 'r17', 19: 'r17', 20: 'r17', 22: 'r17'},
            75: {0: 'r95', 6: 'r95', 8: 'r95', 9: 'r95', 11: 'r95', 13: 'r95', 15: 'r95', 17: 'r95', 19: 'r95', 20: 'r95', 22: 'r95'},
            76: {0: 'r26', 6: 'r26', 8: 'r26', 9: 'r26', 11: 'r26', 13: 'r26', 15: 'r26', 16: 's101', 17: 'r26', 19: 'r26', 20: 'r26', 22: 'r26'},
            77: {0: 'r88', 6: 'r88', 8: 'r88', 9: 'r88', 11: 'r88', 13: 'r88', 15: 'r88', 17: 'r88', 19: 'r88', 20: 'r88', 22: 'r88'},
            78: {0: 'r12', 6: 'r12', 8: 'r12', 9: 'r12', 11: 'r12', 13: 'r12', 15: 'r12', 17: 'r12', 19: 'r12', 20: 'r12', 22: 'r12'},
            79: {0: 'r13', 6: 'r13', 8: 'r13', 9: 'r13', 11: 'r13', 13: 'r13', 15: 'r13', 17: 'r13', 19: 'r13', 20: 'r13', 22: 'r13'},
            80: {8: 'r7', 11: 'r7', 13: 's18', 15: 'r7', 17: 's19', 22: 's25'},
            81: {6: 'r61', 9: 'r61'},
            82: {3: 'r66', 15: 'r66'},
            83: {3: 's106', 15: 's105'},
            84: {0: 'r76', 6: 'r76', 8: 'r76', 9: 'r76', 11: 'r76', 13: 'r76', 15: 'r76', 17: 'r76', 19: 'r76', 20: 'r76', 22: 'r76'},
            85: {13: 's107'},
            86: {13: 'r30'},
            87: {13: 'r31'},
            88: {0: 'r54', 1: 's65', 5: 's62', 6: 'r54', 7: 'r54', 9: 'r54', 11: 'r54', 13: 'r54', 15: 'r54', 19: 'r54', 22: 'r54'},
            89: {0: 'r56', 11: 'r56', 13: 'r56', 15: 'r56', 19: 'r56', 22: 'r56'},
            90: {11: 's28', 13: 's31', 15: 's33', 22: 's34'},
            91: {0: 'r100', 6: 's90', 19: 'r100'},
            92: {0: 'r59', 6: 'r59', 19: 'r59'},
            93: {6: 'r28', 9: 'r28'},
            94: {6: 'r81', 7: 'r81', 9: 'r81', 11: 's28', 13: 's31', 15: 's33', 21: 's36', 22: 's34'},
            95: {0: 'r74', 6: 'r74', 7: 'r74', 9: 'r74', 11: 'r74', 13: 'r74', 15: 'r74', 19: 'r74', 22: 'r74'},
            96: {0: 'r20', 6: 'r20', 19: 'r20'},
            97: {0: 'r23', 6: 'r23', 19: 'r23'},
            98: {0: 'r16', 6: 'r16', 8: 'r16', 9: 'r16', 11: 'r16', 13: 'r16', 15: 'r16', 17: 'r16', 19: 'r16', 20: 'r16', 22: 'r16'},
            99: {0: 'r77', 6: 'r77', 8: 'r77', 9: 'r77', 11: 'r77', 13: 'r77', 15: 'r77', 17: 'r77', 19: 'r77', 20: 'r77', 22: 'r77'},
            100: {0: 'r15', 6: 'r15', 8: 'r15', 9: 'r15', 11: 'r15', 13: 'r15', 15: 'r15', 17: 'r15', 19: 'r15', 20: 'r15', 22: 'r15'},
            101: {0: 'r24', 6: 'r24', 8: 'r24', 9: 'r24', 11: 'r24', 13: 'r24', 15: 'r24', 17: 'r24', 19: 'r24', 20: 'r24', 22: 'r24'},
            102: {0: 'r94', 6: 'r94', 8: 'r94', 9: 'r94', 11: 'r94', 13: 'r94', 15: 'r94', 17: 'r94', 19: 'r94', 20: 'r94', 22: 'r94'},
            103: {0: 'r25', 6: 'r25', 8: 'r25', 9: 'r25', 11: 'r25', 13: 'r25', 15: 'r25', 17: 'r25', 19: 'r25', 20: 'r25', 22: 'r25'},
            104: {6: 'r55', 9: 'r55'},
            105: {3: 'r65', 15: 'r65'},
            106: {6: 'r67', 9: 'r67'},
            107: {2: 'r45', 5: 's116'},
            108: {6: 'r33', 9: 'r33'},
            109: {0: 'r75', 6: 'r75', 7: 'r75', 9: 'r75', 11: 'r75', 13: 'r75', 15: 'r75', 19: 'r75', 22: 'r75'},
            110: {0: 'r53', 6: 'r53', 7: 'r53', 9: 'r53', 11: 'r53', 13: 'r53', 15: 'r53', 19: 'r53', 22: 'r53'},
            111: {0: 'r52', 6: 'r52', 7: 'r52', 9: 'r52', 11: 'r52', 13: 'r52', 15: 'r52', 19: 'r52', 22: 'r52'},
            112: {0: 'r58', 6: 'r58', 19: 'r58'},
            113: {0: 'r60', 6: 'r60', 19: 'r60'},
            114: {6: 'r27', 9: 'r27'},
            115: {2: 'r44'},
            116: {2: 'r43'},
            117: {2: 's119'},
            118: {12: 'r42', 19: 'r42'},
            119: {6: 'r48', 9: 'r48', 12: 'r48', 13: 's107', 19: 'r48'},
            120: {12: 's125', 19: 's126'},
            121: {6: 'r47', 9: 'r47', 12: 'r47', 19: 'r47'},
            122: {6: 'r93', 9: 'r93', 12: 'r93', 19: 'r93'},
            123: {6: 'r46', 9: 'r46', 12: 'r46', 19: 'r46'},
            124: {12: 'r41', 19: 'r41'},
            125: {2: 'r45', 5: 's116'},
            126: {6: 'r87', 9: 'r87', 12: 'r87', 19: 'r87'},
            127: {12: 'r40', 19: 'r40'}
        }
        self.__goto_table = {
            0: {0: 5, 15: 7, 17: 4, 26: 1, 29: 2, 60: 6},
            2: {0: 5, 15: 7, 17: 9, 26: 1},
            8: {27: 13, 41: 16, 46: 12},
            10: {3: 22, 11: 24, 25: 20, 40: 17, 43: 26, 51: 21, 63: 23},
            11: {21: 30, 31: 27, 33: 35, 50: 29, 57: 32, 58: 37},
            13: {41: 16, 46: 39},
            18: {3: 22, 25: 20, 30: 42, 34: 40, 40: 17, 43: 41},
            22: {5: 44, 12: 46},
            23: {13: 49},
            24: {3: 22, 9: 51, 25: 20, 39: 53, 40: 17, 43: 50},
            25: {3: 22, 25: 20, 30: 54, 34: 40, 40: 17, 43: 41},
            29: {56: 57, 61: 55},
            31: {21: 60, 28: 58, 31: 27, 62: 59},
            32: {38: 61},
            33: {23: 64, 35: 63, 42: 66},
            34: {21: 60, 28: 67, 31: 27, 62: 59},
            35: {21: 68, 31: 27},
            40: {3: 22, 25: 20, 40: 17, 43: 70},
            41: {8: 71, 45: 73},
            44: {10: 79, 18: 78, 23: 76, 47: 77},
            49: {44: 81},
            52: {54: 83},
            56: {1: 87, 59: 85},
            59: {21: 89, 31: 27},
            60: {2: 92, 52: 91},
            61: {49: 93},
            72: {3: 22, 25: 20, 40: 17, 43: 96},
            73: {8: 97},
            74: {14: 98, 18: 100, 23: 76, 48: 99},
            76: {32: 102, 55: 103},
            80: {3: 22, 11: 24, 25: 20, 40: 17, 43: 26, 63: 104},
            85: {53: 108},
            88: {4: 109, 23: 111, 36: 110},
            90: {21: 112, 31: 27},
            91: {2: 113},
            94: {21: 30, 31: 27, 33: 35, 50: 29, 57: 114},
            107: {6: 117, 24: 118, 37: 115},
            118: {19: 120},
            119: {7: 121, 20: 122, 53: 123},
            120: {16: 124},
            125: {6: 117, 24: 127, 37: 115}
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
        self.__reduce_to_non_terminal_index = [29, 29, 41, 41, 25, 3, 3, 12, 12, 12, 5, 10, 47, 47, 14, 48, 48, 34, 34, 8, 46, 45, 45, 55, 32, 32, 49, 38, 38, 1, 59, 59, 56, 61, 61, 33, 33, 27, 27, 16, 19, 19, 37, 6, 6, 7, 20, 20, 35, 42, 42, 36, 4, 4, 44, 62, 62, 2, 52, 52, 13, 13, 11, 11, 54, 54, 39, 9, 9, 60, 23, 23, 26, 31, 31, 40, 40, 57, 50, 50, 50, 58, 21, 21, 21, 0, 53, 43, 43, 63, 51, 15, 24, 18, 18, 17, 17, 17, 28, 28, 30, 30]

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
