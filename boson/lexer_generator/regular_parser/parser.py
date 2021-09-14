from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_9': 0,
            '!symbol_5': 1,
            '!symbol_3': 2,
            'reference': 3,
            'unicode_character': 4,
            '!symbol_11': 5,
            'normal_character': 6,
            '!symbol_10': 7,
            '!symbol_4': 8,
            'single_number': 9,
            'escape_character': 10,
            '!symbol_2': 11,
            '!symbol_13': 12,
            '!symbol_12': 13,
            '!symbol_8': 14,
            '!symbol_1': 15,
            '!symbol_6': 16,
            '!symbol_7': 17,
            '$': 18,
            '!symbol_14': 19
        }
        self.__sparse_action_table: dict = {
            0: {2: 's11', 3: 's10', 4: 's15', 6: 's13', 9: 's14', 10: 's17', 11: 's9', 16: 's12'},
            1: {18: 'a'},
            2: {18: 'r6'},
            3: {15: 'r27', 17: 'r27', 18: 'r27'},
            4: {2: 's11', 3: 's10', 4: 's15', 6: 's13', 9: 's14', 10: 's17', 11: 's9', 15: 'r31', 16: 's12', 17: 'r31', 18: 'r31'},
            5: {2: 'r39', 3: 'r39', 4: 'r39', 6: 'r39', 9: 'r39', 10: 'r39', 11: 'r39', 15: 'r39', 16: 'r39', 17: 'r39', 18: 'r39'},
            6: {0: 's37', 2: 'r9', 3: 'r9', 4: 'r9', 5: 's33', 6: 'r9', 7: 's35', 9: 'r9', 10: 'r9', 11: 'r9', 13: 's34', 15: 'r9', 16: 'r9', 17: 'r9', 18: 'r9'},
            7: {0: 'r14', 2: 'r14', 3: 'r14', 4: 'r14', 5: 'r14', 6: 'r14', 7: 'r14', 9: 'r14', 10: 'r14', 11: 'r14', 13: 'r14', 15: 'r14', 16: 'r14', 17: 'r14', 18: 'r14'},
            8: {0: 'r21', 2: 'r21', 3: 'r21', 4: 'r21', 5: 'r21', 6: 'r21', 7: 'r21', 9: 'r21', 10: 'r21', 11: 'r21', 13: 'r21', 15: 'r21', 16: 'r21', 17: 'r21', 18: 'r21'},
            9: {0: 'r22', 2: 'r22', 3: 'r22', 4: 'r22', 5: 'r22', 6: 'r22', 7: 'r22', 9: 'r22', 10: 'r22', 11: 'r22', 13: 'r22', 15: 'r22', 16: 'r22', 17: 'r22', 18: 'r22'},
            10: {0: 'r23', 2: 'r23', 3: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 9: 'r23', 10: 'r23', 11: 'r23', 13: 'r23', 15: 'r23', 16: 'r23', 17: 'r23', 18: 'r23'},
            11: {4: 'r19', 6: 'r19', 8: 's22', 9: 'r19', 10: 'r19'},
            12: {2: 's11', 3: 's10', 4: 's15', 6: 's13', 9: 's14', 10: 's17', 11: 's9', 16: 's12'},
            13: {0: 'r1', 1: 'r1', 2: 'r1', 3: 'r1', 4: 'r1', 5: 'r1', 6: 'r1', 7: 'r1', 9: 'r1', 10: 'r1', 11: 'r1', 13: 'r1', 14: 'r1', 15: 'r1', 16: 'r1', 17: 'r1', 18: 'r1'},
            14: {0: 'r26', 1: 'r26', 2: 'r26', 3: 'r26', 4: 'r26', 5: 'r26', 6: 'r26', 7: 'r26', 9: 'r26', 10: 'r26', 11: 'r26', 13: 'r26', 14: 'r26', 15: 'r26', 16: 'r26', 17: 'r26', 18: 'r26'},
            15: {0: 'r35', 1: 'r35', 2: 'r35', 3: 'r35', 4: 'r35', 5: 'r35', 6: 'r35', 7: 'r35', 9: 'r35', 10: 'r35', 11: 'r35', 13: 'r35', 14: 'r35', 15: 'r35', 16: 'r35', 17: 'r35', 18: 'r35'},
            16: {0: 'r7', 2: 'r7', 3: 'r7', 4: 'r7', 5: 'r7', 6: 'r7', 7: 'r7', 9: 'r7', 10: 'r7', 11: 'r7', 13: 'r7', 15: 'r7', 16: 'r7', 17: 'r7', 18: 'r7'},
            17: {0: 'r41', 1: 'r41', 2: 'r41', 3: 'r41', 4: 'r41', 5: 'r41', 6: 'r41', 7: 'r41', 9: 'r41', 10: 'r41', 11: 'r41', 13: 'r41', 15: 'r41', 16: 'r41', 17: 'r41', 18: 'r41'},
            18: {17: 's19'},
            19: {0: 'r32', 2: 'r32', 3: 'r32', 4: 'r32', 5: 'r32', 6: 'r32', 7: 'r32', 9: 'r32', 10: 'r32', 11: 'r32', 13: 'r32', 15: 'r32', 16: 'r32', 17: 'r32', 18: 'r32'},
            20: {4: 's15', 6: 's13', 9: 's14', 10: 's17'},
            21: {4: 'r5', 6: 'r5', 9: 'r5', 10: 'r5'},
            22: {4: 'r12', 6: 'r12', 9: 'r12', 10: 'r12'},
            23: {1: 's29', 4: 's15', 6: 's13', 9: 's14', 10: 's17'},
            24: {1: 'r2', 4: 'r2', 6: 'r2', 9: 'r2', 10: 'r2'},
            25: {1: 'r4', 4: 'r4', 6: 'r4', 9: 'r4', 10: 'r4'},
            26: {1: 'r7', 4: 'r7', 6: 'r7', 9: 'r7', 10: 'r7', 14: 's27'},
            27: {4: 's15', 6: 's13', 9: 's14'},
            28: {1: 'r10', 4: 'r10', 6: 'r10', 9: 'r10', 10: 'r10'},
            29: {0: 'r28', 2: 'r28', 3: 'r28', 4: 'r28', 5: 'r28', 6: 'r28', 7: 'r28', 9: 'r28', 10: 'r28', 11: 'r28', 13: 'r28', 15: 'r28', 16: 'r28', 17: 'r28', 18: 'r28'},
            30: {1: 'r37', 4: 'r37', 6: 'r37', 9: 'r37', 10: 'r37'},
            31: {2: 'r3', 3: 'r3', 4: 'r3', 6: 'r3', 9: 'r3', 10: 'r3', 11: 'r3', 15: 'r3', 16: 'r3', 17: 'r3', 18: 'r3'},
            32: {2: 'r13', 3: 'r13', 4: 'r13', 6: 'r13', 9: 'r13', 10: 'r13', 11: 'r13', 15: 'r13', 16: 'r13', 17: 'r13', 18: 'r13'},
            33: {2: 'r8', 3: 'r8', 4: 'r8', 6: 'r8', 9: 'r8', 10: 'r8', 11: 'r8', 15: 'r8', 16: 'r8', 17: 'r8', 18: 'r8'},
            34: {9: 's40'},
            35: {2: 'r17', 3: 'r17', 4: 'r17', 6: 'r17', 9: 'r17', 10: 'r17', 11: 'r17', 15: 'r17', 16: 'r17', 17: 'r17', 18: 'r17'},
            36: {2: 'r11', 3: 'r11', 4: 'r11', 6: 'r11', 9: 'r11', 10: 'r11', 11: 'r11', 15: 'r11', 16: 'r11', 17: 'r11', 18: 'r11'},
            37: {2: 'r20', 3: 'r20', 4: 'r20', 6: 'r20', 9: 'r20', 10: 'r20', 11: 'r20', 15: 'r20', 16: 'r20', 17: 'r20', 18: 'r20'},
            38: {12: 's42', 19: 's43'},
            39: {9: 's41', 12: 'r40', 19: 'r40'},
            40: {9: 'r33', 12: 'r33', 19: 'r33'},
            41: {9: 'r38', 12: 'r38', 19: 'r38'},
            42: {9: 's40', 19: 'r34'},
            43: {2: 'r29', 3: 'r29', 4: 'r29', 6: 'r29', 9: 'r29', 10: 'r29', 11: 'r29', 15: 'r29', 16: 'r29', 17: 'r29', 18: 'r29'},
            44: {19: 's47'},
            45: {19: 'r36'},
            46: {19: 'r24'},
            47: {2: 'r15', 3: 'r15', 4: 'r15', 6: 'r15', 9: 'r15', 10: 'r15', 11: 'r15', 15: 'r15', 16: 'r15', 17: 'r15', 18: 'r15'},
            48: {2: 'r25', 3: 'r25', 4: 'r25', 6: 'r25', 9: 'r25', 10: 'r25', 11: 'r25', 15: 'r25', 16: 'r25', 17: 'r25', 18: 'r25'},
            49: {15: 's50', 17: 'r18', 18: 'r18'},
            50: {2: 's11', 3: 's10', 4: 's15', 6: 's13', 9: 's14', 10: 's17', 11: 's9', 16: 's12'},
            51: {15: 'r16', 17: 'r16', 18: 'r16'},
            52: {15: 'r30', 17: 'r30', 18: 'r30'}
        }
        self.__sparse_goto_table: dict = {
            0: {4: 6, 5: 3, 7: 7, 9: 16, 14: 1, 15: 4, 18: 2, 20: 8, 22: 5},
            3: {3: 49},
            4: {4: 6, 7: 7, 9: 16, 20: 8, 22: 48},
            6: {8: 36, 19: 31, 21: 32},
            11: {12: 20, 17: 21},
            12: {4: 6, 5: 3, 7: 7, 9: 16, 15: 4, 18: 18, 20: 8, 22: 5},
            20: {1: 24, 7: 25, 9: 26, 10: 23},
            23: {1: 30, 7: 25, 9: 26},
            27: {9: 28},
            34: {2: 39, 6: 38},
            42: {0: 44, 2: 39, 6: 46, 13: 45},
            49: {11: 51},
            50: {4: 6, 5: 52, 7: 7, 9: 16, 15: 4, 20: 8, 22: 5}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            40: ('*0',),
            38: ('*0', '1'),
            29: ('1', '1'),
            15: ('1', '*3'),
            24: ('0',),
            34: (),
            36: ('*0',),
            10: ('0', '2'),
            23: ('0',),
            32: ('1',),
            28: ('*1', '2'),
            12: ('0',),
            37: ('*0', '1'),
            19: (),
            5: ('*0',),
            35: ('0',),
            22: ('0',),
            21: ('0',),
            14: ('0',),
            11: ('0', '*1'),
            13: ('0',),
            9: (),
            3: ('*0',),
            31: ('*0',),
            25: ('*0', '1'),
            18: ('0', '*1'),
            30: ('1',),
            27: (),
            16: ('*0', '*1'),
            6: ('0',)
        }
        self.__reduce_symbol_count: list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, 2, 1, 1, 1, 5, 2, 1, 2, 0, 1, 1, 1, 1, 1, 2, 1, 0, 4, 3, 2, 1, 3, 1, 0, 1, 1, 2, 2, 1, 1, 1]
        self.__reduce_non_terminal_index: list = [16, 9, 10, 8, 1, 12, 14, 7, 21, 8, 1, 22, 17, 19, 4, 21, 3, 21, 18, 12, 21, 4, 4, 20, 13, 15, 9, 3, 20, 21, 11, 5, 20, 2, 0, 9, 0, 10, 2, 15, 6, 7]

    def parse(self, token_list: list) -> BosonGrammar:
        grammar = BosonGrammar()
        analysis_stack = [0]
        symbol_stack = []
        token_index = 0
        while token_index < len(token_list):
            token: RegularToken = token_list[token_index]
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
                elif statement_index in {0, 1, 2, 33, 4, 7, 8, 39, 41, 17, 20, 26}:
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
