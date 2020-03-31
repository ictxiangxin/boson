from .token import LexicalToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class BosonParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_2': 0,
            '$': 1,
            '!symbol_1': 2,
            '!symbol_9': 3,
            '!symbol_12': 4,
            '!symbol_15': 5,
            'regular': 6,
            '!symbol_11': 7,
            '!symbol_10': 8,
            '!symbol_8': 9,
            '!symbol_4': 10,
            'string': 11,
            '!symbol_13': 12,
            '!symbol_5': 13,
            'name': 14,
            '!symbol_16': 15,
            '!symbol_3': 16,
            'node': 17,
            '!symbol_14': 18,
            'command': 19,
            '!symbol_7': 20,
            '!symbol_6': 21
        }
        self.__sparse_action_table: dict = {
            0: {14: 's7', 19: 's8'},
            1: {1: 'a'},
            2: {1: 'r14', 14: 's7', 19: 's8'},
            3: {1: 'r68', 14: 'r68', 19: 'r68'},
            4: {1: 'r3', 14: 'r3', 19: 'r3'},
            5: {1: 'r7', 14: 'r7', 19: 'r7'},
            6: {1: 'r12', 14: 'r12', 19: 'r12'},
            7: {0: 's16', 9: 's17'},
            8: {11: 's9', 14: 's10'},
            9: {2: 'r23', 11: 'r23', 14: 'r23'},
            10: {2: 'r38', 11: 'r38', 14: 'r38'},
            11: {2: 's15', 11: 's9', 14: 's10'},
            12: {2: 'r48', 11: 'r48', 14: 'r48'},
            13: {2: 'r2', 11: 'r2', 14: 'r2'},
            14: {2: 'r42', 11: 'r42', 14: 'r42'},
            15: {1: 'r67', 14: 'r67', 19: 'r67'},
            16: {6: 's75'},
            17: {0: 'r41', 2: 'r41', 3: 'r41', 7: 's30', 8: 's24', 11: 's20', 14: 's22', 18: 's29'},
            18: {2: 's74'},
            19: {2: 'r10', 3: 'r10'},
            20: {0: 'r22', 2: 'r22', 3: 'r22', 4: 'r22', 5: 'r22', 7: 'r22', 11: 'r22', 12: 'r22', 14: 'r22', 15: 'r22', 18: 'r22'},
            21: {0: 's50', 2: 'r28', 3: 'r28'},
            22: {0: 'r35', 2: 'r35', 3: 'r35', 4: 'r35', 5: 'r35', 7: 'r35', 11: 'r35', 12: 'r35', 14: 'r35', 15: 'r35', 18: 'r35'},
            23: {0: 'r32', 2: 'r32', 3: 'r32'},
            24: {0: 'r66', 2: 'r66', 3: 'r66'},
            25: {0: 'r21', 2: 'r21', 3: 'r21', 4: 'r21', 5: 'r21', 7: 's30', 11: 's20', 14: 's22', 18: 's29'},
            26: {0: 'r51', 2: 'r51', 3: 'r51', 4: 'r51', 5: 'r51', 7: 'r51', 11: 'r51', 14: 'r51', 18: 'r51'},
            27: {0: 'r39', 2: 'r39', 3: 'r39', 4: 'r39', 5: 'r39', 7: 'r39', 11: 'r39', 12: 's41', 14: 'r39', 15: 's40', 18: 'r39'},
            28: {0: 'r26', 2: 'r26', 3: 'r26', 4: 'r26', 5: 'r26', 7: 'r26', 11: 'r26', 14: 'r26', 18: 'r26'},
            29: {7: 's30', 11: 's20', 14: 's22', 18: 's29'},
            30: {7: 's30', 11: 's20', 14: 's22', 18: 's29'},
            31: {4: 's38'},
            32: {3: 's35', 4: 'r30', 5: 'r30'},
            33: {3: 's35', 4: 'r60', 5: 'r60'},
            34: {3: 'r49', 4: 'r49', 5: 'r49'},
            35: {7: 's30', 11: 's20', 14: 's22', 18: 's29'},
            36: {3: 'r65', 4: 'r65', 5: 'r65'},
            37: {3: 'r36', 4: 'r36', 5: 'r36'},
            38: {0: 'r39', 2: 'r39', 3: 'r39', 4: 'r39', 5: 'r39', 7: 'r39', 11: 'r39', 12: 's41', 14: 'r39', 15: 's40', 18: 'r39'},
            39: {0: 'r29', 2: 'r29', 3: 'r29', 4: 'r29', 5: 'r29', 7: 'r29', 11: 'r29', 14: 'r29', 18: 'r29'},
            40: {0: 'r15', 2: 'r15', 3: 'r15', 4: 'r15', 5: 'r15', 7: 'r15', 11: 'r15', 14: 'r15', 18: 'r15'},
            41: {0: 'r56', 2: 'r56', 3: 'r56', 4: 'r56', 5: 'r56', 7: 'r56', 11: 'r56', 14: 'r56', 18: 'r56'},
            42: {0: 'r43', 2: 'r43', 3: 'r43', 4: 'r43', 5: 'r43', 7: 'r43', 11: 'r43', 14: 'r43', 18: 'r43'},
            43: {0: 'r19', 2: 'r19', 3: 'r19', 4: 'r19', 5: 'r19', 7: 'r19', 11: 'r19', 14: 'r19', 18: 'r19'},
            44: {5: 's45'},
            45: {0: 'r17', 2: 'r17', 3: 'r17', 4: 'r17', 5: 'r17', 7: 'r17', 11: 'r17', 14: 'r17', 18: 'r17'},
            46: {0: 'r24', 2: 'r24', 3: 'r24', 4: 'r24', 5: 'r24', 7: 'r24', 11: 'r24', 14: 'r24', 18: 'r24'},
            47: {0: 'r53', 2: 'r53', 3: 'r53', 4: 'r53', 5: 'r53', 7: 'r53', 11: 'r53', 14: 'r53', 18: 'r53'},
            48: {2: 'r59', 3: 'r59'},
            49: {2: 'r46', 3: 'r46'},
            50: {7: 'r37', 14: 's52'},
            51: {7: 'r45'},
            52: {7: 'r9'},
            53: {7: 's55'},
            54: {2: 'r16', 3: 'r16'},
            55: {12: 's59', 17: 'r5'},
            56: {4: 'r13', 20: 'r13'},
            57: {17: 's60'},
            58: {7: 'r58', 17: 'r58'},
            59: {7: 'r52', 17: 'r52'},
            60: {4: 'r18', 7: 'r5', 12: 's59', 20: 'r18'},
            61: {4: 'r47', 20: 'r47'},
            62: {4: 'r40', 20: 'r40'},
            63: {7: 's55'},
            64: {4: 'r20', 20: 'r20'},
            65: {4: 's68', 20: 's67'},
            66: {4: 'r63', 20: 'r63'},
            67: {12: 's59', 17: 'r5'},
            68: {2: 'r64', 3: 'r64', 4: 'r64', 20: 'r64'},
            69: {4: 'r44', 20: 'r44'},
            70: {2: 'r11', 3: 's71'},
            71: {0: 'r41', 2: 'r41', 3: 'r41', 7: 's30', 8: 's24', 11: 's20', 14: 's22', 18: 's29'},
            72: {2: 'r50', 3: 'r50'},
            73: {2: 'r6', 3: 'r6'},
            74: {1: 'r27', 14: 'r27', 19: 'r27'},
            75: {2: 'r54', 10: 'r54', 16: 's78'},
            76: {2: 'r57', 10: 's79'},
            77: {2: 'r1', 10: 'r1'},
            78: {2: 'r34', 10: 'r34'},
            79: {13: 's83'},
            80: {2: 's82'},
            81: {2: 'r61'},
            82: {1: 'r33', 14: 'r33', 19: 'r33'},
            83: {14: 's85'},
            84: {21: 's90'},
            85: {20: 'r25', 21: 'r25'},
            86: {20: 's87', 21: 'r8'},
            87: {14: 's89'},
            88: {20: 'r62', 21: 'r62'},
            89: {20: 'r4', 21: 'r4'},
            90: {2: 'r55'},
            91: {1: 'r31', 14: 'r31', 19: 'r31'}
        }
        self.__sparse_goto_table: dict = {
            0: {3: 4, 6: 6, 10: 3, 19: 2, 21: 5, 24: 1},
            2: {3: 4, 6: 6, 10: 91, 21: 5},
            8: {22: 11, 31: 12, 32: 13},
            11: {31: 14, 32: 13},
            17: {5: 25, 11: 28, 13: 18, 18: 27, 25: 21, 27: 23, 30: 19, 35: 26},
            19: {33: 70},
            21: {7: 48, 38: 49},
            25: {11: 28, 18: 27, 35: 47},
            27: {16: 46, 23: 39, 29: 43},
            29: {1: 44, 5: 25, 11: 28, 18: 27, 27: 32, 35: 26},
            30: {1: 31, 5: 25, 11: 28, 18: 27, 27: 32, 35: 26},
            32: {36: 33, 43: 34},
            33: {43: 37},
            35: {5: 25, 11: 28, 18: 27, 27: 36, 35: 26},
            38: {16: 42, 23: 39, 29: 43},
            50: {0: 51, 2: 53},
            53: {44: 54},
            55: {14: 58, 26: 56, 28: 57},
            56: {20: 65},
            60: {9: 61, 14: 58, 28: 63, 37: 62},
            63: {44: 64},
            65: {42: 66},
            67: {14: 58, 26: 69, 28: 57},
            70: {41: 72},
            71: {5: 25, 11: 28, 18: 27, 25: 21, 27: 23, 30: 73, 35: 26},
            75: {4: 77, 34: 76},
            76: {8: 80, 12: 81},
            83: {40: 84},
            85: {15: 86},
            86: {39: 88}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            60: ('0', '*1'),
            65: ('1',),
            36: ('*0', '*1'),
            17: ('1',),
            43: ('1', '*3'),
            22: ('0',),
            24: ('0', '*1'),
            39: (),
            19: ('*0',),
            47: ('*0', '1', '*2'),
            20: ('*0', '1'),
            18: (),
            40: ('*0',),
            5: (),
            58: ('*0',),
            64: ('1', '*2'),
            44: ('1',),
            13: (),
            63: ('*0', '*1'),
            21: ('*0',),
            53: ('*0', '1'),
            32: ('*0',),
            59: ('0', '*1'),
            16: ('*1', '2'),
            28: (),
            46: ('*0',),
            37: (),
            45: ('*0',),
            11: ('0', '*1'),
            6: ('1',),
            10: (),
            50: ('*0', '*1'),
            27: ('0', '2'),
            8: ('0', '*1'),
            4: ('1',),
            25: (),
            62: ('*0', '*1'),
            33: ('0', '2', '*3', '4'),
            55: ('*2',),
            57: (),
            61: ('*0',),
            54: (),
            1: ('*0',),
            67: ('0', '*1'),
            42: ('*0', '1'),
            31: ('*0', '1'),
            49: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 1, 1, 1, 2, 0, 2, 1, 2, 1, 0, 2, 1, 0, 1, 1, 3, 3, 0, 1, 2, 1, 1, 1, 2, 0, 1, 4, 0, 1, 1, 2, 1, 6, 1, 1, 2, 0, 1, 0, 1, 0, 2, 4, 2, 1, 1, 3, 1, 1, 2, 1, 1, 2, 0, 4, 1, 0, 1, 2, 2, 1, 2, 2, 4, 2, 1, 3, 1]
        self.__reduce_non_terminal_index: list = [17, 34, 31, 10, 39, 28, 41, 10, 40, 0, 33, 13, 10, 20, 24, 23, 38, 11, 9, 16, 37, 27, 18, 32, 35, 15, 35, 3, 7, 29, 1, 19, 25, 6, 4, 18, 36, 2, 32, 16, 9, 25, 22, 11, 42, 2, 7, 26, 22, 36, 33, 5, 14, 5, 34, 12, 23, 8, 28, 30, 1, 8, 15, 20, 44, 43, 25, 21, 19]

    def parse(self, token_list: list) -> BosonGrammar:
        grammar = BosonGrammar()
        analysis_stack = [0]
        symbol_stack = []
        token_index = 0
        while token_index < len(token_list):
            token: LexicalToken = token_list[token_index]
            current_state = analysis_stack[-1]
            operation = self.__sparse_action_table.get(current_state, {}).get(self.__terminal_index_mapping[token.symbol], 'e')
            operation_flag = operation[0]
            if operation_flag == 'e':
                grammar.error_index = token_index
                return grammar
            elif operation_flag == 's':
                analysis_stack.append(int(operation[1:]))
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
                elif statement_index in {0, 2, 3, 7, 9, 12, 14, 15, 23, 26, 29, 30, 34, 35, 38, 41, 48, 51, 52, 56, 66, 68}:
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
