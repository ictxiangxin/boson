from .token import LexicalToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class BosonParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_7': 0,
            'string': 1,
            '!symbol_16': 2,
            '!symbol_11': 3,
            'regular': 4,
            '!symbol_4': 5,
            '!symbol_15': 6,
            '!symbol_8': 7,
            '!symbol_13': 8,
            '!symbol_2': 9,
            '!symbol_14': 10,
            '!symbol_1': 11,
            'command': 12,
            '$': 13,
            '!symbol_6': 14,
            'node': 15,
            '!symbol_12': 16,
            '!symbol_10': 17,
            '!symbol_3': 18,
            'name': 19,
            '!symbol_9': 20,
            '!symbol_5': 21
        }
        self.__sparse_action_table: dict = {
            0: {12: 's4', 19: 's8'},
            1: {13: 'a'},
            2: {12: 's4', 13: 'r54', 19: 's8'},
            3: {12: 'r23', 13: 'r23', 19: 'r23'},
            4: {1: 's90', 19: 's91'},
            5: {12: 'r45', 13: 'r45', 19: 'r45'},
            6: {12: 'r53', 13: 'r53', 19: 'r53'},
            7: {12: 'r57', 13: 'r57', 19: 'r57'},
            8: {7: 's9', 9: 's10'},
            9: {1: 's35', 3: 's37', 8: 's36', 9: 'r58', 11: 'r58', 17: 's29', 19: 's34', 20: 'r58'},
            10: {4: 's11'},
            11: {5: 'r63', 11: 'r63', 18: 's14'},
            12: {5: 's16', 11: 'r21'},
            13: {5: 'r37', 11: 'r37'},
            14: {5: 'r43', 11: 'r43'},
            15: {11: 'r48'},
            16: {21: 's19'},
            17: {11: 's18'},
            18: {12: 'r65', 13: 'r65', 19: 'r65'},
            19: {19: 's20'},
            20: {0: 'r32', 14: 'r32'},
            21: {14: 's22'},
            22: {11: 'r2'},
            23: {0: 's24', 14: 'r55'},
            24: {19: 's26'},
            25: {0: 'r7', 14: 'r7'},
            26: {0: 'r39', 14: 'r39'},
            27: {9: 's64', 11: 'r47', 20: 'r47'},
            28: {9: 'r18', 11: 'r18', 20: 'r18'},
            29: {9: 'r66', 11: 'r66', 20: 'r66'},
            30: {1: 's35', 3: 's37', 8: 's36', 9: 'r56', 10: 'r56', 11: 'r56', 16: 'r56', 19: 's34', 20: 'r56'},
            31: {1: 'r13', 3: 'r13', 8: 'r13', 9: 'r13', 10: 'r13', 11: 'r13', 16: 'r13', 19: 'r13', 20: 'r13'},
            32: {1: 'r64', 3: 'r64', 8: 'r64', 9: 'r64', 10: 'r64', 11: 'r64', 16: 'r64', 19: 'r64', 20: 'r64'},
            33: {1: 'r44', 2: 's54', 3: 'r44', 6: 's53', 8: 'r44', 9: 'r44', 10: 'r44', 11: 'r44', 16: 'r44', 19: 'r44', 20: 'r44'},
            34: {1: 'r16', 2: 'r16', 3: 'r16', 6: 'r16', 8: 'r16', 9: 'r16', 10: 'r16', 11: 'r16', 16: 'r16', 19: 'r16', 20: 'r16'},
            35: {1: 'r61', 2: 'r61', 3: 'r61', 6: 'r61', 8: 'r61', 9: 'r61', 10: 'r61', 11: 'r61', 16: 'r61', 19: 'r61', 20: 'r61'},
            36: {1: 's35', 3: 's37', 8: 's36', 19: 's34'},
            37: {1: 's35', 3: 's37', 8: 's36', 19: 's34'},
            38: {11: 's44'},
            39: {11: 'r41', 20: 'r41'},
            40: {11: 'r25', 20: 's41'},
            41: {1: 's35', 3: 's37', 8: 's36', 9: 'r58', 11: 'r58', 17: 's29', 19: 's34', 20: 'r58'},
            42: {11: 'r50', 20: 'r50'},
            43: {11: 'r8', 20: 'r8'},
            44: {12: 'r27', 13: 'r27', 19: 'r27'},
            45: {16: 's52'},
            46: {10: 'r5', 16: 'r5', 20: 's49'},
            47: {10: 'r46', 16: 'r46', 20: 's49'},
            48: {10: 'r49', 16: 'r49', 20: 'r49'},
            49: {1: 's35', 3: 's37', 8: 's36', 19: 's34'},
            50: {10: 'r52', 16: 'r52', 20: 'r52'},
            51: {10: 'r24', 16: 'r24', 20: 'r24'},
            52: {1: 'r44', 2: 's54', 3: 'r44', 6: 's53', 8: 'r44', 9: 'r44', 10: 'r44', 11: 'r44', 16: 'r44', 19: 'r44', 20: 'r44'},
            53: {1: 'r17', 3: 'r17', 8: 'r17', 9: 'r17', 10: 'r17', 11: 'r17', 16: 'r17', 19: 'r17', 20: 'r17'},
            54: {1: 'r69', 3: 'r69', 8: 'r69', 9: 'r69', 10: 'r69', 11: 'r69', 16: 'r69', 19: 'r69', 20: 'r69'},
            55: {1: 'r6', 3: 'r6', 8: 'r6', 9: 'r6', 10: 'r6', 11: 'r6', 16: 'r6', 19: 'r6', 20: 'r6'},
            56: {1: 'r33', 3: 'r33', 8: 'r33', 9: 'r33', 10: 'r33', 11: 'r33', 16: 'r33', 19: 'r33', 20: 'r33'},
            57: {1: 'r35', 3: 'r35', 8: 'r35', 9: 'r35', 10: 'r35', 11: 'r35', 16: 'r35', 19: 'r35', 20: 'r35'},
            58: {10: 's59'},
            59: {1: 'r12', 3: 'r12', 8: 'r12', 9: 'r12', 10: 'r12', 11: 'r12', 16: 'r12', 19: 'r12', 20: 'r12'},
            60: {1: 'r67', 3: 'r67', 8: 'r67', 9: 'r67', 10: 'r67', 11: 'r67', 16: 'r67', 19: 'r67', 20: 'r67'},
            61: {1: 'r19', 3: 'r19', 8: 'r19', 9: 'r19', 10: 'r19', 11: 'r19', 16: 'r19', 19: 'r19', 20: 'r19'},
            62: {11: 'r68', 20: 'r68'},
            63: {11: 'r31', 20: 'r31'},
            64: {3: 'r10', 8: 'r10', 19: 's65'},
            65: {3: 'r51', 8: 'r51'},
            66: {3: 's69', 8: 's70'},
            67: {3: 'r40', 8: 'r40'},
            68: {11: 'r1', 20: 'r1'},
            69: {6: 's73', 15: 'r28'},
            70: {15: 's71'},
            71: {10: 's72'},
            72: {0: 'r60', 11: 'r60', 16: 'r60', 20: 'r60'},
            73: {3: 'r34', 8: 'r34', 15: 'r34'},
            74: {0: 'r36', 16: 'r36'},
            75: {15: 's77'},
            76: {3: 'r20', 8: 'r20', 15: 'r20'},
            77: {0: 'r26', 3: 'r28', 6: 's73', 8: 'r28', 16: 'r26'},
            78: {0: 'r14', 16: 'r14'},
            79: {0: 'r42', 16: 'r42'},
            80: {3: 's69', 8: 's70'},
            81: {0: 'r22', 16: 'r22'},
            82: {0: 's84', 16: 's85'},
            83: {0: 'r30', 16: 'r30'},
            84: {6: 's73', 15: 'r28'},
            85: {0: 'r4', 11: 'r4', 16: 'r4', 20: 'r4'},
            86: {0: 'r59', 16: 'r59'},
            87: {1: 's90', 11: 's93', 19: 's91'},
            88: {1: 'r11', 11: 'r11', 19: 'r11'},
            89: {1: 'r62', 11: 'r62', 19: 'r62'},
            90: {1: 'r15', 11: 'r15', 19: 'r15'},
            91: {1: 'r38', 11: 'r38', 19: 'r38'},
            92: {1: 'r9', 11: 'r9', 19: 'r9'},
            93: {12: 'r3', 13: 'r3', 19: 'r3'},
            94: {12: 'r29', 13: 'r29', 19: 'r29'}
        }
        self.__sparse_goto_table: dict = {
            0: {5: 5, 12: 6, 14: 2, 36: 3, 37: 7, 41: 1},
            2: {5: 5, 12: 6, 36: 94, 37: 7},
            4: {16: 87, 18: 88, 44: 89},
            9: {0: 32, 2: 28, 3: 31, 7: 38, 21: 39, 27: 27, 31: 30, 34: 33},
            11: {10: 12, 29: 13},
            12: {19: 15, 24: 17},
            19: {25: 21},
            20: {32: 23},
            23: {17: 25},
            27: {23: 63, 40: 62},
            30: {0: 32, 3: 61, 34: 33},
            33: {13: 60, 15: 55, 43: 57},
            36: {0: 32, 2: 46, 3: 31, 6: 58, 31: 30, 34: 33},
            37: {0: 32, 2: 46, 3: 31, 6: 45, 31: 30, 34: 33},
            39: {4: 40},
            40: {9: 42},
            41: {0: 32, 2: 28, 3: 31, 21: 43, 27: 27, 31: 30, 34: 33},
            46: {26: 47, 39: 48},
            47: {39: 51},
            49: {0: 32, 2: 50, 3: 31, 31: 30, 34: 33},
            52: {13: 56, 15: 55, 43: 57},
            64: {8: 67, 42: 66},
            66: {28: 68},
            69: {30: 76, 33: 74, 35: 75},
            74: {1: 82},
            77: {20: 79, 22: 78, 30: 76, 35: 80},
            80: {28: 81},
            82: {38: 83},
            84: {30: 76, 33: 86, 35: 75},
            87: {18: 92, 44: 89}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            46: ('0', '*1'),
            52: ('1',),
            24: ('*0', '*1'),
            12: ('1',),
            33: ('1', '*3'),
            61: ('0',),
            67: ('0', '*1'),
            44: (),
            6: ('*0',),
            14: ('*0', '1', '*2'),
            22: ('*0', '1'),
            26: (),
            42: ('*0',),
            28: (),
            20: ('*0',),
            60: ('1',),
            4: ('1', '*2'),
            59: ('1',),
            36: (),
            30: ('*0', '*1'),
            56: ('*0',),
            19: ('*0', '1'),
            18: ('*0',),
            68: ('0', '*1'),
            1: ('*1', '2'),
            47: (),
            31: ('*0',),
            10: (),
            40: ('*0',),
            25: ('0', '*1'),
            8: ('1',),
            41: (),
            50: ('*0', '*1'),
            27: ('0', '2'),
            55: ('0', '*1'),
            39: ('1',),
            32: (),
            7: ('*0', '*1'),
            65: ('0', '2', '*3', '4'),
            2: ('*2',),
            21: (),
            48: ('*0',),
            63: (),
            37: ('*0',),
            3: ('0', '*1'),
            9: ('*0', '1'),
            29: ('*0', '1'),
            49: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 3, 4, 3, 4, 1, 1, 2, 2, 2, 0, 1, 3, 1, 3, 1, 1, 1, 1, 2, 1, 0, 2, 1, 2, 2, 0, 4, 0, 2, 2, 1, 0, 4, 1, 1, 0, 1, 1, 2, 1, 0, 1, 1, 0, 1, 2, 0, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 0, 2, 3, 1, 1, 0, 1, 6, 1, 2, 2, 1]
        self.__reduce_non_terminal_index: list = [11, 23, 19, 5, 28, 6, 13, 32, 9, 16, 42, 16, 0, 31, 33, 44, 34, 43, 27, 31, 35, 24, 20, 14, 26, 7, 22, 12, 35, 14, 1, 40, 32, 0, 30, 15, 1, 10, 44, 17, 42, 4, 22, 29, 13, 36, 6, 40, 24, 26, 4, 8, 39, 36, 41, 25, 2, 36, 27, 38, 28, 34, 18, 10, 3, 37, 27, 3, 21, 43]

    def parse(self, token_list: list) -> BosonGrammar:
        grammar = BosonGrammar()
        analysis_stack = [0]
        symbol_stack = []
        token_index = 0
        while token_index < len(token_list):
            token: LexicalToken = token_list[token_index]
            current_state = analysis_stack[-1]
            if token.symbol in self.__terminal_index_mapping:
                operation = self.__sparse_action_table.get(current_state, {}).get(self.__terminal_index_mapping[token.symbol], 'e')
            else:
                operation = 'e'
            operation_flag = operation[0]
            if operation_flag == 'e':
                grammar.error_index = token_index
                return grammar
            elif operation_flag == 's':
                analysis_stack.append(int(operation[1:]))
                token_index += 1
                grammar_node = BosonGrammarNode(token.text)
                symbol_stack.append(grammar_node)
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
                    for node_string in self.__sentence_index_grammar_tuple_mapping[statement_index]:
                        if node_string[0] == '*':
                            for node in symbol_package[int(node_string[1:])]:
                                grammar_node.append(node)
                        else:
                            grammar_node.append(symbol_package[int(node_string)])
                    grammar_node.set_reduce_number(statement_index)
                    symbol_stack.append(grammar_node)
                elif statement_index in {0, 5, 11, 13, 15, 16, 17, 23, 34, 35, 38, 43, 45, 51, 53, 54, 57, 58, 62, 64, 66, 69}:
                    grammar_node = BosonGrammarNode()
                    for _ in range(reduce_count):
                        grammar_node.insert(0, symbol_stack.pop())
                    grammar_node.set_reduce_number(statement_index)
                    symbol_stack.append(grammar_node)
                else:
                    raise ValueError('Invalid reduce number: reduce={}'.format(statement_index))
            elif operation_flag == 'a':
                grammar.grammar_tree = symbol_stack[0]
                return grammar
            else:
                raise ValueError('Invalid action: action={}'.format(operation))
        raise RuntimeError('Analyzer unusual exit.')
