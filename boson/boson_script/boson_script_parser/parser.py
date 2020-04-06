from .token import LexicalToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class BosonParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_8': 0,
            '!symbol_6': 1,
            '$': 2,
            '!symbol_4': 3,
            '!symbol_15': 4,
            '!symbol_5': 5,
            'regular': 6,
            'string': 7,
            '!symbol_2': 8,
            '!symbol_7': 9,
            '!symbol_16': 10,
            '!symbol_11': 11,
            '!symbol_14': 12,
            'node': 13,
            'name': 14,
            '!symbol_12': 15,
            '!symbol_1': 16,
            '!symbol_10': 17,
            '!symbol_3': 18,
            'command': 19,
            '!symbol_13': 20,
            '!symbol_9': 21
        }
        self.__sparse_action_table: dict = {
            0: {14: 's8', 19: 's3'},
            1: {2: 'a'},
            2: {2: 'r66', 14: 's8', 19: 's3'},
            3: {7: 's88', 14: 's87'},
            4: {2: 'r5', 14: 'r5', 19: 'r5'},
            5: {2: 'r3', 14: 'r3', 19: 'r3'},
            6: {2: 'r46', 14: 'r46', 19: 'r46'},
            7: {2: 'r56', 14: 'r56', 19: 'r56'},
            8: {0: 's9', 8: 's10'},
            9: {7: 's38', 8: 'r17', 11: 's28', 12: 's27', 14: 's39', 16: 'r17', 17: 's32', 21: 'r17'},
            10: {6: 's11'},
            11: {3: 'r10', 16: 'r10', 18: 's13'},
            12: {3: 'r51', 16: 'r51'},
            13: {3: 'r12', 16: 'r12'},
            14: {3: 's17', 16: 'r52'},
            15: {16: 's26'},
            16: {16: 'r30'},
            17: {5: 's18'},
            18: {14: 's20'},
            19: {1: 's25'},
            20: {1: 'r67', 9: 'r67'},
            21: {1: 'r31', 9: 's23'},
            22: {1: 'r47', 9: 'r47'},
            23: {14: 's24'},
            24: {1: 'r57', 9: 'r57'},
            25: {16: 'r20'},
            26: {2: 'r54', 14: 'r54', 19: 'r54'},
            27: {7: 's38', 11: 's28', 12: 's27', 14: 's39'},
            28: {7: 's38', 11: 's28', 12: 's27', 14: 's39'},
            29: {16: 's72'},
            30: {16: 'r14', 21: 'r14'},
            31: {8: 's46', 16: 'r21', 21: 'r21'},
            32: {8: 'r18', 16: 'r18', 21: 'r18'},
            33: {8: 'r24', 16: 'r24', 21: 'r24'},
            34: {4: 'r65', 7: 's38', 8: 'r65', 11: 's28', 12: 's27', 14: 's39', 15: 'r65', 16: 'r65', 21: 'r65'},
            35: {4: 'r8', 7: 'r8', 8: 'r8', 11: 'r8', 12: 'r8', 14: 'r8', 15: 'r8', 16: 'r8', 21: 'r8'},
            36: {4: 'r44', 7: 'r44', 8: 'r44', 11: 'r44', 12: 'r44', 14: 'r44', 15: 'r44', 16: 'r44', 21: 'r44'},
            37: {4: 'r49', 7: 'r49', 8: 'r49', 10: 's43', 11: 'r49', 12: 'r49', 14: 'r49', 15: 'r49', 16: 'r49', 20: 's44', 21: 'r49'},
            38: {4: 'r39', 7: 'r39', 8: 'r39', 10: 'r39', 11: 'r39', 12: 'r39', 14: 'r39', 15: 'r39', 16: 'r39', 20: 'r39', 21: 'r39'},
            39: {4: 'r60', 7: 'r60', 8: 'r60', 10: 'r60', 11: 'r60', 12: 'r60', 14: 'r60', 15: 'r60', 16: 'r60', 20: 'r60', 21: 'r60'},
            40: {4: 'r53', 7: 'r53', 8: 'r53', 11: 'r53', 12: 'r53', 14: 'r53', 15: 'r53', 16: 'r53', 21: 'r53'},
            41: {4: 'r1', 7: 'r1', 8: 'r1', 11: 'r1', 12: 'r1', 14: 'r1', 15: 'r1', 16: 'r1', 21: 'r1'},
            42: {4: 'r34', 7: 'r34', 8: 'r34', 11: 'r34', 12: 'r34', 14: 'r34', 15: 'r34', 16: 'r34', 21: 'r34'},
            43: {4: 'r6', 7: 'r6', 8: 'r6', 11: 'r6', 12: 'r6', 14: 'r6', 15: 'r6', 16: 'r6', 21: 'r6'},
            44: {4: 'r62', 7: 'r62', 8: 'r62', 11: 'r62', 12: 'r62', 14: 'r62', 15: 'r62', 16: 'r62', 21: 'r62'},
            45: {4: 'r41', 7: 'r41', 8: 'r41', 11: 'r41', 12: 'r41', 14: 'r41', 15: 'r41', 16: 'r41', 21: 'r41'},
            46: {11: 'r9', 14: 's51'},
            47: {16: 'r26', 21: 'r26'},
            48: {16: 'r33', 21: 'r33'},
            49: {11: 's53'},
            50: {11: 'r40'},
            51: {11: 'r29'},
            52: {16: 'r48', 21: 'r48'},
            53: {13: 'r43', 20: 's57'},
            54: {9: 'r23', 15: 'r23'},
            55: {13: 's58'},
            56: {11: 'r37', 13: 'r37'},
            57: {11: 'r32', 13: 'r32'},
            58: {9: 'r25', 11: 'r43', 15: 'r25', 20: 's57'},
            59: {11: 's53'},
            60: {9: 'r16', 15: 'r16'},
            61: {9: 'r7', 15: 'r7'},
            62: {9: 'r45', 15: 'r45'},
            63: {9: 's65', 15: 's66'},
            64: {9: 'r68', 15: 'r68'},
            65: {13: 'r43', 20: 's57'},
            66: {9: 'r15', 15: 'r15', 16: 'r15', 21: 'r15'},
            67: {9: 'r36', 15: 'r36'},
            68: {16: 'r22', 21: 's70'},
            69: {16: 'r58', 21: 'r58'},
            70: {7: 's38', 8: 'r17', 11: 's28', 12: 's27', 14: 's39', 16: 'r17', 17: 's32', 21: 'r17'},
            71: {16: 'r63', 21: 'r63'},
            72: {2: 'r28', 14: 'r28', 19: 'r28'},
            73: {15: 's80'},
            74: {4: 'r35', 15: 'r35', 21: 's77'},
            75: {4: 'r50', 15: 'r50', 21: 's77'},
            76: {4: 'r38', 15: 'r38', 21: 'r38'},
            77: {7: 's38', 11: 's28', 12: 's27', 14: 's39'},
            78: {4: 'r64', 15: 'r64', 21: 'r64'},
            79: {4: 'r11', 15: 'r11', 21: 'r11'},
            80: {4: 'r49', 7: 'r49', 8: 'r49', 10: 's43', 11: 'r49', 12: 'r49', 14: 'r49', 15: 'r49', 16: 'r49', 20: 's44', 21: 'r49'},
            81: {4: 'r42', 7: 'r42', 8: 'r42', 11: 'r42', 12: 'r42', 14: 'r42', 15: 'r42', 16: 'r42', 21: 'r42'},
            82: {4: 's83'},
            83: {4: 'r19', 7: 'r19', 8: 'r19', 11: 'r19', 12: 'r19', 14: 'r19', 15: 'r19', 16: 'r19', 21: 'r19'},
            84: {7: 's88', 14: 's87', 16: 's89'},
            85: {7: 'r4', 14: 'r4', 16: 'r4'},
            86: {7: 'r27', 14: 'r27', 16: 'r27'},
            87: {7: 'r13', 14: 'r13', 16: 'r13'},
            88: {7: 'r59', 14: 'r59', 16: 'r59'},
            89: {2: 'r2', 14: 'r2', 19: 'r2'},
            90: {7: 'r61', 14: 'r61', 16: 'r61'},
            91: {2: 'r55', 14: 'r55', 19: 'r55'}
        }
        self.__sparse_goto_table: dict = {
            0: {0: 5, 8: 2, 13: 4, 17: 7, 37: 1, 42: 6},
            2: {0: 5, 13: 91, 17: 7, 42: 6},
            3: {22: 86, 32: 84, 33: 85},
            9: {7: 35, 14: 29, 19: 33, 20: 30, 29: 34, 31: 36, 35: 37, 38: 31},
            11: {21: 14, 23: 12},
            14: {2: 16, 24: 15},
            18: {16: 19},
            20: {41: 21},
            21: {36: 22},
            27: {7: 35, 19: 74, 29: 34, 31: 36, 35: 37, 40: 82},
            28: {7: 35, 19: 74, 29: 34, 31: 36, 35: 37, 40: 73},
            30: {39: 68},
            31: {6: 48, 9: 47},
            34: {7: 45, 31: 36, 35: 37},
            37: {3: 40, 18: 42, 27: 41},
            46: {15: 50, 44: 49},
            49: {11: 52},
            53: {4: 56, 28: 55, 34: 54},
            54: {1: 63},
            58: {4: 56, 5: 60, 26: 61, 28: 59},
            59: {11: 62},
            63: {43: 64},
            65: {4: 56, 28: 55, 34: 67},
            68: {30: 69},
            70: {7: 35, 19: 33, 20: 71, 29: 34, 31: 36, 35: 37, 38: 31},
            74: {10: 75, 25: 76},
            75: {25: 79},
            77: {7: 35, 19: 78, 29: 34, 31: 36, 35: 37},
            80: {3: 81, 18: 42, 27: 41},
            84: {22: 86, 33: 90}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            50: ('0', '*1'),
            64: ('1',),
            11: ('*0', '*1'),
            19: ('1',),
            42: ('1', '*3'),
            39: ('0',),
            53: ('0', '*1'),
            49: (),
            1: ('*0',),
            16: ('*0', '1', '*2'),
            45: ('*0', '1'),
            25: (),
            7: ('*0',),
            43: (),
            37: ('*0',),
            15: ('1', '*2'),
            36: ('1',),
            23: (),
            68: ('*0', '*1'),
            65: ('*0',),
            41: ('*0', '1'),
            24: ('*0',),
            26: ('0', '*1'),
            48: ('*1', '2'),
            21: (),
            33: ('*0',),
            9: (),
            40: ('*0',),
            22: ('0', '*1'),
            63: ('1',),
            14: (),
            58: ('*0', '*1'),
            28: ('0', '2'),
            31: ('0', '*1'),
            57: ('1',),
            67: (),
            47: ('*0', '*1'),
            54: ('0', '2', '*3', '4'),
            20: ('*2',),
            52: (),
            30: ('*0',),
            10: (),
            51: ('*0',),
            2: ('0', '*1'),
            61: ('*0', '1'),
            55: ('*0', '1'),
            38: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 1, 3, 1, 1, 1, 1, 1, 1, 0, 0, 2, 1, 1, 0, 4, 3, 0, 1, 3, 4, 0, 2, 0, 1, 0, 2, 1, 4, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 4, 0, 1, 2, 1, 2, 3, 0, 2, 1, 0, 2, 6, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 1, 0, 2]
        self.__reduce_non_terminal_index: list = [12, 3, 0, 13, 32, 8, 18, 5, 29, 44, 21, 10, 23, 22, 39, 11, 34, 38, 38, 31, 2, 9, 14, 1, 38, 5, 20, 33, 17, 15, 24, 16, 4, 9, 27, 40, 43, 28, 10, 35, 44, 29, 31, 28, 7, 26, 13, 41, 6, 3, 40, 21, 24, 7, 42, 8, 13, 36, 39, 22, 35, 32, 18, 30, 25, 19, 37, 41, 1]

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
                elif statement_index in {0, 3, 4, 5, 6, 8, 12, 13, 17, 18, 27, 29, 32, 34, 35, 44, 46, 56, 59, 60, 62, 66}:
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
