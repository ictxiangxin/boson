from typing import Dict, List, Tuple

from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: Dict[str, int] = {
            '!symbol_1': 0,
            '!symbol_4': 1,
            '!symbol_3': 2,
            '!symbol_10': 3,
            '!symbol_9': 4,
            'unicode_character': 5,
            '$': 6,
            '!symbol_11': 7,
            'normal_character': 8,
            'single_number': 9,
            'reference': 10,
            '!symbol_7': 11,
            'escape_character': 12,
            '!symbol_6': 13,
            '!symbol_14': 14,
            '!symbol_12': 15,
            '!symbol_5': 16,
            '!symbol_8': 17,
            '!symbol_13': 18,
            '!symbol_2': 19
        }
        self.__sparse_action_table: Dict[int, Dict[int, str]] = {
            0: {2: 's17', 5: 's12', 8: 's14', 9: 's13', 10: 's16', 12: 's10', 13: 's15', 19: 's8'},
            1: {6: 'a'},
            2: {6: 'r13'},
            3: {0: 'r2', 6: 'r2', 11: 'r2'},
            4: {0: 'r10', 2: 's17', 5: 's12', 6: 'r10', 8: 's14', 9: 's13', 10: 's16', 11: 'r10', 12: 's10', 13: 's15', 19: 's8'},
            5: {0: 'r29', 2: 'r29', 5: 'r29', 6: 'r29', 8: 'r29', 9: 'r29', 10: 'r29', 11: 'r29', 12: 'r29', 13: 'r29', 19: 'r29'},
            6: {0: 'r30', 2: 'r30', 3: 's33', 4: 's34', 5: 'r30', 6: 'r30', 7: 's35', 8: 'r30', 9: 'r30', 10: 'r30', 11: 'r30', 12: 'r30', 13: 'r30', 15: 's37', 19: 'r30'},
            7: {0: 'r12', 2: 'r12', 3: 'r12', 4: 'r12', 5: 'r12', 6: 'r12', 7: 'r12', 8: 'r12', 9: 'r12', 10: 'r12', 11: 'r12', 12: 'r12', 13: 'r12', 15: 'r12', 19: 'r12'},
            8: {0: 'r18', 2: 'r18', 3: 'r18', 4: 'r18', 5: 'r18', 6: 'r18', 7: 'r18', 8: 'r18', 9: 'r18', 10: 'r18', 11: 'r18', 12: 'r18', 13: 'r18', 15: 'r18', 19: 'r18'},
            9: {0: 'r22', 2: 'r22', 3: 'r22', 4: 'r22', 5: 'r22', 6: 'r22', 7: 'r22', 8: 'r22', 9: 'r22', 10: 'r22', 11: 'r22', 12: 'r22', 13: 'r22', 15: 'r22', 19: 'r22'},
            10: {0: 'r1', 2: 'r1', 3: 'r1', 4: 'r1', 5: 'r1', 6: 'r1', 7: 'r1', 8: 'r1', 9: 'r1', 10: 'r1', 11: 'r1', 12: 'r1', 13: 'r1', 15: 'r1', 16: 'r1', 19: 'r1'},
            11: {0: 'r6', 2: 'r6', 3: 'r6', 4: 'r6', 5: 'r6', 6: 'r6', 7: 'r6', 8: 'r6', 9: 'r6', 10: 'r6', 11: 'r6', 12: 'r6', 13: 'r6', 15: 'r6', 19: 'r6'},
            12: {0: 'r24', 2: 'r24', 3: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 7: 'r24', 8: 'r24', 9: 'r24', 10: 'r24', 11: 'r24', 12: 'r24', 13: 'r24', 15: 'r24', 16: 'r24', 17: 'r24', 19: 'r24'},
            13: {0: 'r25', 2: 'r25', 3: 'r25', 4: 'r25', 5: 'r25', 6: 'r25', 7: 'r25', 8: 'r25', 9: 'r25', 10: 'r25', 11: 'r25', 12: 'r25', 13: 'r25', 15: 'r25', 16: 'r25', 17: 'r25', 19: 'r25'},
            14: {0: 'r41', 2: 'r41', 3: 'r41', 4: 'r41', 5: 'r41', 6: 'r41', 7: 'r41', 8: 'r41', 9: 'r41', 10: 'r41', 11: 'r41', 12: 'r41', 13: 'r41', 15: 'r41', 16: 'r41', 17: 'r41', 19: 'r41'},
            15: {2: 's17', 5: 's12', 8: 's14', 9: 's13', 10: 's16', 12: 's10', 13: 's15', 19: 's8'},
            16: {0: 'r15', 2: 'r15', 3: 'r15', 4: 'r15', 5: 'r15', 6: 'r15', 7: 'r15', 8: 'r15', 9: 'r15', 10: 'r15', 11: 'r15', 12: 'r15', 13: 'r15', 15: 'r15', 19: 'r15'},
            17: {1: 's18', 5: 'r27', 8: 'r27', 9: 'r27', 12: 'r27'},
            18: {5: 'r5', 8: 'r5', 9: 'r5', 12: 'r5'},
            19: {5: 's12', 8: 's14', 9: 's13', 12: 's10'},
            20: {5: 'r36', 8: 'r36', 9: 'r36', 12: 'r36'},
            21: {5: 'r6', 8: 'r6', 9: 'r6', 12: 'r6', 16: 'r6', 17: 's27'},
            22: {5: 's12', 8: 's14', 9: 's13', 12: 's10', 16: 's25'},
            23: {5: 'r14', 8: 'r14', 9: 'r14', 12: 'r14', 16: 'r14'},
            24: {5: 'r17', 8: 'r17', 9: 'r17', 12: 'r17', 16: 'r17'},
            25: {0: 'r38', 2: 'r38', 3: 'r38', 4: 'r38', 5: 'r38', 6: 'r38', 7: 'r38', 8: 'r38', 9: 'r38', 10: 'r38', 11: 'r38', 12: 'r38', 13: 'r38', 15: 'r38', 19: 'r38'},
            26: {5: 'r9', 8: 'r9', 9: 'r9', 12: 'r9', 16: 'r9'},
            27: {5: 's12', 8: 's14', 9: 's13'},
            28: {5: 'r3', 8: 'r3', 9: 'r3', 12: 'r3', 16: 'r3'},
            29: {11: 's30'},
            30: {0: 'r8', 2: 'r8', 3: 'r8', 4: 'r8', 5: 'r8', 6: 'r8', 7: 'r8', 8: 'r8', 9: 'r8', 10: 'r8', 11: 'r8', 12: 'r8', 13: 'r8', 15: 'r8', 19: 'r8'},
            31: {0: 'r20', 2: 'r20', 5: 'r20', 6: 'r20', 8: 'r20', 9: 'r20', 10: 'r20', 11: 'r20', 12: 'r20', 13: 'r20', 19: 'r20'},
            32: {0: 'r26', 2: 'r26', 5: 'r26', 6: 'r26', 8: 'r26', 9: 'r26', 10: 'r26', 11: 'r26', 12: 'r26', 13: 'r26', 19: 'r26'},
            33: {0: 'r4', 2: 'r4', 5: 'r4', 6: 'r4', 8: 'r4', 9: 'r4', 10: 'r4', 11: 'r4', 12: 'r4', 13: 'r4', 19: 'r4'},
            34: {0: 'r7', 2: 'r7', 5: 'r7', 6: 'r7', 8: 'r7', 9: 'r7', 10: 'r7', 11: 'r7', 12: 'r7', 13: 'r7', 19: 'r7'},
            35: {0: 'r11', 2: 'r11', 5: 'r11', 6: 'r11', 8: 'r11', 9: 'r11', 10: 'r11', 11: 'r11', 12: 'r11', 13: 'r11', 19: 'r11'},
            36: {0: 'r16', 2: 'r16', 5: 'r16', 6: 'r16', 8: 'r16', 9: 'r16', 10: 'r16', 11: 'r16', 12: 'r16', 13: 'r16', 19: 'r16'},
            37: {9: 's40'},
            38: {14: 's42', 18: 's43'},
            39: {9: 's41', 14: 'r35', 18: 'r35'},
            40: {9: 'r23', 14: 'r23', 18: 'r23'},
            41: {9: 'r34', 14: 'r34', 18: 'r34'},
            42: {0: 'r28', 2: 'r28', 5: 'r28', 6: 'r28', 8: 'r28', 9: 'r28', 10: 'r28', 11: 'r28', 12: 'r28', 13: 'r28', 19: 'r28'},
            43: {9: 's40', 14: 'r32'},
            44: {14: 'r39'},
            45: {14: 'r37'},
            46: {14: 's47'},
            47: {0: 'r40', 2: 'r40', 5: 'r40', 6: 'r40', 8: 'r40', 9: 'r40', 10: 'r40', 11: 'r40', 12: 'r40', 13: 'r40', 19: 'r40'},
            48: {0: 'r21', 2: 'r21', 5: 'r21', 6: 'r21', 8: 'r21', 9: 'r21', 10: 'r21', 11: 'r21', 12: 'r21', 13: 'r21', 19: 'r21'},
            49: {0: 's50', 6: 'r19', 11: 'r19'},
            50: {2: 's17', 5: 's12', 8: 's14', 9: 's13', 10: 's16', 12: 's10', 13: 's15', 19: 's8'},
            51: {0: 'r33', 6: 'r33', 11: 'r33'},
            52: {0: 'r31', 6: 'r31', 11: 'r31'}
        }
        self.__sparse_goto_table: Dict[int, Dict[int, int]] = {
            0: {8: 6, 11: 5, 12: 1, 13: 9, 15: 4, 16: 2, 19: 11, 20: 7, 22: 3},
            3: {17: 49},
            4: {8: 6, 11: 48, 13: 9, 19: 11, 20: 7},
            6: {2: 36, 6: 32, 21: 31},
            15: {8: 6, 11: 5, 13: 9, 15: 4, 16: 29, 19: 11, 20: 7, 22: 3},
            17: {3: 20, 5: 19},
            19: {1: 22, 10: 23, 13: 24, 19: 21},
            22: {10: 26, 13: 24, 19: 21},
            27: {19: 28},
            37: {14: 38, 18: 39},
            43: {4: 44, 7: 46, 14: 45, 18: 39},
            49: {9: 51},
            50: {8: 6, 11: 5, 13: 9, 15: 4, 19: 11, 20: 7, 22: 52}
        }
        self.__sentence_index_grammar_tuple_mapping: Dict[int, Tuple[str, ...]] = {
            35: ('*0',),
            34: ('*0', '1'),
            28: ('1', '1'),
            40: ('1', '*3'),
            37: ('0',),
            32: (),
            39: ('*0',),
            3: ('0', '2'),
            15: ('0',),
            8: ('1',),
            38: ('*1', '2'),
            5: ('0',),
            9: ('*0', '1'),
            27: (),
            36: ('*0',),
            24: ('0',),
            18: (),
            12: ('0',),
            22: ('0',),
            16: ('0', '*1'),
            26: ('0',),
            30: (),
            20: ('*0',),
            10: ('*0',),
            21: ('*0', '1'),
            19: ('0', '*1'),
            31: ('1',),
            2: (),
            33: ('*0', '*1'),
            13: ('0',)
        }
        self.__reduce_symbol_count: List[int] = [1, 1, 0, 3, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 0, 3, 1, 0, 2, 0, 2, 2, 1, 1, 1, 4, 1, 5, 1]
        self.__reduce_non_terminal_index: List[int] = [0, 13, 17, 10, 6, 3, 13, 6, 20, 1, 22, 6, 8, 12, 1, 20, 11, 10, 8, 16, 2, 15, 8, 18, 19, 19, 21, 5, 6, 15, 2, 9, 7, 17, 18, 14, 5, 4, 20, 7, 6, 19]

    def parse(self, token_list: List[RegularToken]) -> BosonGrammar:
        grammar: BosonGrammar = BosonGrammar()
        analysis_stack: List[int] = [0]
        symbol_stack: List[BosonGrammarNode] = []
        token_index: int = 0
        while token_index < len(token_list):
            token: RegularToken = token_list[token_index]
            current_state: int = analysis_stack[-1]
            if token.symbol in self.__terminal_index_mapping:
                operation: str = self.__sparse_action_table.get(current_state, {}).get(self.__terminal_index_mapping[token.symbol], 'e')
            else:
                operation: str = 'e'
            operation_flag: str = operation[0]
            if operation_flag == 'e':
                grammar.error_index = token_index
                return grammar
            elif operation_flag == 's':
                analysis_stack.append(int(operation[1:]))
                token_index += 1
                grammar_node: BosonGrammarNode = BosonGrammarNode(token.text)
                symbol_stack.append(grammar_node)
            elif operation_flag == 'r':
                statement_index: int = int(operation[1:])
                reduce_count: int = self.__reduce_symbol_count[statement_index]
                for _ in range(reduce_count):
                    analysis_stack.pop()
                current_state: int = analysis_stack[-1]
                current_non_terminal_index: int = self.__reduce_non_terminal_index[statement_index]
                goto_next_state: int = self.__sparse_goto_table.get(current_state, {}).get(current_non_terminal_index, -1)
                if goto_next_state == -1:
                    raise ValueError('Invalid goto action: state={}, non-terminal={}'.format(current_state, current_non_terminal_index))
                analysis_stack.append(goto_next_state)
                if statement_index in self.__sentence_index_grammar_tuple_mapping:
                    symbol_package: List[BosonGrammarNode] = []
                    for _ in range(reduce_count):
                        symbol_package.insert(0, symbol_stack.pop())
                    grammar_node: BosonGrammarNode = BosonGrammarNode()
                    for node_string in self.__sentence_index_grammar_tuple_mapping[statement_index]:
                        if node_string[0] == '*':
                            for node in symbol_package[int(node_string[1:])]:
                                grammar_node.append(node)
                        else:
                            grammar_node.append(symbol_package[int(node_string)])
                    grammar_node.set_reduce_number(statement_index)
                    symbol_stack.append(grammar_node)
                elif statement_index in {0, 1, 4, 6, 7, 41, 11, 14, 17, 23, 25, 29}:
                    grammar_node: BosonGrammarNode = BosonGrammarNode()
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
