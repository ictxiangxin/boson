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
            'bracket_l': 0,
            'star': 1,
            'brace_r': 2,
            'regular_expression': 3,
            'reduce': 4,
            'at': 5,
            'parentheses_l': 6,
            'internal_function': 7,
            'or': 8,
            'parentheses_r': 9,
            'null': 10,
            'plus': 11,
            'end': 12,
            'command': 13,
            'comma': 14,
            'assign': 15,
            'name': 16,
            'string': 17,
            'bracket_r': 18,
            'node': 19,
            'brace_l': 20,
            '$': 21
        }
        self.__action_table = {
            0: {13: 's7', 16: 's6'},
            1: {21: 'a'},
            2: {13: 'r95', 16: 'r95', 21: 'r95'},
            3: {13: 's7', 16: 's6', 21: 'r65'},
            4: {13: 'r2', 16: 'r2', 21: 'r2'},
            5: {13: 'r94', 16: 'r94', 21: 'r94'},
            6: {4: 's10', 15: 's11'},
            7: {16: 's16', 17: 's14'},
            8: {13: 'r96', 16: 'r96', 21: 'r96'},
            9: {13: 'r1', 16: 'r1', 21: 'r1'},
            10: {0: 's17', 6: 's25', 8: 'r76', 10: 's18', 12: 'r76', 15: 'r76', 16: 's21', 17: 's26'},
            11: {0: 's28', 3: 's29', 6: 's36', 16: 's35'},
            12: {12: 'r37', 16: 'r37', 17: 'r37'},
            13: {12: 's40', 16: 's16', 17: 's14'},
            14: {12: 'r4', 16: 'r4', 17: 'r4'},
            15: {12: 'r21', 16: 'r21', 17: 'r21'},
            16: {12: 'r3', 16: 'r3', 17: 'r3'},
            17: {0: 's17', 6: 's25', 16: 's21', 17: 's26'},
            18: {8: 'r75', 12: 'r75', 15: 'r75'},
            19: {8: 'r30', 12: 'r30', 15: 's45'},
            20: {0: 'r32', 6: 'r32', 8: 'r32', 12: 'r32', 15: 'r32', 16: 'r32', 17: 'r32'},
            21: {0: 'r46', 1: 's47', 6: 'r46', 8: 'r46', 9: 'r46', 11: 's48', 12: 'r46', 15: 'r46', 16: 'r46', 17: 'r46', 18: 'r46'},
            22: {0: 's17', 6: 's25', 8: 'r74', 12: 'r74', 15: 'r74', 16: 's21', 17: 's26'},
            23: {12: 's53'},
            24: {0: 'r78', 6: 'r78', 8: 'r78', 9: 'r78', 12: 'r78', 15: 'r78', 16: 'r78', 17: 'r78', 18: 'r78'},
            25: {0: 's17', 6: 's25', 16: 's21', 17: 's26'},
            26: {0: 'r80', 6: 'r80', 8: 'r80', 9: 'r80', 12: 'r80', 15: 'r80', 16: 'r80', 17: 'r80', 18: 'r80'},
            27: {8: 'r24', 12: 'r24'},
            28: {0: 's28', 6: 's36', 16: 's35'},
            29: {5: 's61', 12: 'r59'},
            30: {0: 's28', 5: 'r90', 6: 's36', 8: 'r90', 12: 'r90', 16: 's35'},
            31: {0: 'r83', 5: 'r83', 6: 'r83', 8: 'r83', 9: 'r83', 12: 'r83', 16: 'r83', 18: 'r83'},
            32: {12: 'r85'},
            33: {12: 's63'},
            34: {0: 'r9', 5: 'r9', 6: 'r9', 8: 'r9', 12: 'r9', 16: 'r9'},
            35: {0: 'r12', 1: 's47', 5: 'r12', 6: 'r12', 8: 'r12', 9: 'r12', 11: 's48', 12: 'r12', 16: 'r12', 18: 'r12'},
            36: {0: 's28', 6: 's36', 16: 's35'},
            37: {8: 'r62', 12: 'r62'},
            38: {5: 's71', 8: 'r7', 12: 'r7'},
            39: {12: 'r38', 16: 'r38', 17: 'r38'},
            40: {13: 'r68', 16: 'r68', 21: 'r68'},
            41: {0: 's17', 6: 's25', 9: 'r97', 16: 's21', 17: 's26', 18: 'r97'},
            42: {0: 'r51', 6: 'r51', 8: 's74', 9: 'r51', 16: 'r51', 17: 'r51', 18: 'r51'},
            43: {18: 's76'},
            44: {8: 'r29', 12: 'r29'},
            45: {6: 'r27', 16: 's79'},
            46: {8: 'r73', 12: 'r73'},
            47: {0: 'r67', 5: 'r67', 6: 'r67', 8: 'r67', 9: 'r67', 12: 'r67', 15: 'r67', 16: 'r67', 17: 'r67', 18: 'r67'},
            48: {0: 'r66', 5: 'r66', 6: 'r66', 8: 'r66', 9: 'r66', 12: 'r66', 15: 'r66', 16: 'r66', 17: 'r66', 18: 'r66'},
            49: {0: 'r45', 6: 'r45', 8: 'r45', 9: 'r45', 12: 'r45', 15: 'r45', 16: 'r45', 17: 'r45', 18: 'r45'},
            50: {0: 'r44', 6: 'r44', 8: 'r44', 9: 'r44', 12: 'r44', 15: 'r44', 16: 'r44', 17: 'r44', 18: 'r44'},
            51: {0: 'r79', 6: 'r79', 8: 'r79', 9: 'r79', 12: 'r79', 15: 'r79', 16: 'r79', 17: 'r79', 18: 'r79'},
            52: {0: 'r31', 6: 'r31', 8: 'r31', 12: 'r31', 15: 'r31', 16: 'r31', 17: 'r31'},
            53: {13: 'r81', 16: 'r81', 21: 'r81'},
            54: {9: 's80'},
            55: {8: 's82', 12: 'r77'},
            56: {0: 'r17', 6: 'r17', 8: 's85', 9: 'r17', 16: 'r17', 18: 'r17'},
            57: {0: 's28', 6: 's36', 9: 'r99', 16: 's35', 18: 'r99'},
            58: {18: 's87'},
            59: {12: 'r58'},
            60: {12: 'r86'},
            61: {20: 's88'},
            62: {0: 'r8', 5: 'r8', 6: 'r8', 8: 'r8', 12: 'r8', 16: 'r8'},
            63: {13: 'r92', 16: 'r92', 21: 'r92'},
            64: {0: 'r11', 5: 'r11', 6: 'r11', 8: 'r11', 9: 'r11', 12: 'r11', 16: 'r11', 18: 'r11'},
            65: {0: 'r84', 5: 'r84', 6: 'r84', 8: 'r84', 9: 'r84', 12: 'r84', 16: 'r84', 18: 'r84'},
            66: {0: 'r10', 5: 'r10', 6: 'r10', 8: 'r10', 9: 'r10', 12: 'r10', 16: 'r10', 18: 'r10'},
            67: {9: 's89'},
            68: {8: 's90', 12: 'r91'},
            69: {8: 'r6', 12: 'r6'},
            70: {8: 'r89', 12: 'r89'},
            71: {20: 's92'},
            72: {0: 'r50', 6: 'r50', 9: 'r50', 16: 'r50', 17: 'r50', 18: 'r50'},
            73: {8: 's74', 9: 'r98', 18: 'r98'},
            74: {0: 's17', 6: 's25', 16: 's21', 17: 's26'},
            75: {8: 'r53', 9: 'r53', 18: 'r53'},
            76: {0: 'r69', 6: 'r69', 8: 'r69', 9: 'r69', 12: 'r69', 15: 'r69', 16: 'r69', 17: 'r69', 18: 'r69'},
            77: {6: 'r26'},
            78: {6: 's95'},
            79: {6: 'r25'},
            80: {0: 'r49', 1: 's47', 6: 'r49', 8: 'r49', 9: 'r49', 11: 's48', 12: 'r49', 15: 'r49', 16: 'r49', 17: 'r49', 18: 'r49'},
            81: {8: 'r23', 12: 'r23'},
            82: {0: 's17', 6: 's25', 8: 'r76', 10: 's18', 12: 'r76', 15: 'r76', 16: 's21', 17: 's26'},
            83: {8: 's85', 9: 'r100', 18: 'r100'},
            84: {8: 'r19', 9: 'r19', 18: 'r19'},
            85: {0: 's28', 6: 's36', 16: 's35'},
            86: {0: 'r16', 6: 'r16', 9: 'r16', 16: 'r16', 18: 'r16'},
            87: {0: 'r71', 5: 'r71', 6: 'r71', 8: 'r71', 9: 'r71', 12: 'r71', 16: 'r71', 18: 'r71'},
            88: {7: 's105', 16: 's104'},
            89: {0: 'r15', 1: 's47', 5: 'r15', 6: 'r15', 8: 'r15', 9: 'r15', 11: 's48', 12: 'r15', 16: 'r15', 18: 'r15'},
            90: {0: 's28', 6: 's36', 16: 's35'},
            91: {8: 'r61', 12: 'r61'},
            92: {7: 's105', 16: 's104'},
            93: {8: 'r54', 9: 'r54', 18: 'r54'},
            94: {8: 'r52', 9: 'r52', 18: 'r52'},
            95: {1: 's113', 19: 'r40'},
            96: {8: 'r28', 12: 'r28'},
            97: {0: 'r70', 6: 'r70', 8: 'r70', 9: 'r70', 12: 'r70', 15: 'r70', 16: 'r70', 17: 'r70', 18: 'r70'},
            98: {0: 'r47', 6: 'r47', 8: 'r47', 9: 'r47', 12: 'r47', 15: 'r47', 16: 'r47', 17: 'r47', 18: 'r47'},
            99: {0: 'r48', 6: 'r48', 8: 'r48', 9: 'r48', 12: 'r48', 15: 'r48', 16: 'r48', 17: 'r48', 18: 'r48'},
            100: {8: 'r22', 12: 'r22'},
            101: {8: 'r20', 9: 'r20', 18: 'r20'},
            102: {8: 'r18', 9: 'r18', 18: 'r18'},
            103: {2: 'r56', 7: 'r56', 16: 'r56'},
            104: {2: 'r88', 7: 'r88', 16: 'r88'},
            105: {2: 'r87', 7: 'r87', 16: 'r87'},
            106: {2: 's118', 7: 's105', 16: 's104'},
            107: {0: 'r14', 5: 'r14', 6: 'r14', 8: 'r14', 9: 'r14', 12: 'r14', 16: 'r14', 18: 'r14'},
            108: {0: 'r13', 5: 'r13', 6: 'r13', 8: 'r13', 9: 'r13', 12: 'r13', 16: 'r13', 18: 'r13'},
            109: {0: 'r72', 5: 'r72', 6: 'r72', 8: 'r72', 9: 'r72', 12: 'r72', 16: 'r72', 18: 'r72'},
            110: {8: 'r60', 12: 'r60'},
            111: {2: 's119', 7: 's105', 16: 's104'},
            112: {2: 'r64', 7: 'r64', 16: 'r64'},
            113: {19: 'r36'},
            114: {19: 'r39'},
            115: {9: 'r35', 14: 'r35'},
            116: {19: 's122'},
            117: {2: 'r55', 7: 'r55', 16: 'r55'},
            118: {12: 'r57'},
            119: {8: 'r5', 12: 'r5'},
            120: {2: 'r63', 7: 'r63', 16: 'r63'},
            121: {9: 's124', 14: 's123'},
            122: {6: 's95', 8: 'r43', 9: 'r43', 12: 'r43', 14: 'r43'},
            123: {1: 's113', 19: 'r40'},
            124: {8: 'r82', 9: 'r82', 12: 'r82', 14: 'r82'},
            125: {9: 'r34', 14: 'r34'},
            126: {8: 'r93', 9: 'r93', 12: 'r93', 14: 'r93'},
            127: {8: 'r42', 9: 'r42', 12: 'r42', 14: 'r42'},
            128: {8: 'r41', 9: 'r41', 12: 'r41', 14: 'r41'},
            129: {9: 'r33', 14: 'r33'}
        }
        self.__goto_table = {
            0: {1: 5, 3: 2, 4: 8, 36: 1, 43: 3, 44: 4},
            3: {1: 5, 3: 2, 4: 8, 44: 9},
            7: {6: 13, 16: 12, 37: 15},
            10: {2: 24, 15: 27, 38: 20, 41: 23, 48: 22, 58: 19},
            11: {0: 31, 10: 30, 31: 33, 34: 37, 35: 32, 39: 38, 53: 34},
            13: {16: 39, 37: 15},
            17: {2: 24, 5: 41, 38: 42, 62: 43},
            19: {33: 46, 46: 44},
            21: {7: 49, 24: 50, 30: 51},
            22: {2: 24, 38: 52},
            25: {2: 24, 5: 41, 38: 42, 62: 54},
            27: {25: 55},
            28: {0: 31, 18: 57, 50: 58, 53: 56},
            29: {12: 60, 57: 59},
            30: {0: 31, 53: 62},
            35: {23: 64, 24: 66, 55: 65},
            36: {0: 31, 18: 57, 50: 67, 53: 56},
            37: {51: 68},
            38: {20: 69, 26: 70},
            41: {2: 24, 38: 72},
            42: {13: 73, 40: 75},
            45: {42: 78, 60: 77},
            55: {47: 81},
            56: {28: 84, 45: 83},
            57: {0: 31, 53: 86},
            68: {49: 91},
            73: {40: 93},
            74: {2: 24, 38: 94},
            78: {11: 96},
            80: {22: 97, 24: 98, 27: 99},
            82: {2: 24, 15: 100, 38: 20, 48: 22, 58: 19},
            83: {28: 101},
            85: {0: 31, 53: 102},
            88: {29: 103, 32: 106},
            89: {19: 107, 24: 108, 52: 109},
            90: {0: 31, 10: 30, 34: 110, 39: 38, 53: 34},
            92: {21: 111, 29: 112},
            95: {56: 114, 59: 115, 61: 116},
            106: {29: 117},
            111: {29: 120},
            115: {17: 121},
            121: {8: 125},
            122: {11: 128, 14: 126, 54: 127},
            123: {56: 114, 59: 129, 61: 116}
        }
        self.__node_table = {
            0: ('*0', '1'),
            37: ('*0', '1'),
            67: ('0', ('*1', ('?',))),
            91: ('0', '2'),
            54: ('*0', '1'),
            58: (),
            85: ('0', ('1', ('*2',))),
            60: ('*0', '1'),
            61: (),
            90: ('0', ('*1', ('1',))),
            62: ('*0', '1'),
            6: (),
            88: ('0', ('1', ('*2',))),
            7: ('*0', '1'),
            89: ('*0',),
            11: (),
            83: ('0', ('*1', ('?',))),
            14: (),
            71: ('1', ('*3', ('?',))),
            70: ('1',),
            15: ('*0', '1'),
            19: ('*0', '1'),
            98: ('*0',),
            99: ('0', ('*1', ('1',))),
            80: ('0', '2'),
            22: ('*0', '1'),
            23: (),
            76: ('0', ('*1', ('1',))),
            26: (),
            29: (),
            72: ('0', ('*1', (('*1', ('?',)), '2'))),
            30: ('*0', '1'),
            73: ('*0',),
            33: ('*0', '1'),
            34: (),
            81: ('1', ('*2', ('1',))),
            39: (),
            42: (),
            92: (('*0', ('?',)), '1', ('*2', ('?',))),
            45: (),
            78: ('0', ('*1', ('?',))),
            79: ('0',),
            48: (),
            69: ('1', ('*3', ('?',))),
            68: ('1',),
            49: ('*0', '1'),
            53: ('*0', '1'),
            96: ('*0',),
            97: ('0', ('*1', ('1',)))
        }
        self.__reduce_symbol_sum = [2, 1, 1, 1, 4, 1, 0, 2, 1, 1, 1, 0, 1, 1, 0, 2, 1, 2, 1, 2, 1, 2, 2, 0, 1, 1, 0, 3, 1, 0, 2, 1, 2, 2, 0, 1, 1, 2, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 2, 1, 2, 1, 2, 2, 1, 4, 1, 0, 2, 2, 0, 2, 1, 1, 1, 1, 3, 3, 4, 3, 4, 2, 1, 1, 0, 2, 1, 2, 1, 4, 4, 1, 2, 1, 2, 1, 1, 2, 1, 2, 4, 3, 1, 1, 1, 1, 2, 1, 2]
        self.__reduce_to_non_terminal_index = [43, 43, 37, 37, 20, 26, 26, 10, 10, 23, 55, 55, 19, 52, 52, 18, 18, 28, 45, 45, 16, 47, 25, 25, 60, 42, 42, 46, 33, 33, 48, 48, 8, 17, 17, 56, 6, 6, 61, 61, 54, 14, 14, 7, 30, 30, 27, 22, 22, 5, 5, 40, 13, 13, 32, 32, 57, 12, 12, 49, 51, 51, 21, 21, 36, 24, 24, 1, 2, 2, 0, 0, 15, 58, 58, 58, 41, 38, 38, 38, 3, 11, 53, 53, 31, 31, 29, 29, 34, 39, 35, 4, 59, 44, 44, 44, 62, 62, 50, 50]

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
                elif statement_index in [1, 2, 3, 4, 5, 8, 9, 10, 12, 13, 16, 17, 18, 20, 21, 24, 25, 27, 28, 31, 32, 35, 36, 38, 40, 41, 43, 44, 46, 47, 50, 51, 52, 55, 56, 57, 59, 63, 64, 65, 66, 74, 75, 77, 82, 84, 86, 87, 93, 94, 95]:
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
            67: 'command',
            91: 'lexical_define',
            85: 'regular_expression',
            83: 'lexical_name_closure',
            71: 'lexical_closure',
            70: 'lexical_optional',
            99: 'lexical_select',
            80: 'reduce',
            92: 'grammar_node',
            78: 'name_closure',
            79: 'literal',
            69: 'complex_closure',
            68: 'complex_optional',
            97: 'select'
        }
        self.__reduce_number_to_grammar_number = {
            64: 0,
            93: 1,
            95: 2,
            94: 3,
            84: 6,
            90: 8,
            88: 9,
            89: 10,
            82: 11,
            98: 15,
            86: 17,
            87: 18,
            76: 20,
            72: 21,
            73: 22,
            74: 23,
            75: 24,
            81: 25,
            77: 27,
            96: 32,
            65: 34,
            66: 35
        }
        self.__naive_reduce_number = {65, 2, 3, 66, 74, 75, 77, 79, 82, 84, 86, 87, 93, 94, 95}
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
