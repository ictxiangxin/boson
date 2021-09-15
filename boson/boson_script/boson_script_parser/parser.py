from .token import LexicalToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class BosonParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_6': 0,
            'node': 1,
            'regular': 2,
            '!symbol_12': 3,
            'command': 4,
            '!symbol_3': 5,
            '!symbol_5': 6,
            'name': 7,
            '!symbol_8': 8,
            '!symbol_16': 9,
            '!symbol_7': 10,
            'string': 11,
            '!symbol_9': 12,
            '!symbol_10': 13,
            '$': 14,
            '!symbol_1': 15,
            '!symbol_15': 16,
            '!symbol_13': 17,
            '!symbol_14': 18,
            '!symbol_2': 19,
            '!symbol_11': 20,
            '!symbol_4': 21
        }
        self.__sparse_action_table: dict = {
            0: {4: 's7', 7: 's8'},
            1: {14: 'a'},
            2: {4: 's7', 7: 's8', 14: 'r29'},
            3: {4: 'r56', 7: 'r56', 14: 'r56'},
            4: {4: 'r22', 7: 'r22', 14: 'r22'},
            5: {4: 'r43', 7: 'r43', 14: 'r43'},
            6: {4: 'r59', 7: 'r59', 14: 'r59'},
            7: {7: 's94', 11: 's93'},
            8: {8: 's9', 19: 's10'},
            9: {7: 's27', 11: 's28', 12: 'r61', 13: 's35', 15: 'r61', 17: 's29', 19: 'r61', 20: 's30'},
            10: {2: 's11'},
            11: {5: 's14', 15: 'r37', 21: 'r37'},
            12: {15: 'r23', 21: 's17'},
            13: {15: 'r64', 21: 'r64'},
            14: {15: 'r12', 21: 'r12'},
            15: {15: 's26'},
            16: {15: 'r52'},
            17: {6: 's18'},
            18: {7: 's20'},
            19: {0: 's25'},
            20: {0: 'r7', 10: 'r7'},
            21: {0: 'r65', 10: 's23'},
            22: {0: 'r31', 10: 'r31'},
            23: {7: 's24'},
            24: {0: 'r26', 10: 'r26'},
            25: {15: 'r45'},
            26: {4: 'r55', 7: 'r55', 14: 'r55'},
            27: {3: 'r40', 7: 'r40', 9: 'r40', 11: 'r40', 12: 'r40', 15: 'r40', 16: 'r40', 17: 'r40', 18: 'r40', 19: 'r40', 20: 'r40'},
            28: {3: 'r44', 7: 'r44', 9: 'r44', 11: 'r44', 12: 'r44', 15: 'r44', 16: 'r44', 17: 'r44', 18: 'r44', 19: 'r44', 20: 'r44'},
            29: {7: 's27', 11: 's28', 17: 's29', 20: 's30'},
            30: {7: 's27', 11: 's28', 17: 's29', 20: 's30'},
            31: {15: 's78'},
            32: {12: 'r39', 15: 'r39'},
            33: {12: 'r5', 15: 'r5', 19: 's47'},
            34: {12: 'r50', 15: 'r50', 19: 'r50'},
            35: {12: 'r73', 15: 'r73', 19: 'r73'},
            36: {3: 'r20', 7: 's27', 11: 's28', 12: 'r20', 15: 'r20', 17: 's29', 18: 'r20', 19: 'r20', 20: 's30'},
            37: {3: 'r71', 7: 'r71', 11: 'r71', 12: 'r71', 15: 'r71', 17: 'r71', 18: 'r71', 19: 'r71', 20: 'r71'},
            38: {3: 'r34', 7: 'r34', 11: 'r34', 12: 'r34', 15: 'r34', 17: 'r34', 18: 'r34', 19: 'r34', 20: 'r34'},
            39: {3: 'r46', 7: 'r46', 9: 's43', 11: 'r46', 12: 'r46', 15: 'r46', 16: 's42', 17: 'r46', 18: 'r46', 19: 'r46', 20: 'r46'},
            40: {3: 'r49', 7: 'r49', 11: 'r49', 12: 'r49', 15: 'r49', 17: 'r49', 18: 'r49', 19: 'r49', 20: 'r49'},
            41: {3: 'r42', 7: 'r42', 11: 'r42', 12: 'r42', 15: 'r42', 17: 'r42', 18: 'r42', 19: 'r42', 20: 'r42'},
            42: {3: 'r25', 7: 'r25', 11: 'r25', 12: 'r25', 15: 'r25', 17: 'r25', 18: 'r25', 19: 'r25', 20: 'r25'},
            43: {3: 'r28', 7: 'r28', 11: 'r28', 12: 'r28', 15: 'r28', 17: 'r28', 18: 'r28', 19: 'r28', 20: 'r28'},
            44: {3: 'r54', 7: 'r54', 11: 'r54', 12: 'r54', 15: 'r54', 17: 'r54', 18: 'r54', 19: 'r54', 20: 'r54'},
            45: {3: 'r69', 7: 'r69', 11: 'r69', 12: 'r69', 15: 'r69', 17: 'r69', 18: 'r69', 19: 'r69', 20: 'r69'},
            46: {12: 'r3', 15: 'r3'},
            47: {7: 's51', 17: 'r48', 20: 'r48'},
            48: {12: 'r58', 15: 'r58'},
            49: {17: 's53', 20: 's52'},
            50: {17: 'r67', 20: 'r67'},
            51: {17: 'r8', 20: 'r8'},
            52: {1: 'r30', 3: 'r63', 16: 's63'},
            53: {1: 's55'},
            54: {12: 'r1', 15: 'r1'},
            55: {18: 's56'},
            56: {3: 'r60', 10: 'r60', 12: 'r60', 15: 'r60'},
            57: {3: 's73'},
            58: {3: 'r68'},
            59: {3: 'r2'},
            60: {3: 'r9', 10: 'r9'},
            61: {1: 's64'},
            62: {1: 'r24', 17: 'r24', 20: 'r24'},
            63: {1: 'r35', 17: 'r35', 20: 'r35'},
            64: {3: 'r72', 10: 'r72', 16: 's63', 17: 'r30', 20: 'r30'},
            65: {17: 's53', 20: 's52'},
            66: {3: 'r17', 10: 'r17'},
            67: {3: 'r32', 10: 'r32'},
            68: {3: 'r21', 10: 'r21'},
            69: {3: 'r27', 10: 's71'},
            70: {3: 'r13', 10: 'r13'},
            71: {1: 'r30', 16: 's63'},
            72: {3: 'r18', 10: 'r18'},
            73: {3: 'r33', 10: 'r33', 12: 'r33', 15: 'r33'},
            74: {12: 's76', 15: 'r38'},
            75: {12: 'r16', 15: 'r16'},
            76: {7: 's27', 11: 's28', 12: 'r61', 13: 's35', 15: 'r61', 17: 's29', 19: 'r61', 20: 's30'},
            77: {12: 'r51', 15: 'r51'},
            78: {4: 'r6', 7: 'r6', 14: 'r6'},
            79: {3: 's86'},
            80: {3: 'r62', 12: 's81', 18: 'r62'},
            81: {7: 's27', 11: 's28', 17: 's29', 20: 's30'},
            82: {3: 'r10', 12: 's81', 18: 'r10'},
            83: {3: 'r70', 12: 'r70', 18: 'r70'},
            84: {3: 'r66', 12: 'r66', 18: 'r66'},
            85: {3: 'r11', 12: 'r11', 18: 'r11'},
            86: {3: 'r46', 7: 'r46', 9: 's43', 11: 'r46', 12: 'r46', 15: 'r46', 16: 's42', 17: 'r46', 18: 'r46', 19: 'r46', 20: 'r46'},
            87: {3: 'r41', 7: 'r41', 11: 'r41', 12: 'r41', 15: 'r41', 17: 'r41', 18: 'r41', 19: 'r41', 20: 'r41'},
            88: {18: 's89'},
            89: {3: 'r19', 7: 'r19', 11: 'r19', 12: 'r19', 15: 'r19', 17: 'r19', 18: 'r19', 19: 'r19', 20: 'r19'},
            90: {7: 's94', 11: 's93', 15: 's95'},
            91: {7: 'r4', 11: 'r4', 15: 'r4'},
            92: {7: 'r47', 11: 'r47', 15: 'r47'},
            93: {7: 'r14', 11: 'r14', 15: 'r14'},
            94: {7: 'r53', 11: 'r53', 15: 'r53'},
            95: {4: 'r15', 7: 'r15', 14: 'r15'},
            96: {7: 'r57', 11: 'r57', 15: 'r57'},
            97: {4: 'r36', 7: 'r36', 14: 'r36'}
        }
        self.__sparse_goto_table: dict = {
            0: {10: 1, 20: 3, 27: 4, 30: 5, 42: 2, 47: 6},
            2: {20: 97, 27: 4, 30: 5, 47: 6},
            7: {14: 90, 18: 91, 32: 92},
            9: {8: 31, 21: 37, 22: 32, 25: 34, 26: 39, 35: 36, 39: 33, 44: 38},
            11: {11: 12, 13: 13},
            12: {4: 16, 31: 15},
            18: {40: 19},
            20: {15: 21},
            21: {23: 22},
            29: {21: 37, 25: 80, 26: 39, 28: 88, 35: 36, 44: 38},
            30: {21: 37, 25: 80, 26: 39, 28: 79, 35: 36, 44: 38},
            32: {37: 74},
            33: {33: 46, 36: 48},
            36: {21: 45, 26: 39, 44: 38},
            39: {12: 40, 34: 44, 41: 41},
            47: {3: 49, 9: 50},
            49: {7: 54},
            52: {1: 58, 2: 59, 16: 60, 19: 57, 38: 61, 46: 62},
            60: {24: 69},
            64: {17: 67, 38: 65, 45: 66, 46: 62},
            65: {7: 68},
            69: {6: 70},
            71: {16: 72, 38: 61, 46: 62},
            74: {43: 75},
            76: {21: 37, 22: 77, 25: 34, 26: 39, 35: 36, 39: 33, 44: 38},
            80: {5: 82, 29: 83},
            81: {21: 37, 25: 85, 26: 39, 35: 36, 44: 38},
            82: {29: 84},
            86: {12: 40, 34: 87, 41: 41},
            90: {18: 96, 32: 92}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            10: ('0', '*1'),
            11: ('1',),
            66: ('*0', '*1'),
            19: ('1',),
            41: ('1', '*3'),
            44: ('0',),
            54: ('0', '*1'),
            46: (),
            49: ('*0',),
            17: ('*0', '1', '*2'),
            21: ('*0', '1'),
            72: (),
            32: ('*0',),
            30: (),
            24: ('*0',),
            27: ('0', '*1'),
            18: ('1',),
            9: (),
            13: ('*0', '*1'),
            60: ('1',),
            33: ('*1',),
            2: ('*0',),
            63: (),
            68: ('*0',),
            20: ('*0',),
            69: ('*0', '1'),
            58: ('0', '*1'),
            1: ('*1', '2'),
            5: (),
            3: ('*0',),
            48: (),
            67: ('*0',),
            38: ('0', '*1'),
            51: ('1',),
            39: (),
            16: ('*0', '*1'),
            6: ('0', '2'),
            65: ('0', '*1'),
            26: ('1',),
            7: (),
            31: ('*0', '*1'),
            55: ('0', '2', '*3', '4'),
            45: ('*2',),
            23: (),
            52: ('*0',),
            37: (),
            64: ('*0',),
            15: ('0', '*1'),
            57: ('*0', '1'),
            36: ('*0', '1'),
            70: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 3, 1, 1, 1, 0, 4, 0, 1, 0, 2, 2, 1, 2, 1, 3, 2, 3, 2, 3, 1, 2, 1, 0, 1, 1, 2, 2, 1, 1, 0, 2, 1, 3, 1, 1, 2, 0, 2, 0, 1, 4, 1, 1, 1, 4, 0, 1, 0, 1, 1, 2, 1, 1, 2, 6, 1, 2, 2, 1, 3, 0, 1, 0, 1, 2, 2, 1, 1, 2, 1, 1, 0, 1]
        self.__reduce_non_terminal_index: list = [0, 33, 1, 36, 14, 36, 30, 15, 9, 24, 28, 29, 13, 24, 32, 47, 37, 16, 6, 44, 25, 17, 20, 31, 38, 41, 23, 2, 41, 10, 38, 15, 45, 7, 21, 46, 42, 11, 8, 37, 26, 44, 12, 20, 26, 4, 34, 18, 3, 34, 39, 43, 31, 32, 21, 27, 42, 14, 22, 20, 7, 39, 28, 19, 11, 40, 5, 3, 19, 35, 5, 35, 45, 39]

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
                elif statement_index in {0, 4, 8, 12, 14, 22, 25, 28, 29, 34, 35, 40, 42, 43, 47, 50, 53, 56, 59, 61, 62, 71, 73}:
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
