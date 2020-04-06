from .token import LexicalToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class BosonParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_8': 0,
            '!symbol_7': 1,
            '!symbol_10': 2,
            '!symbol_6': 3,
            '$': 4,
            'node': 5,
            '!symbol_9': 6,
            '!symbol_5': 7,
            '!symbol_2': 8,
            'name': 9,
            '!symbol_16': 10,
            '!symbol_15': 11,
            'regular': 12,
            '!symbol_1': 13,
            '!symbol_13': 14,
            '!symbol_14': 15,
            '!symbol_12': 16,
            '!symbol_4': 17,
            '!symbol_11': 18,
            'command': 19,
            'string': 20,
            '!symbol_3': 21
        }
        self.__sparse_action_table: dict = {
            0: {9: 's7', 19: 's8'},
            1: {4: 'a'},
            2: {4: 'r65', 9: 's7', 19: 's8'},
            3: {4: 'r45', 9: 'r45', 19: 'r45'},
            4: {4: 'r7', 9: 'r7', 19: 'r7'},
            5: {4: 'r58', 9: 'r58', 19: 'r58'},
            6: {4: 'r66', 9: 'r66', 19: 'r66'},
            7: {0: 's16', 8: 's17'},
            8: {9: 's12', 20: 's13'},
            9: {9: 's12', 13: 's14', 20: 's13'},
            10: {9: 'r51', 13: 'r51', 20: 'r51'},
            11: {9: 'r10', 13: 'r10', 20: 'r10'},
            12: {9: 'r13', 13: 'r13', 20: 'r13'},
            13: {9: 'r41', 13: 'r41', 20: 'r41'},
            14: {4: 'r15', 9: 'r15', 19: 'r15'},
            15: {9: 'r67', 13: 'r67', 20: 'r67'},
            16: {2: 's37', 6: 'r52', 8: 'r52', 9: 's44', 13: 'r52', 14: 's45', 18: 's46', 20: 's43'},
            17: {12: 's18'},
            18: {13: 'r16', 17: 'r16', 21: 's21'},
            19: {13: 'r9', 17: 's23'},
            20: {13: 'r22', 17: 'r22'},
            21: {13: 'r42', 17: 'r42'},
            22: {13: 'r31'},
            23: {7: 's26'},
            24: {13: 's25'},
            25: {4: 'r36', 9: 'r36', 19: 'r36'},
            26: {9: 's27'},
            27: {1: 'r34', 3: 'r34'},
            28: {3: 's29'},
            29: {13: 'r55'},
            30: {1: 's32', 3: 'r12'},
            31: {1: 'r19', 3: 'r19'},
            32: {9: 's33'},
            33: {1: 'r49', 3: 'r49'},
            34: {13: 's93'},
            35: {6: 'r44', 13: 'r44'},
            36: {6: 'r61', 8: 's64', 13: 'r61'},
            37: {6: 'r6', 8: 'r6', 13: 'r6'},
            38: {6: 'r48', 8: 'r48', 13: 'r48'},
            39: {6: 'r40', 8: 'r40', 9: 's44', 13: 'r40', 14: 's45', 15: 'r40', 16: 'r40', 18: 's46', 20: 's43'},
            40: {6: 'r62', 8: 'r62', 9: 'r62', 13: 'r62', 14: 'r62', 15: 'r62', 16: 'r62', 18: 'r62', 20: 'r62'},
            41: {6: 'r3', 8: 'r3', 9: 'r3', 13: 'r3', 14: 'r3', 15: 'r3', 16: 'r3', 18: 'r3', 20: 'r3'},
            42: {6: 'r30', 8: 'r30', 9: 'r30', 10: 's59', 11: 's58', 13: 'r30', 14: 'r30', 15: 'r30', 16: 'r30', 18: 'r30', 20: 'r30'},
            43: {6: 'r29', 8: 'r29', 9: 'r29', 10: 'r29', 11: 'r29', 13: 'r29', 14: 'r29', 15: 'r29', 16: 'r29', 18: 'r29', 20: 'r29'},
            44: {6: 'r64', 8: 'r64', 9: 'r64', 10: 'r64', 11: 'r64', 13: 'r64', 14: 'r64', 15: 'r64', 16: 'r64', 18: 'r64', 20: 'r64'},
            45: {9: 's44', 14: 's45', 18: 's46', 20: 's43'},
            46: {9: 's44', 14: 's45', 18: 's46', 20: 's43'},
            47: {16: 's54'},
            48: {6: 's51', 15: 'r68', 16: 'r68'},
            49: {6: 's51', 15: 'r26', 16: 'r26'},
            50: {6: 'r21', 15: 'r21', 16: 'r21'},
            51: {9: 's44', 14: 's45', 18: 's46', 20: 's43'},
            52: {6: 'r59', 15: 'r59', 16: 'r59'},
            53: {6: 'r35', 15: 'r35', 16: 'r35'},
            54: {6: 'r30', 8: 'r30', 9: 'r30', 10: 's59', 11: 's58', 13: 'r30', 14: 'r30', 15: 'r30', 16: 'r30', 18: 'r30', 20: 'r30'},
            55: {6: 'r53', 8: 'r53', 9: 'r53', 13: 'r53', 14: 'r53', 15: 'r53', 16: 'r53', 18: 'r53', 20: 'r53'},
            56: {6: 'r46', 8: 'r46', 9: 'r46', 13: 'r46', 14: 'r46', 15: 'r46', 16: 'r46', 18: 'r46', 20: 'r46'},
            57: {6: 'r69', 8: 'r69', 9: 'r69', 13: 'r69', 14: 'r69', 15: 'r69', 16: 'r69', 18: 'r69', 20: 'r69'},
            58: {6: 'r4', 8: 'r4', 9: 'r4', 13: 'r4', 14: 'r4', 15: 'r4', 16: 'r4', 18: 'r4', 20: 'r4'},
            59: {6: 'r63', 8: 'r63', 9: 'r63', 13: 'r63', 14: 'r63', 15: 'r63', 16: 'r63', 18: 'r63', 20: 'r63'},
            60: {15: 's61'},
            61: {6: 'r8', 8: 'r8', 9: 'r8', 13: 'r8', 14: 'r8', 15: 'r8', 16: 'r8', 18: 'r8', 20: 'r8'},
            62: {6: 'r47', 8: 'r47', 9: 'r47', 13: 'r47', 14: 'r47', 15: 'r47', 16: 'r47', 18: 'r47', 20: 'r47'},
            63: {6: 'r2', 8: 'r2', 9: 'r2', 13: 'r2', 14: 'r2', 15: 'r2', 16: 'r2', 18: 'r2', 20: 'r2'},
            64: {9: 's69', 14: 'r33', 18: 'r33'},
            65: {6: 'r56', 13: 'r56'},
            66: {6: 'r23', 13: 'r23'},
            67: {14: 's71', 18: 's72'},
            68: {14: 'r43', 18: 'r43'},
            69: {14: 'r39', 18: 'r39'},
            70: {6: 'r27', 13: 'r27'},
            71: {5: 's87'},
            72: {5: 'r28', 11: 's76'},
            73: {1: 'r11', 16: 'r11'},
            74: {5: 's77'},
            75: {5: 'r38', 14: 'r38', 18: 'r38'},
            76: {5: 'r32', 14: 'r32', 18: 'r32'},
            77: {1: 'r37', 11: 's76', 14: 'r28', 16: 'r37', 18: 'r28'},
            78: {14: 's71', 18: 's72'},
            79: {1: 'r14', 16: 'r14'},
            80: {1: 'r25', 16: 'r25'},
            81: {1: 'r17', 16: 'r17'},
            82: {1: 's84', 16: 's85'},
            83: {1: 'r18', 16: 'r18'},
            84: {5: 'r28', 11: 's76'},
            85: {1: 'r54', 6: 'r54', 13: 'r54', 16: 'r54'},
            86: {1: 'r5', 16: 'r5'},
            87: {15: 's88'},
            88: {1: 'r50', 6: 'r50', 13: 'r50', 16: 'r50'},
            89: {6: 's90', 13: 'r1'},
            90: {2: 's37', 6: 'r52', 8: 'r52', 9: 's44', 13: 'r52', 14: 's45', 18: 's46', 20: 's43'},
            91: {6: 'r20', 13: 'r20'},
            92: {6: 'r57', 13: 'r57'},
            93: {4: 'r60', 9: 'r60', 19: 'r60'},
            94: {4: 'r24', 9: 'r24', 19: 'r24'}
        }
        self.__sparse_goto_table: dict = {
            0: {9: 5, 16: 1, 21: 2, 35: 4, 37: 6, 40: 3},
            2: {9: 5, 35: 4, 37: 6, 40: 94},
            8: {2: 9, 19: 10, 38: 11},
            9: {19: 15, 38: 11},
            16: {4: 40, 6: 42, 7: 35, 13: 36, 27: 38, 29: 41, 42: 34, 44: 39},
            18: {15: 20, 24: 19},
            19: {30: 24, 34: 22},
            26: {14: 28},
            27: {20: 30},
            30: {3: 31},
            35: {1: 89},
            36: {11: 66, 43: 65},
            39: {4: 63, 6: 42, 29: 41},
            42: {12: 56, 18: 62, 23: 57},
            45: {4: 40, 6: 42, 8: 60, 27: 48, 29: 41, 44: 39},
            46: {4: 40, 6: 42, 8: 47, 27: 48, 29: 41, 44: 39},
            48: {32: 49, 39: 50},
            49: {39: 53},
            51: {4: 40, 6: 42, 27: 52, 29: 41, 44: 39},
            54: {12: 56, 18: 55, 23: 57},
            64: {28: 68, 36: 67},
            67: {0: 70},
            72: {10: 74, 31: 73, 41: 75},
            73: {5: 82},
            77: {10: 78, 17: 80, 26: 79, 41: 75},
            78: {0: 81},
            82: {33: 83},
            84: {10: 74, 31: 86, 41: 75},
            89: {22: 91},
            90: {4: 40, 6: 42, 7: 92, 13: 36, 27: 38, 29: 41, 44: 39}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            26: ('0', '*1'),
            59: ('1',),
            35: ('*0', '*1'),
            8: ('1',),
            53: ('1', '*3'),
            29: ('0',),
            47: ('0', '*1'),
            30: (),
            46: ('*0',),
            14: ('*0', '1', '*2'),
            17: ('*0', '1'),
            37: (),
            25: ('*0',),
            28: (),
            38: ('*0',),
            50: ('1',),
            54: ('1', '*2'),
            5: ('1',),
            11: (),
            18: ('*0', '*1'),
            40: ('*0',),
            2: ('*0', '1'),
            48: ('*0',),
            56: ('0', '*1'),
            27: ('*1', '2'),
            61: (),
            23: ('*0',),
            33: (),
            43: ('*0',),
            1: ('0', '*1'),
            57: ('1',),
            44: (),
            20: ('*0', '*1'),
            60: ('0', '2'),
            12: ('0', '*1'),
            49: ('1',),
            34: (),
            19: ('*0', '*1'),
            36: ('0', '2', '*3', '4'),
            55: ('*2',),
            9: (),
            31: ('*0',),
            16: (),
            22: ('*0',),
            15: ('0', '*1'),
            67: ('*0', '1'),
            24: ('*0', '1'),
            21: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 2, 2, 1, 1, 2, 1, 1, 3, 0, 1, 0, 2, 1, 3, 3, 0, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 3, 0, 1, 0, 1, 1, 0, 0, 2, 6, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 2, 3, 1, 0, 4, 4, 4, 2, 2, 1, 2, 4, 0, 1, 1, 1, 1, 1, 2, 1, 1]
        self.__reduce_non_terminal_index: list = [25, 42, 44, 4, 23, 33, 13, 40, 29, 30, 19, 5, 14, 38, 31, 9, 24, 17, 5, 20, 1, 32, 24, 43, 21, 26, 8, 11, 10, 6, 18, 30, 41, 36, 20, 32, 35, 26, 10, 28, 27, 38, 15, 36, 1, 21, 18, 4, 13, 3, 0, 2, 13, 29, 0, 34, 7, 22, 40, 39, 37, 43, 44, 23, 6, 16, 40, 2, 8, 12]

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
                elif statement_index in {0, 3, 4, 6, 7, 10, 13, 32, 39, 41, 42, 45, 51, 52, 58, 62, 63, 64, 65, 66, 68, 69}:
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
