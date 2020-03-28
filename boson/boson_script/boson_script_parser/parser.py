from .token import LexicalToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class BosonParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_11': 0,
            '!symbol_13': 1,
            'command': 2,
            '!symbol_9': 3,
            'regular': 4,
            '!symbol_10': 5,
            '!symbol_4': 6,
            'string': 7,
            'node': 8,
            '!symbol_15': 9,
            '$': 10,
            '!symbol_1': 11,
            '!symbol_8': 12,
            '!symbol_3': 13,
            '!symbol_6': 14,
            '!symbol_2': 15,
            '!symbol_14': 16,
            '!symbol_12': 17,
            'name': 18,
            '!symbol_7': 19,
            '!symbol_16': 20,
            '!symbol_5': 21
        }
        self.__sparse_action_table: dict = {
            0: {2: 's7', 18: 's8'},
            1: {10: 'a'},
            2: {2: 's7', 10: 'r13', 18: 's8'},
            3: {2: 'r65', 10: 'r65', 18: 'r65'},
            4: {2: 'r12', 10: 'r12', 18: 'r12'},
            5: {2: 'r26', 10: 'r26', 18: 'r26'},
            6: {2: 'r48', 10: 'r48', 18: 'r48'},
            7: {7: 's87', 18: 's88'},
            8: {12: 's10', 15: 's9'},
            9: {4: 's68'},
            10: {0: 's14', 3: 'r1', 5: 's19', 7: 's11', 11: 'r1', 15: 'r1', 16: 's13', 18: 's12'},
            11: {0: 'r44', 1: 'r44', 3: 'r44', 7: 'r44', 9: 'r44', 11: 'r44', 15: 'r44', 16: 'r44', 17: 'r44', 18: 'r44', 20: 'r44'},
            12: {0: 'r59', 1: 'r59', 3: 'r59', 7: 'r59', 9: 'r59', 11: 'r59', 15: 'r59', 16: 'r59', 17: 'r59', 18: 'r59', 20: 'r59'},
            13: {0: 's14', 7: 's11', 16: 's13', 18: 's12'},
            14: {0: 's14', 7: 's11', 16: 's13', 18: 's12'},
            15: {11: 's56'},
            16: {3: 'r40', 11: 'r40'},
            17: {3: 'r60', 11: 'r60', 15: 's31'},
            18: {3: 'r2', 11: 'r2', 15: 'r2'},
            19: {3: 'r10', 11: 'r10', 15: 'r10'},
            20: {0: 's14', 3: 'r27', 7: 's11', 9: 'r27', 11: 'r27', 15: 'r27', 16: 's13', 17: 'r27', 18: 's12'},
            21: {0: 'r56', 3: 'r56', 7: 'r56', 9: 'r56', 11: 'r56', 15: 'r56', 16: 'r56', 17: 'r56', 18: 'r56'},
            22: {0: 'r35', 3: 'r35', 7: 'r35', 9: 'r35', 11: 'r35', 15: 'r35', 16: 'r35', 17: 'r35', 18: 'r35'},
            23: {0: 'r29', 1: 's27', 3: 'r29', 7: 'r29', 9: 'r29', 11: 'r29', 15: 'r29', 16: 'r29', 17: 'r29', 18: 'r29', 20: 's26'},
            24: {0: 'r25', 3: 'r25', 7: 'r25', 9: 'r25', 11: 'r25', 15: 'r25', 16: 'r25', 17: 'r25', 18: 'r25'},
            25: {0: 'r19', 3: 'r19', 7: 'r19', 9: 'r19', 11: 'r19', 15: 'r19', 16: 'r19', 17: 'r19', 18: 'r19'},
            26: {0: 'r23', 3: 'r23', 7: 'r23', 9: 'r23', 11: 'r23', 15: 'r23', 16: 'r23', 17: 'r23', 18: 'r23'},
            27: {0: 'r42', 3: 'r42', 7: 'r42', 9: 'r42', 11: 'r42', 15: 'r42', 16: 'r42', 17: 'r42', 18: 'r42'},
            28: {0: 'r52', 3: 'r52', 7: 'r52', 9: 'r52', 11: 'r52', 15: 'r52', 16: 'r52', 17: 'r52', 18: 'r52'},
            29: {0: 'r22', 3: 'r22', 7: 'r22', 9: 'r22', 11: 'r22', 15: 'r22', 16: 'r22', 17: 'r22', 18: 'r22'},
            30: {3: 'r63', 11: 'r63'},
            31: {0: 'r55', 18: 's35'},
            32: {3: 'r18', 11: 'r18'},
            33: {0: 's36'},
            34: {0: 'r67'},
            35: {0: 'r54'},
            36: {1: 's41', 8: 'r61'},
            37: {3: 'r39', 11: 'r39'},
            38: {17: 'r11', 19: 'r11'},
            39: {8: 's42'},
            40: {0: 'r7', 8: 'r7'},
            41: {0: 'r33', 8: 'r33'},
            42: {0: 'r61', 1: 's41', 17: 'r30', 19: 'r30'},
            43: {17: 'r53', 19: 'r53'},
            44: {17: 'r51', 19: 'r51'},
            45: {0: 's36'},
            46: {17: 'r38', 19: 'r38'},
            47: {17: 's50', 19: 's49'},
            48: {17: 'r66', 19: 'r66'},
            49: {1: 's41', 8: 'r61'},
            50: {3: 'r24', 11: 'r24', 17: 'r24', 19: 'r24'},
            51: {17: 'r21', 19: 'r21'},
            52: {3: 's53', 11: 'r62'},
            53: {0: 's14', 3: 'r1', 5: 's19', 7: 's11', 11: 'r1', 15: 'r1', 16: 's13', 18: 's12'},
            54: {3: 'r5', 11: 'r5'},
            55: {3: 'r50', 11: 'r50'},
            56: {2: 'r36', 10: 'r36', 18: 'r36'},
            57: {17: 's64'},
            58: {3: 's59', 9: 'r41', 17: 'r41'},
            59: {0: 's14', 7: 's11', 16: 's13', 18: 's12'},
            60: {3: 's59', 9: 'r37', 17: 'r37'},
            61: {3: 'r8', 9: 'r8', 17: 'r8'},
            62: {3: 'r4', 9: 'r4', 17: 'r4'},
            63: {3: 'r16', 9: 'r16', 17: 'r16'},
            64: {0: 'r29', 1: 's27', 3: 'r29', 7: 'r29', 9: 'r29', 11: 'r29', 15: 'r29', 16: 'r29', 17: 'r29', 18: 'r29', 20: 's26'},
            65: {0: 'r47', 3: 'r47', 7: 'r47', 9: 'r47', 11: 'r47', 15: 'r47', 16: 'r47', 17: 'r47', 18: 'r47'},
            66: {9: 's67'},
            67: {0: 'r15', 3: 'r15', 7: 'r15', 9: 'r15', 11: 'r15', 15: 'r15', 16: 'r15', 17: 'r15', 18: 'r15'},
            68: {6: 'r68', 11: 'r68', 13: 's71'},
            69: {6: 's72', 11: 'r58'},
            70: {6: 'r43', 11: 'r43'},
            71: {6: 'r3', 11: 'r3'},
            72: {21: 's76'},
            73: {11: 's75'},
            74: {11: 'r45'},
            75: {2: 'r20', 10: 'r20', 18: 'r20'},
            76: {18: 's78'},
            77: {14: 's83'},
            78: {14: 'r64', 19: 'r64'},
            79: {14: 'r34', 19: 's81'},
            80: {14: 'r28', 19: 'r28'},
            81: {18: 's82'},
            82: {14: 'r9', 19: 'r9'},
            83: {11: 'r57'},
            84: {7: 's87', 11: 's89', 18: 's88'},
            85: {7: 'r6', 11: 'r6', 18: 'r6'},
            86: {7: 'r17', 11: 'r17', 18: 'r17'},
            87: {7: 'r14', 11: 'r14', 18: 'r14'},
            88: {7: 'r32', 11: 'r32', 18: 'r32'},
            89: {2: 'r49', 10: 'r49', 18: 'r49'},
            90: {7: 'r31', 11: 'r31', 18: 'r31'},
            91: {2: 'r46', 10: 'r46', 18: 'r46'}
        }
        self.__sparse_goto_table: dict = {
            0: {0: 1, 2: 4, 13: 2, 26: 5, 28: 3, 41: 6},
            2: {2: 4, 26: 5, 28: 91, 41: 6},
            7: {11: 85, 15: 86, 25: 84},
            10: {18: 20, 19: 18, 20: 17, 31: 23, 32: 22, 34: 21, 35: 16, 37: 15},
            13: {8: 66, 18: 20, 19: 58, 31: 23, 32: 22, 34: 21},
            14: {8: 57, 18: 20, 19: 58, 31: 23, 32: 22, 34: 21},
            16: {9: 52},
            17: {23: 32, 29: 30},
            20: {31: 23, 32: 22, 34: 29},
            23: {5: 25, 33: 24, 44: 28},
            31: {4: 33, 16: 34},
            33: {42: 37},
            36: {7: 38, 10: 39, 38: 40},
            38: {14: 47},
            42: {10: 45, 12: 43, 36: 44, 38: 40},
            45: {42: 46},
            47: {1: 48},
            49: {7: 51, 10: 39, 38: 40},
            52: {43: 54},
            53: {18: 20, 19: 18, 20: 17, 31: 23, 32: 22, 34: 21, 35: 55},
            58: {17: 60, 21: 61},
            59: {18: 20, 19: 63, 31: 23, 32: 22, 34: 21},
            60: {21: 62},
            64: {5: 25, 33: 24, 44: 65},
            68: {6: 69, 24: 70},
            69: {27: 73, 40: 74},
            76: {22: 77},
            78: {39: 79},
            79: {30: 80},
            84: {11: 90, 15: 86}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            37: ('0', '*1'),
            16: ('1',),
            4: ('*0', '*1'),
            15: ('1',),
            47: ('1', '*3'),
            44: ('0',),
            52: ('0', '*1'),
            29: (),
            25: ('*0',),
            53: ('*0', '1', '*2'),
            38: ('*0', '1'),
            30: (),
            51: ('*0',),
            61: (),
            7: ('*0',),
            24: ('1', '*2'),
            21: ('1',),
            11: (),
            66: ('*0', '*1'),
            27: ('*0',),
            22: ('*0', '1'),
            2: ('*0',),
            18: ('0', '*1'),
            39: ('*1', '2'),
            60: (),
            63: ('*0',),
            55: (),
            67: ('*0',),
            62: ('0', '*1'),
            50: ('1',),
            40: (),
            5: ('*0', '*1'),
            36: ('0', '2'),
            34: ('0', '*1'),
            9: ('1',),
            64: (),
            28: ('*0', '*1'),
            20: ('0', '2', '*3', '4'),
            57: ('*2',),
            58: (),
            45: ('*0',),
            68: (),
            43: ('*0',),
            49: ('0', '*1'),
            31: ('*0', '1'),
            46: ('*0', '1'),
            8: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 0, 1, 1, 2, 2, 1, 1, 1, 2, 1, 0, 1, 1, 1, 3, 2, 1, 2, 1, 6, 2, 2, 1, 4, 1, 1, 1, 2, 0, 0, 2, 1, 1, 2, 1, 4, 2, 2, 3, 0, 1, 1, 1, 1, 1, 2, 4, 1, 3, 2, 1, 2, 3, 1, 0, 1, 4, 0, 1, 0, 0, 2, 1, 0, 1, 2, 1, 0]
        self.__reduce_non_terminal_index: list = [3, 20, 20, 24, 17, 9, 25, 10, 17, 30, 20, 14, 28, 0, 15, 32, 21, 11, 35, 33, 2, 1, 18, 5, 42, 44, 28, 19, 39, 44, 12, 25, 15, 38, 22, 34, 26, 8, 36, 29, 9, 8, 5, 6, 31, 27, 13, 32, 28, 41, 43, 12, 34, 7, 16, 4, 18, 40, 27, 31, 23, 10, 37, 23, 39, 13, 14, 4, 6]

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
                state_number = int(operation[1:])
                analysis_stack.append(state_number)
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
                elif statement_index in {0, 1, 3, 6, 10, 12, 13, 14, 17, 19, 23, 26, 32, 33, 35, 41, 42, 48, 54, 56, 59, 65}:
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
