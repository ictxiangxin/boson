from typing import Dict, List, Tuple

from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: Dict[str, int] = {
            'escape_character': 0,
            '!symbol_12': 1,
            '$': 2,
            '!symbol_13': 3,
            '!symbol_11': 4,
            '!symbol_3': 5,
            '!symbol_7': 6,
            '!symbol_10': 7,
            'single_number': 8,
            '!symbol_9': 9,
            'normal_character': 10,
            '!symbol_4': 11,
            '!symbol_14': 12,
            '!symbol_5': 13,
            '!symbol_6': 14,
            'reference': 15,
            '!symbol_1': 16,
            '!symbol_2': 17,
            '!symbol_8': 18,
            'unicode_character': 19
        }
        self.__sparse_action_table: Dict[int, Dict[int, str]] = {
            0: {0: 's10', 5: 's16', 8: 's14', 10: 's13', 14: 's17', 15: 's15', 17: 's8', 19: 's12'},
            1: {2: 'a'},
            2: {2: 'r30'},
            3: {2: 'r39', 6: 'r39', 16: 'r39'},
            4: {0: 's10', 2: 'r20', 5: 's16', 6: 'r20', 8: 's14', 10: 's13', 14: 's17', 15: 's15', 16: 'r20', 17: 's8', 19: 's12'},
            5: {0: 'r25', 2: 'r25', 5: 'r25', 6: 'r25', 8: 'r25', 10: 'r25', 14: 'r25', 15: 'r25', 16: 'r25', 17: 'r25', 19: 'r25'},
            6: {0: 'r8', 1: 's34', 2: 'r8', 4: 's33', 5: 'r8', 6: 'r8', 7: 's37', 8: 'r8', 9: 's36', 10: 'r8', 14: 'r8', 15: 'r8', 16: 'r8', 17: 'r8', 19: 'r8'},
            7: {0: 'r16', 1: 'r16', 2: 'r16', 4: 'r16', 5: 'r16', 6: 'r16', 7: 'r16', 8: 'r16', 9: 'r16', 10: 'r16', 14: 'r16', 15: 'r16', 16: 'r16', 17: 'r16', 19: 'r16'},
            8: {0: 'r23', 1: 'r23', 2: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 8: 'r23', 9: 'r23', 10: 'r23', 14: 'r23', 15: 'r23', 16: 'r23', 17: 'r23', 19: 'r23'},
            9: {0: 'r33', 1: 'r33', 2: 'r33', 4: 'r33', 5: 'r33', 6: 'r33', 7: 'r33', 8: 'r33', 9: 'r33', 10: 'r33', 14: 'r33', 15: 'r33', 16: 'r33', 17: 'r33', 19: 'r33'},
            10: {0: 'r12', 1: 'r12', 2: 'r12', 4: 'r12', 5: 'r12', 6: 'r12', 7: 'r12', 8: 'r12', 9: 'r12', 10: 'r12', 13: 'r12', 14: 'r12', 15: 'r12', 16: 'r12', 17: 'r12', 19: 'r12'},
            11: {0: 'r14', 1: 'r14', 2: 'r14', 4: 'r14', 5: 'r14', 6: 'r14', 7: 'r14', 8: 'r14', 9: 'r14', 10: 'r14', 14: 'r14', 15: 'r14', 16: 'r14', 17: 'r14', 19: 'r14'},
            12: {0: 'r17', 1: 'r17', 2: 'r17', 4: 'r17', 5: 'r17', 6: 'r17', 7: 'r17', 8: 'r17', 9: 'r17', 10: 'r17', 13: 'r17', 14: 'r17', 15: 'r17', 16: 'r17', 17: 'r17', 18: 'r17', 19: 'r17'},
            13: {0: 'r19', 1: 'r19', 2: 'r19', 4: 'r19', 5: 'r19', 6: 'r19', 7: 'r19', 8: 'r19', 9: 'r19', 10: 'r19', 13: 'r19', 14: 'r19', 15: 'r19', 16: 'r19', 17: 'r19', 18: 'r19', 19: 'r19'},
            14: {0: 'r37', 1: 'r37', 2: 'r37', 4: 'r37', 5: 'r37', 6: 'r37', 7: 'r37', 8: 'r37', 9: 'r37', 10: 'r37', 13: 'r37', 14: 'r37', 15: 'r37', 16: 'r37', 17: 'r37', 18: 'r37', 19: 'r37'},
            15: {0: 'r27', 1: 'r27', 2: 'r27', 4: 'r27', 5: 'r27', 6: 'r27', 7: 'r27', 8: 'r27', 9: 'r27', 10: 'r27', 14: 'r27', 15: 'r27', 16: 'r27', 17: 'r27', 19: 'r27'},
            16: {0: 'r41', 8: 'r41', 10: 'r41', 11: 's21', 19: 'r41'},
            17: {0: 's10', 5: 's16', 8: 's14', 10: 's13', 14: 's17', 15: 's15', 17: 's8', 19: 's12'},
            18: {6: 's19'},
            19: {0: 'r38', 1: 'r38', 2: 'r38', 4: 'r38', 5: 'r38', 6: 'r38', 7: 'r38', 8: 'r38', 9: 'r38', 10: 'r38', 14: 'r38', 15: 'r38', 16: 'r38', 17: 'r38', 19: 'r38'},
            20: {0: 'r40', 8: 'r40', 10: 'r40', 19: 'r40'},
            21: {0: 'r15', 8: 'r15', 10: 'r15', 19: 'r15'},
            22: {0: 's10', 8: 's14', 10: 's13', 19: 's12'},
            23: {0: 's10', 8: 's14', 10: 's13', 13: 's30', 19: 's12'},
            24: {0: 'r5', 8: 'r5', 10: 'r5', 13: 'r5', 19: 'r5'},
            25: {0: 'r14', 8: 'r14', 10: 'r14', 13: 'r14', 18: 's27', 19: 'r14'},
            26: {0: 'r1', 8: 'r1', 10: 'r1', 13: 'r1', 19: 'r1'},
            27: {8: 's14', 10: 's13', 19: 's12'},
            28: {0: 'r4', 8: 'r4', 10: 'r4', 13: 'r4', 19: 'r4'},
            29: {0: 'r3', 8: 'r3', 10: 'r3', 13: 'r3', 19: 'r3'},
            30: {0: 'r32', 1: 'r32', 2: 'r32', 4: 'r32', 5: 'r32', 6: 'r32', 7: 'r32', 8: 'r32', 9: 'r32', 10: 'r32', 14: 'r32', 15: 'r32', 16: 'r32', 17: 'r32', 19: 'r32'},
            31: {0: 'r6', 2: 'r6', 5: 'r6', 6: 'r6', 8: 'r6', 10: 'r6', 14: 'r6', 15: 'r6', 16: 'r6', 17: 'r6', 19: 'r6'},
            32: {0: 'r21', 2: 'r21', 5: 'r21', 6: 'r21', 8: 'r21', 10: 'r21', 14: 'r21', 15: 'r21', 16: 'r21', 17: 'r21', 19: 'r21'},
            33: {0: 'r10', 2: 'r10', 5: 'r10', 6: 'r10', 8: 'r10', 10: 'r10', 14: 'r10', 15: 'r10', 16: 'r10', 17: 'r10', 19: 'r10'},
            34: {8: 's40'},
            35: {0: 'r9', 2: 'r9', 5: 'r9', 6: 'r9', 8: 'r9', 10: 'r9', 14: 'r9', 15: 'r9', 16: 'r9', 17: 'r9', 19: 'r9'},
            36: {0: 'r31', 2: 'r31', 5: 'r31', 6: 'r31', 8: 'r31', 10: 'r31', 14: 'r31', 15: 'r31', 16: 'r31', 17: 'r31', 19: 'r31'},
            37: {0: 'r36', 2: 'r36', 5: 'r36', 6: 'r36', 8: 'r36', 10: 'r36', 14: 'r36', 15: 'r36', 16: 'r36', 17: 'r36', 19: 'r36'},
            38: {3: 's43', 12: 's42'},
            39: {3: 'r11', 8: 's41', 12: 'r11'},
            40: {3: 'r2', 8: 'r2', 12: 'r2'},
            41: {3: 'r7', 8: 'r7', 12: 'r7'},
            42: {0: 'r13', 2: 'r13', 5: 'r13', 6: 'r13', 8: 'r13', 10: 'r13', 14: 'r13', 15: 'r13', 16: 'r13', 17: 'r13', 19: 'r13'},
            43: {8: 's40', 12: 'r18'},
            44: {12: 's47'},
            45: {12: 'r34'},
            46: {12: 'r28'},
            47: {0: 'r29', 2: 'r29', 5: 'r29', 6: 'r29', 8: 'r29', 10: 'r29', 14: 'r29', 15: 'r29', 16: 'r29', 17: 'r29', 19: 'r29'},
            48: {0: 'r22', 2: 'r22', 5: 'r22', 6: 'r22', 8: 'r22', 10: 'r22', 14: 'r22', 15: 'r22', 16: 'r22', 17: 'r22', 19: 'r22'},
            49: {2: 'r24', 6: 'r24', 16: 's50'},
            50: {0: 's10', 5: 's16', 8: 's14', 10: 's13', 14: 's17', 15: 's15', 17: 's8', 19: 's12'},
            51: {2: 'r26', 6: 'r26', 16: 'r26'},
            52: {2: 'r35', 6: 'r35', 16: 'r35'}
        }
        self.__sparse_goto_table: Dict[int, Dict[int, int]] = {
            0: {0: 5, 1: 4, 2: 1, 4: 9, 8: 11, 10: 3, 13: 6, 15: 2, 22: 7},
            3: {16: 49},
            4: {0: 48, 4: 9, 8: 11, 13: 6, 22: 7},
            6: {5: 32, 11: 31, 21: 35},
            16: {12: 20, 17: 22},
            17: {0: 5, 1: 4, 4: 9, 8: 11, 10: 3, 13: 6, 15: 18, 22: 7},
            22: {4: 26, 6: 23, 8: 25, 20: 24},
            23: {4: 26, 8: 25, 20: 29},
            27: {8: 28},
            34: {7: 38, 18: 39},
            43: {7: 46, 9: 44, 18: 39, 19: 45},
            49: {3: 51},
            50: {0: 5, 1: 4, 4: 9, 8: 11, 10: 52, 13: 6, 22: 7}
        }
        self.__sentence_index_grammar_tuple_mapping: Dict[int, Tuple[str, ...]] = {
            11: ('*0',),
            7: ('*0', '1'),
            13: ('1', '1'),
            29: ('1', '*3'),
            18: (),
            34: ('*0',),
            4: ('0', '2'),
            27: ('0',),
            38: ('1',),
            32: ('*1', '2'),
            3: ('*0', '1'),
            41: (),
            40: ('*0',),
            17: ('0',),
            23: (),
            16: ('0',),
            33: ('0',),
            9: ('0', '*1'),
            8: (),
            6: ('*0',),
            20: ('*0',),
            22: ('*0', '1'),
            24: ('0', '*1'),
            35: ('1',),
            39: (),
            26: ('*0', '*1'),
            30: ('0',)
        }
        self.__reduce_symbol_count: List[int] = [1, 1, 1, 2, 3, 1, 1, 2, 0, 2, 1, 1, 1, 3, 1, 1, 1, 1, 0, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 5, 1, 1, 4, 1, 1, 2, 1, 1, 3, 0, 1, 0]
        self.__reduce_non_terminal_index: List[int] = [14, 20, 18, 6, 20, 6, 21, 18, 21, 0, 5, 7, 4, 5, 4, 12, 13, 8, 9, 8, 10, 11, 1, 13, 15, 1, 16, 22, 19, 5, 2, 5, 22, 13, 9, 3, 5, 8, 22, 16, 17, 17]

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
                elif statement_index in {0, 1, 2, 36, 5, 37, 10, 12, 14, 15, 19, 21, 25, 28, 31}:
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
