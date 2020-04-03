from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            'escape_character': 0,
            'normal_character': 1,
            '!symbol_8': 2,
            '$': 3,
            '!symbol_10': 4,
            '!symbol_4': 5,
            '!symbol_3': 6,
            '!symbol_1': 7,
            '!symbol_5': 8,
            '!symbol_7': 9,
            '!symbol_2': 10,
            'reference': 11,
            '!symbol_6': 12,
            '!symbol_14': 13,
            'single_number': 14,
            '!symbol_12': 15,
            '!symbol_13': 16,
            '!symbol_11': 17,
            '!symbol_9': 18
        }
        self.__sparse_action_table: dict = {
            0: {0: 's11', 1: 's12', 6: 's16', 10: 's8', 11: 's15', 12: 's14', 14: 's13'},
            1: {3: 'a'},
            2: {3: 'r13'},
            3: {3: 'r31', 7: 'r31', 9: 'r31'},
            4: {0: 's11', 1: 's12', 3: 'r17', 6: 's16', 7: 'r17', 9: 'r17', 10: 's8', 11: 's15', 12: 's14', 14: 's13'},
            5: {0: 'r8', 1: 'r8', 3: 'r8', 6: 'r8', 7: 'r8', 9: 'r8', 10: 'r8', 11: 'r8', 12: 'r8', 14: 'r8'},
            6: {0: 'r16', 1: 'r16', 3: 'r16', 4: 's35', 6: 'r16', 7: 'r16', 9: 'r16', 10: 'r16', 11: 'r16', 12: 'r16', 14: 'r16', 15: 's33', 17: 's32', 18: 's34'},
            7: {0: 'r12', 1: 'r12', 3: 'r12', 4: 'r12', 6: 'r12', 7: 'r12', 9: 'r12', 10: 'r12', 11: 'r12', 12: 'r12', 14: 'r12', 15: 'r12', 17: 'r12', 18: 'r12'},
            8: {0: 'r24', 1: 'r24', 3: 'r24', 4: 'r24', 6: 'r24', 7: 'r24', 9: 'r24', 10: 'r24', 11: 'r24', 12: 'r24', 14: 'r24', 15: 'r24', 17: 'r24', 18: 'r24'},
            9: {0: 'r25', 1: 'r25', 3: 'r25', 4: 'r25', 6: 'r25', 7: 'r25', 9: 'r25', 10: 'r25', 11: 'r25', 12: 'r25', 14: 'r25', 15: 'r25', 17: 'r25', 18: 'r25'},
            10: {0: 'r27', 1: 'r27', 3: 'r27', 4: 'r27', 6: 'r27', 7: 'r27', 9: 'r27', 10: 'r27', 11: 'r27', 12: 'r27', 14: 'r27', 15: 'r27', 17: 'r27', 18: 'r27'},
            11: {0: 'r33', 1: 'r33', 3: 'r33', 4: 'r33', 6: 'r33', 7: 'r33', 8: 'r33', 9: 'r33', 10: 'r33', 11: 'r33', 12: 'r33', 14: 'r33', 15: 'r33', 17: 'r33', 18: 'r33'},
            12: {0: 'r14', 1: 'r14', 2: 'r14', 3: 'r14', 4: 'r14', 6: 'r14', 7: 'r14', 8: 'r14', 9: 'r14', 10: 'r14', 11: 'r14', 12: 'r14', 14: 'r14', 15: 'r14', 17: 'r14', 18: 'r14'},
            13: {0: 'r26', 1: 'r26', 2: 'r26', 3: 'r26', 4: 'r26', 6: 'r26', 7: 'r26', 8: 'r26', 9: 'r26', 10: 'r26', 11: 'r26', 12: 'r26', 14: 'r26', 15: 'r26', 17: 'r26', 18: 'r26'},
            14: {0: 's11', 1: 's12', 6: 's16', 10: 's8', 11: 's15', 12: 's14', 14: 's13'},
            15: {0: 'r21', 1: 'r21', 3: 'r21', 4: 'r21', 6: 'r21', 7: 'r21', 9: 'r21', 10: 'r21', 11: 'r21', 12: 'r21', 14: 'r21', 15: 'r21', 17: 'r21', 18: 'r21'},
            16: {0: 'r6', 1: 'r6', 5: 's17', 14: 'r6'},
            17: {0: 'r37', 1: 'r37', 14: 'r37'},
            18: {0: 's11', 1: 's12', 14: 's13'},
            19: {0: 'r39', 1: 'r39', 14: 'r39'},
            20: {0: 'r27', 1: 'r27', 2: 's26', 8: 'r27', 14: 'r27'},
            21: {0: 's11', 1: 's12', 8: 's24', 14: 's13'},
            22: {0: 'r4', 1: 'r4', 8: 'r4', 14: 'r4'},
            23: {0: 'r22', 1: 'r22', 8: 'r22', 14: 'r22'},
            24: {0: 'r30', 1: 'r30', 3: 'r30', 4: 'r30', 6: 'r30', 7: 'r30', 9: 'r30', 10: 'r30', 11: 'r30', 12: 'r30', 14: 'r30', 15: 'r30', 17: 'r30', 18: 'r30'},
            25: {0: 'r7', 1: 'r7', 8: 'r7', 14: 'r7'},
            26: {1: 's12', 14: 's13'},
            27: {0: 'r23', 1: 'r23', 8: 'r23', 14: 'r23'},
            28: {9: 's29'},
            29: {0: 'r1', 1: 'r1', 3: 'r1', 4: 'r1', 6: 'r1', 7: 'r1', 9: 'r1', 10: 'r1', 11: 'r1', 12: 'r1', 14: 'r1', 15: 'r1', 17: 'r1', 18: 'r1'},
            30: {0: 'r10', 1: 'r10', 3: 'r10', 6: 'r10', 7: 'r10', 9: 'r10', 10: 'r10', 11: 'r10', 12: 'r10', 14: 'r10'},
            31: {0: 'r20', 1: 'r20', 3: 'r20', 6: 'r20', 7: 'r20', 9: 'r20', 10: 'r20', 11: 'r20', 12: 'r20', 14: 'r20'},
            32: {0: 'r5', 1: 'r5', 3: 'r5', 6: 'r5', 7: 'r5', 9: 'r5', 10: 'r5', 11: 'r5', 12: 'r5', 14: 'r5'},
            33: {14: 's38'},
            34: {0: 'r35', 1: 'r35', 3: 'r35', 6: 'r35', 7: 'r35', 9: 'r35', 10: 'r35', 11: 'r35', 12: 'r35', 14: 'r35'},
            35: {0: 'r38', 1: 'r38', 3: 'r38', 6: 'r38', 7: 'r38', 9: 'r38', 10: 'r38', 11: 'r38', 12: 'r38', 14: 'r38'},
            36: {0: 'r40', 1: 'r40', 3: 'r40', 6: 'r40', 7: 'r40', 9: 'r40', 10: 'r40', 11: 'r40', 12: 'r40', 14: 'r40'},
            37: {13: 's41', 16: 's42'},
            38: {13: 'r3', 14: 'r3', 16: 'r3'},
            39: {13: 'r15', 14: 's40', 16: 'r15'},
            40: {13: 'r9', 14: 'r9', 16: 'r9'},
            41: {0: 'r19', 1: 'r19', 3: 'r19', 6: 'r19', 7: 'r19', 9: 'r19', 10: 'r19', 11: 'r19', 12: 'r19', 14: 'r19'},
            42: {13: 'r2', 14: 's38'},
            43: {13: 'r18'},
            44: {13: 'r32'},
            45: {13: 's46'},
            46: {0: 'r36', 1: 'r36', 3: 'r36', 6: 'r36', 7: 'r36', 9: 'r36', 10: 'r36', 11: 'r36', 12: 'r36', 14: 'r36'},
            47: {0: 'r11', 1: 'r11', 3: 'r11', 6: 'r11', 7: 'r11', 9: 'r11', 10: 'r11', 11: 'r11', 12: 'r11', 14: 'r11'},
            48: {3: 'r34', 7: 's50', 9: 'r34'},
            49: {3: 'r28', 7: 'r28', 9: 'r28'},
            50: {0: 's11', 1: 's12', 6: 's16', 10: 's8', 11: 's15', 12: 's14', 14: 's13'},
            51: {3: 'r29', 7: 'r29', 9: 'r29'}
        }
        self.__sparse_goto_table: dict = {
            0: {1: 10, 7: 5, 8: 7, 12: 4, 13: 1, 15: 2, 16: 9, 21: 6, 22: 3},
            3: {9: 48},
            4: {1: 10, 7: 47, 8: 7, 16: 9, 21: 6},
            6: {5: 36, 6: 30, 14: 31},
            14: {1: 10, 7: 5, 8: 7, 12: 4, 15: 28, 16: 9, 21: 6, 22: 3},
            16: {3: 18, 11: 19},
            18: {0: 21, 1: 20, 16: 23, 20: 22},
            21: {1: 20, 16: 23, 20: 25},
            26: {1: 27},
            33: {4: 37, 10: 39},
            42: {4: 44, 10: 39, 17: 45, 19: 43},
            48: {2: 49},
            50: {1: 10, 7: 5, 8: 7, 12: 4, 16: 9, 21: 6, 22: 51}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            15: ('*0',),
            9: ('*0', '1'),
            19: ('1', '1'),
            36: ('1', '*3'),
            32: ('0',),
            2: (),
            18: ('*0',),
            23: ('0', '2'),
            21: ('0',),
            1: ('1',),
            30: ('*1', '2'),
            37: ('0',),
            7: ('*0', '1'),
            6: (),
            39: ('*0',),
            24: ('0',),
            12: ('0',),
            25: ('0',),
            40: ('0', '*1'),
            20: ('0',),
            16: (),
            10: ('*0',),
            17: ('*0',),
            11: ('*0', '1'),
            34: ('0', '*1'),
            29: ('1',),
            31: (),
            28: ('*0', '*1'),
            13: ('0',)
        }
        self.__reduce_symbol_count: list = [1, 3, 0, 1, 1, 1, 0, 2, 1, 2, 1, 2, 1, 1, 1, 1, 0, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 1, 2, 2, 4, 0, 1, 1, 2, 1, 5, 1, 1, 1, 2]
        self.__reduce_non_terminal_index: list = [18, 8, 17, 10, 0, 14, 3, 0, 12, 10, 5, 12, 21, 13, 1, 4, 5, 22, 17, 14, 6, 8, 20, 20, 21, 21, 1, 16, 9, 2, 8, 9, 19, 16, 15, 14, 14, 11, 14, 3, 7]

    def parse(self, token_list: list) -> BosonGrammar:
        grammar = BosonGrammar()
        analysis_stack = [0]
        symbol_stack = []
        token_index = 0
        while token_index < len(token_list):
            token: RegularToken = token_list[token_index]
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
                elif statement_index in {0, 33, 3, 4, 5, 35, 38, 8, 14, 22, 26, 27}:
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
