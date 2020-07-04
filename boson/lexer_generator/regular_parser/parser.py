from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_4': 0,
            '!symbol_12': 1,
            'reference': 2,
            '$': 3,
            '!symbol_2': 4,
            '!symbol_11': 5,
            'normal_character': 6,
            '!symbol_9': 7,
            '!symbol_10': 8,
            '!symbol_1': 9,
            '!symbol_13': 10,
            '!symbol_5': 11,
            'escape_character': 12,
            '!symbol_14': 13,
            'single_number': 14,
            '!symbol_6': 15,
            '!symbol_7': 16,
            '!symbol_3': 17,
            '!symbol_8': 18
        }
        self.__sparse_action_table: dict = {
            0: {2: 's11', 4: 's8', 6: 's16', 12: 's13', 14: 's15', 15: 's12', 17: 's10'},
            1: {3: 'a'},
            2: {3: 'r32'},
            3: {3: 'r31', 9: 'r31', 16: 'r31'},
            4: {2: 's11', 3: 'r9', 4: 's8', 6: 's16', 9: 'r9', 12: 's13', 14: 's15', 15: 's12', 16: 'r9', 17: 's10'},
            5: {2: 'r39', 3: 'r39', 4: 'r39', 6: 'r39', 9: 'r39', 12: 'r39', 14: 'r39', 15: 'r39', 16: 'r39', 17: 'r39'},
            6: {1: 's32', 2: 'r2', 3: 'r2', 4: 'r2', 5: 's33', 6: 'r2', 7: 's35', 8: 's34', 9: 'r2', 12: 'r2', 14: 'r2', 15: 'r2', 16: 'r2', 17: 'r2'},
            7: {1: 'r14', 2: 'r14', 3: 'r14', 4: 'r14', 5: 'r14', 6: 'r14', 7: 'r14', 8: 'r14', 9: 'r14', 12: 'r14', 14: 'r14', 15: 'r14', 16: 'r14', 17: 'r14'},
            8: {1: 'r22', 2: 'r22', 3: 'r22', 4: 'r22', 5: 'r22', 6: 'r22', 7: 'r22', 8: 'r22', 9: 'r22', 12: 'r22', 14: 'r22', 15: 'r22', 16: 'r22', 17: 'r22'},
            9: {1: 'r25', 2: 'r25', 3: 'r25', 4: 'r25', 5: 'r25', 6: 'r25', 7: 'r25', 8: 'r25', 9: 'r25', 12: 'r25', 14: 'r25', 15: 'r25', 16: 'r25', 17: 'r25'},
            10: {0: 's21', 6: 'r40', 12: 'r40', 14: 'r40'},
            11: {1: 'r18', 2: 'r18', 3: 'r18', 4: 'r18', 5: 'r18', 6: 'r18', 7: 'r18', 8: 'r18', 9: 'r18', 12: 'r18', 14: 'r18', 15: 'r18', 16: 'r18', 17: 'r18'},
            12: {2: 's11', 4: 's8', 6: 's16', 12: 's13', 14: 's15', 15: 's12', 17: 's10'},
            13: {1: 'r11', 2: 'r11', 3: 'r11', 4: 'r11', 5: 'r11', 6: 'r11', 7: 'r11', 8: 'r11', 9: 'r11', 11: 'r11', 12: 'r11', 14: 'r11', 15: 'r11', 16: 'r11', 17: 'r11'},
            14: {1: 'r38', 2: 'r38', 3: 'r38', 4: 'r38', 5: 'r38', 6: 'r38', 7: 'r38', 8: 'r38', 9: 'r38', 12: 'r38', 14: 'r38', 15: 'r38', 16: 'r38', 17: 'r38'},
            15: {1: 'r17', 2: 'r17', 3: 'r17', 4: 'r17', 5: 'r17', 6: 'r17', 7: 'r17', 8: 'r17', 9: 'r17', 11: 'r17', 12: 'r17', 14: 'r17', 15: 'r17', 16: 'r17', 17: 'r17', 18: 'r17'},
            16: {1: 'r20', 2: 'r20', 3: 'r20', 4: 'r20', 5: 'r20', 6: 'r20', 7: 'r20', 8: 'r20', 9: 'r20', 11: 'r20', 12: 'r20', 14: 'r20', 15: 'r20', 16: 'r20', 17: 'r20', 18: 'r20'},
            17: {16: 's18'},
            18: {1: 'r33', 2: 'r33', 3: 'r33', 4: 'r33', 5: 'r33', 6: 'r33', 7: 'r33', 8: 'r33', 9: 'r33', 12: 'r33', 14: 'r33', 15: 'r33', 16: 'r33', 17: 'r33'},
            19: {6: 's16', 12: 's13', 14: 's15'},
            20: {6: 'r8', 12: 'r8', 14: 'r8'},
            21: {6: 'r24', 12: 'r24', 14: 'r24'},
            22: {6: 's16', 11: 's28', 12: 's13', 14: 's15'},
            23: {6: 'r35', 11: 'r35', 12: 'r35', 14: 'r35'},
            24: {6: 'r38', 11: 'r38', 12: 'r38', 14: 'r38', 18: 's26'},
            25: {6: 'r15', 11: 'r15', 12: 'r15', 14: 'r15'},
            26: {6: 's16', 14: 's15'},
            27: {6: 'r7', 11: 'r7', 12: 'r7', 14: 'r7'},
            28: {1: 'r12', 2: 'r12', 3: 'r12', 4: 'r12', 5: 'r12', 6: 'r12', 7: 'r12', 8: 'r12', 9: 'r12', 12: 'r12', 14: 'r12', 15: 'r12', 16: 'r12', 17: 'r12'},
            29: {6: 'r28', 11: 'r28', 12: 'r28', 14: 'r28'},
            30: {2: 'r4', 3: 'r4', 4: 'r4', 6: 'r4', 9: 'r4', 12: 'r4', 14: 'r4', 15: 'r4', 16: 'r4', 17: 'r4'},
            31: {2: 'r29', 3: 'r29', 4: 'r29', 6: 'r29', 9: 'r29', 12: 'r29', 14: 'r29', 15: 'r29', 16: 'r29', 17: 'r29'},
            32: {14: 's39'},
            33: {2: 'r6', 3: 'r6', 4: 'r6', 6: 'r6', 9: 'r6', 12: 'r6', 14: 'r6', 15: 'r6', 16: 'r6', 17: 'r6'},
            34: {2: 'r10', 3: 'r10', 4: 'r10', 6: 'r10', 9: 'r10', 12: 'r10', 14: 'r10', 15: 'r10', 16: 'r10', 17: 'r10'},
            35: {2: 'r23', 3: 'r23', 4: 'r23', 6: 'r23', 9: 'r23', 12: 'r23', 14: 'r23', 15: 'r23', 16: 'r23', 17: 'r23'},
            36: {2: 'r37', 3: 'r37', 4: 'r37', 6: 'r37', 9: 'r37', 12: 'r37', 14: 'r37', 15: 'r37', 16: 'r37', 17: 'r37'},
            37: {10: 's42', 13: 's41'},
            38: {10: 'r26', 13: 'r26', 14: 's40'},
            39: {10: 'r34', 13: 'r34', 14: 'r34'},
            40: {10: 'r30', 13: 'r30', 14: 'r30'},
            41: {2: 'r1', 3: 'r1', 4: 'r1', 6: 'r1', 9: 'r1', 12: 'r1', 14: 'r1', 15: 'r1', 16: 'r1', 17: 'r1'},
            42: {13: 'r19', 14: 's39'},
            43: {13: 's46'},
            44: {13: 'r21'},
            45: {13: 'r13'},
            46: {2: 'r3', 3: 'r3', 4: 'r3', 6: 'r3', 9: 'r3', 12: 'r3', 14: 'r3', 15: 'r3', 16: 'r3', 17: 'r3'},
            47: {2: 'r16', 3: 'r16', 4: 'r16', 6: 'r16', 9: 'r16', 12: 'r16', 14: 'r16', 15: 'r16', 16: 'r16', 17: 'r16'},
            48: {3: 'r27', 9: 's50', 16: 'r27'},
            49: {3: 'r5', 9: 'r5', 16: 'r5'},
            50: {2: 's11', 4: 's8', 6: 's16', 12: 's13', 14: 's15', 15: 's12', 17: 's10'},
            51: {3: 'r36', 9: 'r36', 16: 'r36'}
        }
        self.__sparse_goto_table: dict = {
            0: {1: 9, 2: 5, 6: 1, 9: 7, 10: 4, 11: 6, 12: 2, 15: 3, 22: 14},
            3: {14: 48},
            4: {1: 9, 2: 47, 9: 7, 11: 6, 22: 14},
            6: {0: 36, 5: 30, 13: 31},
            10: {17: 19, 19: 20},
            12: {1: 9, 2: 5, 9: 7, 10: 4, 11: 6, 12: 17, 15: 3, 22: 14},
            19: {9: 25, 16: 22, 20: 23, 22: 24},
            22: {9: 25, 20: 29, 22: 24},
            26: {22: 27},
            32: {4: 38, 7: 37},
            42: {4: 38, 7: 45, 18: 43, 21: 44},
            48: {3: 49},
            50: {1: 9, 2: 5, 9: 7, 10: 4, 11: 6, 15: 51, 22: 14}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            26: ('*0',),
            30: ('*0', '1'),
            1: ('1', '1'),
            3: ('1', '*3'),
            13: ('0',),
            19: (),
            21: ('*0',),
            7: ('0', '2'),
            18: ('0',),
            33: ('1',),
            12: ('*1', '2'),
            24: ('0',),
            28: ('*0', '1'),
            40: (),
            8: ('*0',),
            22: ('0',),
            25: ('0',),
            14: ('0',),
            37: ('0', '*1'),
            29: ('0',),
            2: (),
            4: ('*0',),
            9: ('*0',),
            16: ('*0', '1'),
            27: ('0', '*1'),
            36: ('1',),
            31: (),
            5: ('*0', '*1'),
            32: ('0',)
        }
        self.__reduce_symbol_count: list = [1, 3, 0, 5, 1, 2, 1, 3, 1, 1, 1, 1, 4, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 1, 3, 1, 1, 2, 2, 1, 1, 0]
        self.__reduce_non_terminal_index: list = [8, 13, 0, 13, 0, 14, 13, 20, 17, 15, 13, 9, 1, 21, 11, 20, 10, 22, 1, 18, 22, 18, 11, 13, 19, 11, 7, 12, 16, 5, 4, 14, 6, 1, 4, 16, 3, 2, 9, 10, 17]

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
                elif statement_index in {0, 34, 35, 6, 38, 39, 10, 11, 15, 17, 20, 23}:
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
