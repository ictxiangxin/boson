from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            'unicode_character': 0,
            'single_number': 1,
            '!symbol_8': 2,
            '!symbol_7': 3,
            '!symbol_11': 4,
            'normal_character': 5,
            '!symbol_5': 6,
            '!symbol_2': 7,
            '!symbol_13': 8,
            '!symbol_10': 9,
            '!symbol_4': 10,
            '!symbol_1': 11,
            'escape_character': 12,
            'reference': 13,
            '!symbol_3': 14,
            '$': 15,
            '!symbol_6': 16,
            '!symbol_12': 17,
            '!symbol_14': 18,
            '!symbol_9': 19
        }
        self.__sparse_action_table: dict = {
            0: {0: 's13', 1: 's14', 5: 's12', 7: 's7', 12: 's11', 13: 's15', 14: 's16', 16: 's17'},
            1: {15: 'a'},
            2: {15: 'r35'},
            3: {3: 'r15', 11: 'r15', 15: 'r15'},
            4: {0: 's13', 1: 's14', 3: 'r24', 5: 's12', 7: 's7', 11: 'r24', 12: 's11', 13: 's15', 14: 's16', 15: 'r24', 16: 's17'},
            5: {0: 'r34', 1: 'r34', 3: 'r34', 5: 'r34', 7: 'r34', 11: 'r34', 12: 'r34', 13: 'r34', 14: 'r34', 15: 'r34', 16: 'r34'},
            6: {0: 'r9', 1: 'r9', 3: 'r9', 4: 's35', 5: 'r9', 7: 'r9', 9: 's33', 11: 'r9', 12: 'r9', 13: 'r9', 14: 'r9', 15: 'r9', 16: 'r9', 17: 's34', 19: 's37'},
            7: {0: 'r8', 1: 'r8', 3: 'r8', 4: 'r8', 5: 'r8', 7: 'r8', 9: 'r8', 11: 'r8', 12: 'r8', 13: 'r8', 14: 'r8', 15: 'r8', 16: 'r8', 17: 'r8', 19: 'r8'},
            8: {0: 'r20', 1: 'r20', 3: 'r20', 4: 'r20', 5: 'r20', 7: 'r20', 9: 'r20', 11: 'r20', 12: 'r20', 13: 'r20', 14: 'r20', 15: 'r20', 16: 'r20', 17: 'r20', 19: 'r20'},
            9: {0: 'r39', 1: 'r39', 3: 'r39', 4: 'r39', 5: 'r39', 7: 'r39', 9: 'r39', 11: 'r39', 12: 'r39', 13: 'r39', 14: 'r39', 15: 'r39', 16: 'r39', 17: 'r39', 19: 'r39'},
            10: {0: 'r5', 1: 'r5', 3: 'r5', 4: 'r5', 5: 'r5', 7: 'r5', 9: 'r5', 11: 'r5', 12: 'r5', 13: 'r5', 14: 'r5', 15: 'r5', 16: 'r5', 17: 'r5', 19: 'r5'},
            11: {0: 'r31', 1: 'r31', 3: 'r31', 4: 'r31', 5: 'r31', 6: 'r31', 7: 'r31', 9: 'r31', 11: 'r31', 12: 'r31', 13: 'r31', 14: 'r31', 15: 'r31', 16: 'r31', 17: 'r31', 19: 'r31'},
            12: {0: 'r10', 1: 'r10', 2: 'r10', 3: 'r10', 4: 'r10', 5: 'r10', 6: 'r10', 7: 'r10', 9: 'r10', 11: 'r10', 12: 'r10', 13: 'r10', 14: 'r10', 15: 'r10', 16: 'r10', 17: 'r10', 19: 'r10'},
            13: {0: 'r23', 1: 'r23', 2: 'r23', 3: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 9: 'r23', 11: 'r23', 12: 'r23', 13: 'r23', 14: 'r23', 15: 'r23', 16: 'r23', 17: 'r23', 19: 'r23'},
            14: {0: 'r38', 1: 'r38', 2: 'r38', 3: 'r38', 4: 'r38', 5: 'r38', 6: 'r38', 7: 'r38', 9: 'r38', 11: 'r38', 12: 'r38', 13: 'r38', 14: 'r38', 15: 'r38', 16: 'r38', 17: 'r38', 19: 'r38'},
            15: {0: 'r21', 1: 'r21', 3: 'r21', 4: 'r21', 5: 'r21', 7: 'r21', 9: 'r21', 11: 'r21', 12: 'r21', 13: 'r21', 14: 'r21', 15: 'r21', 16: 'r21', 17: 'r21', 19: 'r21'},
            16: {0: 'r36', 1: 'r36', 5: 'r36', 10: 's20', 12: 'r36'},
            17: {0: 's13', 1: 's14', 5: 's12', 7: 's7', 12: 's11', 13: 's15', 14: 's16', 16: 's17'},
            18: {3: 's19'},
            19: {0: 'r25', 1: 'r25', 3: 'r25', 4: 'r25', 5: 'r25', 7: 'r25', 9: 'r25', 11: 'r25', 12: 'r25', 13: 'r25', 14: 'r25', 15: 'r25', 16: 'r25', 17: 'r25', 19: 'r25'},
            20: {0: 'r32', 1: 'r32', 5: 'r32', 12: 'r32'},
            21: {0: 's13', 1: 's14', 5: 's12', 12: 's11'},
            22: {0: 'r7', 1: 'r7', 5: 'r7', 12: 'r7'},
            23: {0: 's13', 1: 's14', 5: 's12', 6: 's30', 12: 's11'},
            24: {0: 'r29', 1: 'r29', 5: 'r29', 6: 'r29', 12: 'r29'},
            25: {0: 'r19', 1: 'r19', 5: 'r19', 6: 'r19', 12: 'r19'},
            26: {0: 'r5', 1: 'r5', 2: 's27', 5: 'r5', 6: 'r5', 12: 'r5'},
            27: {0: 's13', 1: 's14', 5: 's12'},
            28: {0: 'r26', 1: 'r26', 5: 'r26', 6: 'r26', 12: 'r26'},
            29: {0: 'r16', 1: 'r16', 5: 'r16', 6: 'r16', 12: 'r16'},
            30: {0: 'r22', 1: 'r22', 3: 'r22', 4: 'r22', 5: 'r22', 7: 'r22', 9: 'r22', 11: 'r22', 12: 'r22', 13: 'r22', 14: 'r22', 15: 'r22', 16: 'r22', 17: 'r22', 19: 'r22'},
            31: {0: 'r12', 1: 'r12', 3: 'r12', 5: 'r12', 7: 'r12', 11: 'r12', 12: 'r12', 13: 'r12', 14: 'r12', 15: 'r12', 16: 'r12'},
            32: {0: 'r11', 1: 'r11', 3: 'r11', 5: 'r11', 7: 'r11', 11: 'r11', 12: 'r11', 13: 'r11', 14: 'r11', 15: 'r11', 16: 'r11'},
            33: {0: 'r2', 1: 'r2', 3: 'r2', 5: 'r2', 7: 'r2', 11: 'r2', 12: 'r2', 13: 'r2', 14: 'r2', 15: 'r2', 16: 'r2'},
            34: {1: 's40'},
            35: {0: 'r14', 1: 'r14', 3: 'r14', 5: 'r14', 7: 'r14', 11: 'r14', 12: 'r14', 13: 'r14', 14: 'r14', 15: 'r14', 16: 'r14'},
            36: {0: 'r4', 1: 'r4', 3: 'r4', 5: 'r4', 7: 'r4', 11: 'r4', 12: 'r4', 13: 'r4', 14: 'r4', 15: 'r4', 16: 'r4'},
            37: {0: 'r41', 1: 'r41', 3: 'r41', 5: 'r41', 7: 'r41', 11: 'r41', 12: 'r41', 13: 'r41', 14: 'r41', 15: 'r41', 16: 'r41'},
            38: {8: 's42', 18: 's43'},
            39: {1: 's41', 8: 'r18', 18: 'r18'},
            40: {1: 'r3', 8: 'r3', 18: 'r3'},
            41: {1: 'r1', 8: 'r1', 18: 'r1'},
            42: {1: 's40', 18: 'r6'},
            43: {0: 'r17', 1: 'r17', 3: 'r17', 5: 'r17', 7: 'r17', 11: 'r17', 12: 'r17', 13: 'r17', 14: 'r17', 15: 'r17', 16: 'r17'},
            44: {18: 's47'},
            45: {18: 'r40'},
            46: {18: 'r30'},
            47: {0: 'r13', 1: 'r13', 3: 'r13', 5: 'r13', 7: 'r13', 11: 'r13', 12: 'r13', 13: 'r13', 14: 'r13', 15: 'r13', 16: 'r13'},
            48: {0: 'r33', 1: 'r33', 3: 'r33', 5: 'r33', 7: 'r33', 11: 'r33', 12: 'r33', 13: 'r33', 14: 'r33', 15: 'r33', 16: 'r33'},
            49: {3: 'r27', 11: 's50', 15: 'r27'},
            50: {0: 's13', 1: 's14', 5: 's12', 7: 's7', 12: 's11', 13: 's15', 14: 's16', 16: 's17'},
            51: {3: 'r37', 11: 'r37', 15: 'r37'},
            52: {3: 'r28', 11: 'r28', 15: 'r28'}
        }
        self.__sparse_goto_table: dict = {
            0: {3: 1, 4: 5, 9: 2, 10: 3, 11: 10, 16: 6, 17: 8, 19: 4, 21: 9},
            3: {14: 49},
            4: {4: 48, 11: 10, 16: 6, 17: 8, 21: 9},
            6: {0: 31, 2: 36, 15: 32},
            16: {1: 22, 5: 21},
            17: {4: 5, 9: 18, 10: 3, 11: 10, 16: 6, 17: 8, 19: 4, 21: 9},
            21: {7: 23, 11: 26, 18: 24, 21: 25},
            23: {11: 26, 18: 29, 21: 25},
            27: {11: 28},
            34: {12: 39, 20: 38},
            42: {6: 44, 12: 39, 20: 46, 22: 45},
            49: {13: 51},
            50: {4: 5, 10: 52, 11: 10, 16: 6, 17: 8, 19: 4, 21: 9}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            18: ('*0',),
            1: ('*0', '1'),
            17: ('1', '1'),
            13: ('1', '*3'),
            30: ('0',),
            6: (),
            40: ('*0',),
            26: ('0', '2'),
            21: ('0',),
            25: ('1',),
            22: ('*1', '2'),
            32: ('0',),
            16: ('*0', '1'),
            36: (),
            7: ('*0',),
            23: ('0',),
            8: (),
            20: ('0',),
            39: ('0',),
            4: ('0', '*1'),
            11: ('0',),
            9: (),
            12: ('*0',),
            24: ('*0',),
            33: ('*0', '1'),
            27: ('0', '*1'),
            28: ('1',),
            15: (),
            37: ('*0', '*1'),
            35: ('0',)
        }
        self.__reduce_symbol_count: list = [1, 2, 1, 1, 2, 1, 0, 1, 1, 0, 1, 1, 1, 5, 1, 0, 2, 3, 1, 1, 1, 1, 4, 1, 1, 3, 3, 2, 2, 1, 1, 1, 1, 2, 1, 1, 0, 2, 1, 1, 1, 1]
        self.__reduce_non_terminal_index: list = [8, 12, 15, 12, 4, 21, 6, 5, 16, 2, 11, 0, 2, 15, 15, 14, 7, 15, 20, 18, 16, 17, 17, 11, 10, 17, 18, 9, 13, 7, 22, 21, 1, 19, 19, 3, 5, 14, 11, 16, 6, 15]

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
                elif statement_index in {0, 2, 3, 34, 5, 38, 41, 10, 14, 19, 29, 31}:
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
