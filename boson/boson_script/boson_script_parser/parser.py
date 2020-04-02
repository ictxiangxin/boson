from .token import LexicalToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class BosonParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_6': 0,
            '!symbol_12': 1,
            'command': 2,
            '!symbol_10': 3,
            '!symbol_2': 4,
            '!symbol_16': 5,
            '!symbol_13': 6,
            '!symbol_5': 7,
            'regular': 8,
            'string': 9,
            '!symbol_1': 10,
            '!symbol_8': 11,
            '!symbol_3': 12,
            '!symbol_14': 13,
            '$': 14,
            'node': 15,
            '!symbol_9': 16,
            '!symbol_4': 17,
            '!symbol_11': 18,
            '!symbol_15': 19,
            '!symbol_7': 20,
            'name': 21
        }
        self.__sparse_action_table: dict = {
            0: {2: 's8', 21: 's7'},
            1: {14: 'a'},
            2: {2: 's8', 14: 'r19', 21: 's7'},
            3: {2: 'r21', 14: 'r21', 21: 'r21'},
            4: {2: 'r8', 14: 'r8', 21: 'r8'},
            5: {2: 'r31', 14: 'r31', 21: 'r31'},
            6: {2: 'r46', 14: 'r46', 21: 'r46'},
            7: {4: 's16', 11: 's17'},
            8: {9: 's12', 21: 's11'},
            9: {9: 's12', 10: 's15', 21: 's11'},
            10: {9: 'r68', 10: 'r68', 21: 'r68'},
            11: {9: 'r22', 10: 'r22', 21: 'r22'},
            12: {9: 'r39', 10: 'r39', 21: 'r39'},
            13: {9: 'r11', 10: 'r11', 21: 'r11'},
            14: {9: 'r24', 10: 'r24', 21: 'r24'},
            15: {2: 'r4', 14: 'r4', 21: 'r4'},
            16: {8: 's75'},
            17: {3: 's22', 4: 'r15', 9: 's29', 10: 'r15', 13: 's18', 16: 'r15', 18: 's30', 21: 's28'},
            18: {9: 's29', 13: 's18', 18: 's30', 21: 's28'},
            19: {10: 's72'},
            20: {10: 'r28', 16: 'r28'},
            21: {4: 's46', 10: 'r35', 16: 'r35'},
            22: {4: 'r59', 10: 'r59', 16: 'r59'},
            23: {4: 'r67', 10: 'r67', 16: 'r67'},
            24: {1: 'r5', 4: 'r5', 9: 's29', 10: 'r5', 13: 's18', 16: 'r5', 18: 's30', 19: 'r5', 21: 's28'},
            25: {1: 'r16', 4: 'r16', 9: 'r16', 10: 'r16', 13: 'r16', 16: 'r16', 18: 'r16', 19: 'r16', 21: 'r16'},
            26: {1: 'r20', 4: 'r20', 9: 'r20', 10: 'r20', 13: 'r20', 16: 'r20', 18: 'r20', 19: 'r20', 21: 'r20'},
            27: {1: 'r62', 4: 'r62', 5: 's38', 6: 's37', 9: 'r62', 10: 'r62', 13: 'r62', 16: 'r62', 18: 'r62', 19: 'r62', 21: 'r62'},
            28: {1: 'r45', 4: 'r45', 5: 'r45', 6: 'r45', 9: 'r45', 10: 'r45', 13: 'r45', 16: 'r45', 18: 'r45', 19: 'r45', 21: 'r45'},
            29: {1: 'r61', 4: 'r61', 5: 'r61', 6: 'r61', 9: 'r61', 10: 'r61', 13: 'r61', 16: 'r61', 18: 'r61', 19: 'r61', 21: 'r61'},
            30: {9: 's29', 13: 's18', 18: 's30', 21: 's28'},
            31: {1: 'r38', 16: 's41', 19: 'r38'},
            32: {1: 's33'},
            33: {1: 'r62', 4: 'r62', 5: 's38', 6: 's37', 9: 'r62', 10: 'r62', 13: 'r62', 16: 'r62', 18: 'r62', 19: 'r62', 21: 'r62'},
            34: {1: 'r64', 4: 'r64', 9: 'r64', 10: 'r64', 13: 'r64', 16: 'r64', 18: 'r64', 19: 'r64', 21: 'r64'},
            35: {1: 'r9', 4: 'r9', 9: 'r9', 10: 'r9', 13: 'r9', 16: 'r9', 18: 'r9', 19: 'r9', 21: 'r9'},
            36: {1: 'r55', 4: 'r55', 9: 'r55', 10: 'r55', 13: 'r55', 16: 'r55', 18: 'r55', 19: 'r55', 21: 'r55'},
            37: {1: 'r23', 4: 'r23', 9: 'r23', 10: 'r23', 13: 'r23', 16: 'r23', 18: 'r23', 19: 'r23', 21: 'r23'},
            38: {1: 'r25', 4: 'r25', 9: 'r25', 10: 'r25', 13: 'r25', 16: 'r25', 18: 'r25', 19: 'r25', 21: 'r25'},
            39: {1: 'r51', 16: 's41', 19: 'r51'},
            40: {1: 'r60', 16: 'r60', 19: 'r60'},
            41: {9: 's29', 13: 's18', 18: 's30', 21: 's28'},
            42: {1: 'r56', 16: 'r56', 19: 'r56'},
            43: {1: 'r63', 16: 'r63', 19: 'r63'},
            44: {1: 'r54', 4: 'r54', 9: 'r54', 10: 'r54', 13: 'r54', 16: 'r54', 18: 'r54', 19: 'r54', 21: 'r54'},
            45: {1: 'r41', 4: 'r41', 9: 'r41', 10: 'r41', 13: 'r41', 16: 'r41', 18: 'r41', 19: 'r41', 21: 'r41'},
            46: {18: 'r17', 21: 's51'},
            47: {10: 'r40', 16: 'r40'},
            48: {10: 'r33', 16: 'r33'},
            49: {18: 's53'},
            50: {18: 'r37'},
            51: {18: 'r30'},
            52: {10: 'r53', 16: 'r53'},
            53: {6: 's57', 15: 'r47'},
            54: {1: 'r6', 20: 'r6'},
            55: {15: 's58'},
            56: {15: 'r50', 18: 'r50'},
            57: {15: 'r34', 18: 'r34'},
            58: {1: 'r7', 6: 's57', 18: 'r47', 20: 'r7'},
            59: {18: 's53'},
            60: {1: 'r66', 20: 'r66'},
            61: {1: 'r36', 20: 'r36'},
            62: {1: 'r65', 20: 'r65'},
            63: {1: 's65', 20: 's64'},
            64: {6: 's57', 15: 'r47'},
            65: {1: 'r32', 10: 'r32', 16: 'r32', 20: 'r32'},
            66: {1: 'r52', 20: 'r52'},
            67: {1: 'r48', 20: 'r48'},
            68: {10: 'r18', 16: 's70'},
            69: {10: 'r13', 16: 'r13'},
            70: {3: 's22', 4: 'r15', 9: 's29', 10: 'r15', 13: 's18', 16: 'r15', 18: 's30', 21: 's28'},
            71: {10: 'r3', 16: 'r3'},
            72: {2: 'r58', 14: 'r58', 21: 'r58'},
            73: {19: 's74'},
            74: {1: 'r10', 4: 'r10', 9: 'r10', 10: 'r10', 13: 'r10', 16: 'r10', 18: 'r10', 19: 'r10', 21: 'r10'},
            75: {10: 'r49', 12: 's78', 17: 'r49'},
            76: {10: 'r1', 17: 's79'},
            77: {10: 'r27', 17: 'r27'},
            78: {10: 'r42', 17: 'r42'},
            79: {7: 's83'},
            80: {10: 's82'},
            81: {10: 'r2'},
            82: {2: 'r44', 14: 'r44', 21: 'r44'},
            83: {21: 's85'},
            84: {0: 's90'},
            85: {0: 'r12', 20: 'r12'},
            86: {0: 'r43', 20: 's88'},
            87: {0: 'r26', 20: 'r26'},
            88: {21: 's89'},
            89: {0: 'r29', 20: 'r29'},
            90: {10: 'r57'},
            91: {2: 'r14', 14: 'r14', 21: 'r14'}
        }
        self.__sparse_goto_table: dict = {
            0: {1: 5, 22: 4, 24: 2, 30: 1, 32: 3, 44: 6},
            2: {1: 5, 22: 4, 32: 91, 44: 6},
            8: {8: 13, 33: 9, 43: 10},
            9: {8: 14, 43: 10},
            17: {3: 21, 6: 25, 15: 26, 16: 19, 19: 20, 34: 24, 40: 23, 42: 27},
            18: {6: 25, 15: 26, 21: 73, 34: 24, 40: 31, 42: 27},
            20: {27: 68},
            21: {23: 48, 31: 47},
            24: {6: 45, 15: 26, 42: 27},
            27: {0: 36, 2: 44, 17: 34},
            30: {6: 25, 15: 26, 21: 32, 34: 24, 40: 31, 42: 27},
            31: {29: 39, 37: 40},
            33: {0: 36, 2: 35, 17: 34},
            39: {37: 43},
            41: {6: 25, 15: 26, 34: 24, 40: 42, 42: 27},
            46: {4: 49, 12: 50},
            49: {25: 52},
            53: {7: 56, 9: 55, 11: 54},
            54: {20: 63},
            58: {7: 56, 9: 59, 38: 61, 41: 60},
            59: {25: 62},
            63: {10: 66},
            64: {7: 56, 9: 55, 11: 67},
            68: {13: 69},
            70: {3: 21, 6: 25, 15: 26, 19: 71, 34: 24, 40: 23, 42: 27},
            75: {5: 76, 39: 77},
            76: {14: 81, 35: 80},
            83: {36: 84},
            85: {18: 86},
            86: {28: 87}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            51: ('0', '*1'),
            56: ('1',),
            63: ('*0', '*1'),
            10: ('1',),
            9: ('1', '*3'),
            61: ('0',),
            54: ('0', '*1'),
            62: (),
            64: ('*0',),
            66: ('*0', '1', '*2'),
            65: ('*0', '1'),
            7: (),
            36: ('*0',),
            47: (),
            50: ('*0',),
            32: ('1', '*2'),
            48: ('1',),
            6: (),
            52: ('*0', '*1'),
            5: ('*0',),
            41: ('*0', '1'),
            67: ('*0',),
            40: ('0', '*1'),
            53: ('*1', '2'),
            35: (),
            33: ('*0',),
            17: (),
            37: ('*0',),
            18: ('0', '*1'),
            3: ('1',),
            28: (),
            13: ('*0', '*1'),
            58: ('0', '2'),
            43: ('0', '*1'),
            29: ('1',),
            12: (),
            26: ('*0', '*1'),
            44: ('0', '2', '*3', '4'),
            57: ('*2',),
            1: (),
            2: ('*0',),
            49: (),
            27: ('*0',),
            4: ('0', '*1'),
            24: ('*0', '1'),
            14: ('*0', '1'),
            60: ('*0',)
        }
        self.__reduce_symbol_count: list = [1, 0, 1, 2, 3, 1, 0, 0, 1, 4, 3, 1, 0, 2, 2, 0, 1, 0, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 0, 2, 1, 1, 4, 1, 1, 0, 1, 1, 1, 1, 2, 2, 1, 2, 6, 1, 1, 0, 2, 0, 1, 2, 2, 3, 2, 1, 2, 4, 4, 1, 1, 1, 0, 2, 1, 2, 3, 1, 1]
        self.__reduce_non_terminal_index: list = [26, 35, 35, 13, 1, 40, 20, 41, 32, 15, 15, 33, 18, 27, 24, 3, 34, 4, 16, 30, 6, 24, 43, 0, 33, 0, 18, 5, 27, 28, 12, 32, 25, 31, 7, 31, 41, 4, 21, 43, 19, 34, 39, 36, 22, 42, 32, 9, 10, 5, 9, 21, 20, 23, 6, 17, 37, 14, 44, 3, 29, 42, 2, 29, 2, 38, 11, 3, 8]

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
                elif statement_index in {0, 8, 11, 15, 16, 19, 20, 21, 22, 23, 25, 30, 31, 34, 38, 39, 42, 45, 46, 55, 59, 68}:
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
