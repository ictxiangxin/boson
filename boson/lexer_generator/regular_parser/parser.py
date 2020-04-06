from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_3': 0,
            '!symbol_4': 1,
            '!symbol_6': 2,
            '!symbol_10': 3,
            'single_number': 4,
            'escape_character': 5,
            '!symbol_2': 6,
            '!symbol_5': 7,
            '!symbol_9': 8,
            '!symbol_11': 9,
            '$': 10,
            '!symbol_12': 11,
            '!symbol_14': 12,
            'normal_character': 13,
            '!symbol_8': 14,
            '!symbol_1': 15,
            '!symbol_7': 16,
            'reference': 17,
            '!symbol_13': 18
        }
        self.__sparse_action_table: dict = {
            0: {0: 's10', 2: 's11', 4: 's13', 5: 's15', 6: 's7', 13: 's14', 17: 's12'},
            1: {10: 'a'},
            2: {10: 'r34'},
            3: {10: 'r35', 15: 'r35', 16: 'r35'},
            4: {0: 's10', 2: 's11', 4: 's13', 5: 's15', 6: 's7', 10: 'r5', 13: 's14', 15: 'r5', 16: 'r5', 17: 's12'},
            5: {0: 'r13', 2: 'r13', 4: 'r13', 5: 'r13', 6: 'r13', 10: 'r13', 13: 'r13', 15: 'r13', 16: 'r13', 17: 'r13'},
            6: {0: 'r2', 2: 'r2', 3: 's33', 4: 'r2', 5: 'r2', 6: 'r2', 8: 's34', 9: 's35', 10: 'r2', 11: 's32', 13: 'r2', 15: 'r2', 16: 'r2', 17: 'r2'},
            7: {0: 'r7', 2: 'r7', 3: 'r7', 4: 'r7', 5: 'r7', 6: 'r7', 8: 'r7', 9: 'r7', 10: 'r7', 11: 'r7', 13: 'r7', 15: 'r7', 16: 'r7', 17: 'r7'},
            8: {0: 'r15', 2: 'r15', 3: 'r15', 4: 'r15', 5: 'r15', 6: 'r15', 8: 'r15', 9: 'r15', 10: 'r15', 11: 'r15', 13: 'r15', 15: 'r15', 16: 'r15', 17: 'r15'},
            9: {0: 'r26', 2: 'r26', 3: 'r26', 4: 'r26', 5: 'r26', 6: 'r26', 8: 'r26', 9: 'r26', 10: 'r26', 11: 'r26', 13: 'r26', 15: 'r26', 16: 'r26', 17: 'r26'},
            10: {1: 's21', 4: 'r40', 5: 'r40', 13: 'r40'},
            11: {0: 's10', 2: 's11', 4: 's13', 5: 's15', 6: 's7', 13: 's14', 17: 's12'},
            12: {0: 'r39', 2: 'r39', 3: 'r39', 4: 'r39', 5: 'r39', 6: 'r39', 8: 'r39', 9: 'r39', 10: 'r39', 11: 'r39', 13: 'r39', 15: 'r39', 16: 'r39', 17: 'r39'},
            13: {0: 'r3', 2: 'r3', 3: 'r3', 4: 'r3', 5: 'r3', 6: 'r3', 7: 'r3', 8: 'r3', 9: 'r3', 10: 'r3', 11: 'r3', 13: 'r3', 14: 'r3', 15: 'r3', 16: 'r3', 17: 'r3'},
            14: {0: 'r16', 2: 'r16', 3: 'r16', 4: 'r16', 5: 'r16', 6: 'r16', 7: 'r16', 8: 'r16', 9: 'r16', 10: 'r16', 11: 'r16', 13: 'r16', 14: 'r16', 15: 'r16', 16: 'r16', 17: 'r16'},
            15: {0: 'r19', 2: 'r19', 3: 'r19', 4: 'r19', 5: 'r19', 6: 'r19', 7: 'r19', 8: 'r19', 9: 'r19', 10: 'r19', 11: 'r19', 13: 'r19', 15: 'r19', 16: 'r19', 17: 'r19'},
            16: {0: 'r27', 2: 'r27', 3: 'r27', 4: 'r27', 5: 'r27', 6: 'r27', 8: 'r27', 9: 'r27', 10: 'r27', 11: 'r27', 13: 'r27', 15: 'r27', 16: 'r27', 17: 'r27'},
            17: {16: 's18'},
            18: {0: 'r25', 2: 'r25', 3: 'r25', 4: 'r25', 5: 'r25', 6: 'r25', 8: 'r25', 9: 'r25', 10: 'r25', 11: 'r25', 13: 'r25', 15: 'r25', 16: 'r25', 17: 'r25'},
            19: {4: 's13', 5: 's15', 13: 's14'},
            20: {4: 'r37', 5: 'r37', 13: 'r37'},
            21: {4: 'r6', 5: 'r6', 13: 'r6'},
            22: {4: 's13', 5: 's15', 7: 's29', 13: 's14'},
            23: {4: 'r10', 5: 'r10', 7: 'r10', 13: 'r10'},
            24: {4: 'r20', 5: 'r20', 7: 'r20', 13: 'r20'},
            25: {4: 'r27', 5: 'r27', 7: 'r27', 13: 'r27', 14: 's26'},
            26: {4: 's13', 13: 's14'},
            27: {4: 'r29', 5: 'r29', 7: 'r29', 13: 'r29'},
            28: {4: 'r8', 5: 'r8', 7: 'r8', 13: 'r8'},
            29: {0: 'r24', 2: 'r24', 3: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 8: 'r24', 9: 'r24', 10: 'r24', 11: 'r24', 13: 'r24', 15: 'r24', 16: 'r24', 17: 'r24'},
            30: {0: 'r31', 2: 'r31', 4: 'r31', 5: 'r31', 6: 'r31', 10: 'r31', 13: 'r31', 15: 'r31', 16: 'r31', 17: 'r31'},
            31: {0: 'r14', 2: 'r14', 4: 'r14', 5: 'r14', 6: 'r14', 10: 'r14', 13: 'r14', 15: 'r14', 16: 'r14', 17: 'r14'},
            32: {4: 's39'},
            33: {0: 'r11', 2: 'r11', 4: 'r11', 5: 'r11', 6: 'r11', 10: 'r11', 13: 'r11', 15: 'r11', 16: 'r11', 17: 'r11'},
            34: {0: 'r17', 2: 'r17', 4: 'r17', 5: 'r17', 6: 'r17', 10: 'r17', 13: 'r17', 15: 'r17', 16: 'r17', 17: 'r17'},
            35: {0: 'r36', 2: 'r36', 4: 'r36', 5: 'r36', 6: 'r36', 10: 'r36', 13: 'r36', 15: 'r36', 16: 'r36', 17: 'r36'},
            36: {0: 'r30', 2: 'r30', 4: 'r30', 5: 'r30', 6: 'r30', 10: 'r30', 13: 'r30', 15: 'r30', 16: 'r30', 17: 'r30'},
            37: {12: 's42', 18: 's41'},
            38: {4: 's40', 12: 'r4', 18: 'r4'},
            39: {4: 'r12', 12: 'r12', 18: 'r12'},
            40: {4: 'r18', 12: 'r18', 18: 'r18'},
            41: {4: 's39', 12: 'r33'},
            42: {0: 'r23', 2: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 10: 'r23', 13: 'r23', 15: 'r23', 16: 'r23', 17: 'r23'},
            43: {12: 's46'},
            44: {12: 'r21'},
            45: {12: 'r38'},
            46: {0: 'r1', 2: 'r1', 4: 'r1', 5: 'r1', 6: 'r1', 10: 'r1', 13: 'r1', 15: 'r1', 16: 'r1', 17: 'r1'},
            47: {0: 'r32', 2: 'r32', 4: 'r32', 5: 'r32', 6: 'r32', 10: 'r32', 13: 'r32', 15: 'r32', 16: 'r32', 17: 'r32'},
            48: {10: 'r9', 15: 's50', 16: 'r9'},
            49: {10: 'r22', 15: 'r22', 16: 'r22'},
            50: {0: 's10', 2: 's11', 4: 's13', 5: 's15', 6: 's7', 13: 's14', 17: 's12'},
            51: {10: 'r28', 15: 'r28', 16: 'r28'}
        }
        self.__sparse_goto_table: dict = {
            0: {0: 8, 3: 6, 4: 2, 5: 1, 9: 5, 13: 9, 14: 3, 15: 4, 16: 16},
            3: {22: 48},
            4: {0: 8, 3: 6, 9: 47, 13: 9, 16: 16},
            6: {8: 30, 10: 36, 21: 31},
            10: {1: 20, 6: 19},
            11: {0: 8, 3: 6, 4: 17, 9: 5, 13: 9, 14: 3, 15: 4, 16: 16},
            19: {0: 24, 16: 25, 17: 22, 20: 23},
            22: {0: 24, 16: 25, 20: 28},
            26: {16: 27},
            32: {2: 37, 7: 38},
            41: {2: 45, 7: 38, 12: 43, 19: 44},
            48: {18: 49},
            50: {0: 8, 3: 6, 9: 5, 13: 9, 14: 51, 15: 4, 16: 16}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            4: ('*0',),
            18: ('*0', '1'),
            23: ('1', '1'),
            1: ('1', '*3'),
            38: ('0',),
            33: (),
            21: ('*0',),
            29: ('0', '2'),
            39: ('0',),
            25: ('1',),
            24: ('*1', '2'),
            6: ('0',),
            8: ('*0', '1'),
            40: (),
            37: ('*0',),
            7: ('0',),
            26: ('0',),
            15: ('0',),
            30: ('0', '*1'),
            14: ('0',),
            2: (),
            31: ('*0',),
            5: ('*0',),
            32: ('*0', '1'),
            9: ('0', '*1'),
            28: ('1',),
            35: (),
            22: ('*0', '*1'),
            34: ('0',)
        }
        self.__reduce_symbol_count: list = [1, 5, 0, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 3, 4, 3, 1, 1, 2, 3, 2, 1, 2, 0, 1, 0, 1, 1, 1, 1, 0]
        self.__reduce_non_terminal_index: list = [11, 21, 10, 16, 2, 14, 1, 3, 17, 4, 17, 21, 7, 15, 8, 3, 16, 21, 7, 0, 20, 12, 22, 21, 13, 13, 3, 0, 18, 20, 9, 10, 15, 12, 5, 22, 21, 6, 19, 13, 6]

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
                elif statement_index in {0, 3, 36, 10, 11, 12, 13, 16, 17, 19, 20, 27}:
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
