from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_3': 0,
            '!symbol_14': 1,
            '!symbol_8': 2,
            '!symbol_1': 3,
            '!symbol_13': 4,
            '!symbol_9': 5,
            '!symbol_7': 6,
            '!symbol_4': 7,
            '!symbol_6': 8,
            '!symbol_10': 9,
            '!symbol_5': 10,
            'single_number': 11,
            'escape_character': 12,
            '!symbol_11': 13,
            '$': 14,
            'reference': 15,
            '!symbol_2': 16,
            'normal_character': 17,
            '!symbol_12': 18
        }
        self.__sparse_action_table: dict = {
            0: {0: 's11', 8: 's12', 11: 's15', 12: 's14', 15: 's10', 16: 's7', 17: 's16'},
            1: {14: 'a'},
            2: {14: 'r32'},
            3: {3: 'r39', 6: 'r39', 14: 'r39'},
            4: {0: 's11', 3: 'r36', 6: 'r36', 8: 's12', 11: 's15', 12: 's14', 14: 'r36', 15: 's10', 16: 's7', 17: 's16'},
            5: {0: 'r35', 3: 'r35', 6: 'r35', 8: 'r35', 11: 'r35', 12: 'r35', 14: 'r35', 15: 'r35', 16: 'r35', 17: 'r35'},
            6: {0: 'r14', 3: 'r14', 5: 's35', 6: 'r14', 8: 'r14', 9: 's34', 11: 'r14', 12: 'r14', 13: 's32', 14: 'r14', 15: 'r14', 16: 'r14', 17: 'r14', 18: 's33'},
            7: {0: 'r5', 3: 'r5', 5: 'r5', 6: 'r5', 8: 'r5', 9: 'r5', 11: 'r5', 12: 'r5', 13: 'r5', 14: 'r5', 15: 'r5', 16: 'r5', 17: 'r5', 18: 'r5'},
            8: {0: 'r21', 3: 'r21', 5: 'r21', 6: 'r21', 8: 'r21', 9: 'r21', 11: 'r21', 12: 'r21', 13: 'r21', 14: 'r21', 15: 'r21', 16: 'r21', 17: 'r21', 18: 'r21'},
            9: {0: 'r37', 3: 'r37', 5: 'r37', 6: 'r37', 8: 'r37', 9: 'r37', 11: 'r37', 12: 'r37', 13: 'r37', 14: 'r37', 15: 'r37', 16: 'r37', 17: 'r37', 18: 'r37'},
            10: {0: 'r2', 3: 'r2', 5: 'r2', 6: 'r2', 8: 'r2', 9: 'r2', 11: 'r2', 12: 'r2', 13: 'r2', 14: 'r2', 15: 'r2', 16: 'r2', 17: 'r2', 18: 'r2'},
            11: {7: 's20', 11: 'r7', 12: 'r7', 17: 'r7'},
            12: {0: 's11', 8: 's12', 11: 's15', 12: 's14', 15: 's10', 16: 's7', 17: 's16'},
            13: {0: 'r8', 3: 'r8', 5: 'r8', 6: 'r8', 8: 'r8', 9: 'r8', 11: 'r8', 12: 'r8', 13: 'r8', 14: 'r8', 15: 'r8', 16: 'r8', 17: 'r8', 18: 'r8'},
            14: {0: 'r16', 3: 'r16', 5: 'r16', 6: 'r16', 8: 'r16', 9: 'r16', 10: 'r16', 11: 'r16', 12: 'r16', 13: 'r16', 14: 'r16', 15: 'r16', 16: 'r16', 17: 'r16', 18: 'r16'},
            15: {0: 'r20', 2: 'r20', 3: 'r20', 5: 'r20', 6: 'r20', 8: 'r20', 9: 'r20', 10: 'r20', 11: 'r20', 12: 'r20', 13: 'r20', 14: 'r20', 15: 'r20', 16: 'r20', 17: 'r20', 18: 'r20'},
            16: {0: 'r25', 2: 'r25', 3: 'r25', 5: 'r25', 6: 'r25', 8: 'r25', 9: 'r25', 10: 'r25', 11: 'r25', 12: 'r25', 13: 'r25', 14: 'r25', 15: 'r25', 16: 'r25', 17: 'r25', 18: 'r25'},
            17: {6: 's18'},
            18: {0: 'r29', 3: 'r29', 5: 'r29', 6: 'r29', 8: 'r29', 9: 'r29', 11: 'r29', 12: 'r29', 13: 'r29', 14: 'r29', 15: 'r29', 16: 'r29', 17: 'r29', 18: 'r29'},
            19: {11: 'r27', 12: 'r27', 17: 'r27'},
            20: {11: 'r9', 12: 'r9', 17: 'r9'},
            21: {11: 's15', 12: 's14', 17: 's16'},
            22: {10: 's28', 11: 's15', 12: 's14', 17: 's16'},
            23: {10: 'r33', 11: 'r33', 12: 'r33', 17: 'r33'},
            24: {2: 's26', 10: 'r8', 11: 'r8', 12: 'r8', 17: 'r8'},
            25: {10: 'r34', 11: 'r34', 12: 'r34', 17: 'r34'},
            26: {11: 's15', 17: 's16'},
            27: {10: 'r12', 11: 'r12', 12: 'r12', 17: 'r12'},
            28: {0: 'r24', 3: 'r24', 5: 'r24', 6: 'r24', 8: 'r24', 9: 'r24', 11: 'r24', 12: 'r24', 13: 'r24', 14: 'r24', 15: 'r24', 16: 'r24', 17: 'r24', 18: 'r24'},
            29: {10: 'r23', 11: 'r23', 12: 'r23', 17: 'r23'},
            30: {0: 'r10', 3: 'r10', 6: 'r10', 8: 'r10', 11: 'r10', 12: 'r10', 14: 'r10', 15: 'r10', 16: 'r10', 17: 'r10'},
            31: {0: 'r38', 3: 'r38', 6: 'r38', 8: 'r38', 11: 'r38', 12: 'r38', 14: 'r38', 15: 'r38', 16: 'r38', 17: 'r38'},
            32: {0: 'r3', 3: 'r3', 6: 'r3', 8: 'r3', 11: 'r3', 12: 'r3', 14: 'r3', 15: 'r3', 16: 'r3', 17: 'r3'},
            33: {4: 'r1', 11: 's38'},
            34: {0: 'r18', 3: 'r18', 6: 'r18', 8: 'r18', 11: 'r18', 12: 'r18', 14: 'r18', 15: 'r18', 16: 'r18', 17: 'r18'},
            35: {0: 'r31', 3: 'r31', 6: 'r31', 8: 'r31', 11: 'r31', 12: 'r31', 14: 'r31', 15: 'r31', 16: 'r31', 17: 'r31'},
            36: {0: 'r28', 3: 'r28', 6: 'r28', 8: 'r28', 11: 'r28', 12: 'r28', 14: 'r28', 15: 'r28', 16: 'r28', 17: 'r28'},
            37: {1: 'r19', 4: 'r19', 11: 's45'},
            38: {1: 'r30', 4: 'r30', 11: 'r30'},
            39: {4: 's42'},
            40: {1: 'r11', 4: 'r11'},
            41: {1: 'r4', 4: 'r4'},
            42: {1: 'r1', 11: 's38'},
            43: {1: 's44'},
            44: {0: 'r17', 3: 'r17', 6: 'r17', 8: 'r17', 11: 'r17', 12: 'r17', 14: 'r17', 15: 'r17', 16: 'r17', 17: 'r17'},
            45: {1: 'r22', 4: 'r22', 11: 'r22'},
            46: {0: 'r15', 3: 'r15', 6: 'r15', 8: 'r15', 11: 'r15', 12: 'r15', 14: 'r15', 15: 'r15', 16: 'r15', 17: 'r15'},
            47: {3: 's48', 6: 'r13', 14: 'r13'},
            48: {0: 's11', 8: 's12', 11: 's15', 12: 's14', 15: 's10', 16: 's7', 17: 's16'},
            49: {3: 'r6', 6: 'r6', 14: 'r6'},
            50: {3: 'r26', 6: 'r26', 14: 'r26'}
        }
        self.__sparse_goto_table: dict = {
            0: {1: 4, 2: 2, 8: 1, 11: 13, 13: 8, 14: 3, 15: 6, 17: 9, 18: 5},
            3: {9: 47},
            4: {11: 13, 13: 8, 15: 6, 17: 9, 18: 46},
            6: {5: 36, 6: 31, 19: 30},
            11: {3: 19, 4: 21},
            12: {1: 4, 2: 17, 11: 13, 13: 8, 14: 3, 15: 6, 17: 9, 18: 5},
            21: {10: 23, 11: 24, 12: 22, 13: 25},
            22: {10: 29, 11: 24, 13: 25},
            26: {11: 27},
            33: {0: 41, 16: 37, 21: 39, 22: 40},
            42: {0: 41, 16: 37, 21: 43, 22: 40},
            47: {20: 49},
            48: {1: 4, 11: 13, 13: 8, 14: 50, 15: 6, 17: 9, 18: 5}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            19: ('*0',),
            22: ('*0', '1'),
            17: ('*1', '*3'),
            4: ('0',),
            1: (),
            11: ('*0',),
            12: ('0', '2'),
            2: ('0',),
            29: ('1',),
            24: ('*1', '2'),
            9: ('0',),
            23: ('*0', '1'),
            7: (),
            27: ('*0',),
            5: ('0',),
            37: ('0',),
            21: ('0',),
            28: ('0', '*1'),
            38: ('0',),
            14: (),
            10: ('*0',),
            36: ('*0',),
            15: ('*0', '1'),
            13: ('0', '*1'),
            26: ('1',),
            39: (),
            6: ('*0', '*1'),
            32: ('0',)
        }
        self.__reduce_symbol_count: list = [1, 0, 1, 1, 1, 1, 2, 0, 1, 1, 1, 1, 3, 2, 0, 2, 1, 5, 1, 1, 1, 1, 2, 2, 4, 1, 2, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        self.__reduce_non_terminal_index: list = [7, 21, 17, 6, 22, 15, 9, 4, 13, 3, 5, 21, 10, 2, 5, 1, 13, 6, 6, 0, 11, 15, 16, 12, 17, 11, 20, 4, 18, 17, 16, 6, 8, 12, 10, 1, 14, 15, 19, 9]

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
                elif statement_index in {0, 33, 34, 3, 35, 8, 16, 18, 20, 25, 30, 31}:
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
