from typing import Dict, List, Tuple

from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: Dict[str, int] = {
            '!symbol_14': 0,
            '!symbol_2': 1,
            '!symbol_13': 2,
            '!symbol_4': 3,
            '!symbol_6': 4,
            'reference': 5,
            'single_number': 6,
            'normal_character': 7,
            '!symbol_11': 8,
            'unicode_character': 9,
            '!symbol_8': 10,
            '!symbol_10': 11,
            '!symbol_9': 12,
            '!symbol_1': 13,
            '!symbol_5': 14,
            'escape_character': 15,
            '!symbol_3': 16,
            '$': 17,
            '!symbol_12': 18,
            '!symbol_7': 19
        }
        self.__sparse_action_table: Dict[int, Dict[int, str]] = {
            0: {1: 's7', 4: 's17', 5: 's16', 6: 's13', 7: 's12', 9: 's14', 15: 's10', 16: 's15'},
            1: {17: 'a'},
            2: {17: 'r19'},
            3: {13: 'r15', 17: 'r15', 19: 'r15'},
            4: {1: 's7', 4: 's17', 5: 's16', 6: 's13', 7: 's12', 9: 's14', 13: 'r41', 15: 's10', 16: 's15', 17: 'r41', 19: 'r41'},
            5: {1: 'r4', 4: 'r4', 5: 'r4', 6: 'r4', 7: 'r4', 9: 'r4', 13: 'r4', 15: 'r4', 16: 'r4', 17: 'r4', 19: 'r4'},
            6: {1: 'r29', 4: 'r29', 5: 'r29', 6: 'r29', 7: 'r29', 8: 's33', 9: 'r29', 11: 's34', 12: 's35', 13: 'r29', 15: 'r29', 16: 'r29', 17: 'r29', 18: 's37', 19: 'r29'},
            7: {1: 'r18', 4: 'r18', 5: 'r18', 6: 'r18', 7: 'r18', 8: 'r18', 9: 'r18', 11: 'r18', 12: 'r18', 13: 'r18', 15: 'r18', 16: 'r18', 17: 'r18', 18: 'r18', 19: 'r18'},
            8: {1: 'r28', 4: 'r28', 5: 'r28', 6: 'r28', 7: 'r28', 8: 'r28', 9: 'r28', 11: 'r28', 12: 'r28', 13: 'r28', 15: 'r28', 16: 'r28', 17: 'r28', 18: 'r28', 19: 'r28'},
            9: {1: 'r30', 4: 'r30', 5: 'r30', 6: 'r30', 7: 'r30', 8: 'r30', 9: 'r30', 11: 'r30', 12: 'r30', 13: 'r30', 15: 'r30', 16: 'r30', 17: 'r30', 18: 'r30', 19: 'r30'},
            10: {1: 'r2', 4: 'r2', 5: 'r2', 6: 'r2', 7: 'r2', 8: 'r2', 9: 'r2', 11: 'r2', 12: 'r2', 13: 'r2', 14: 'r2', 15: 'r2', 16: 'r2', 17: 'r2', 18: 'r2', 19: 'r2'},
            11: {1: 'r20', 4: 'r20', 5: 'r20', 6: 'r20', 7: 'r20', 8: 'r20', 9: 'r20', 11: 'r20', 12: 'r20', 13: 'r20', 15: 'r20', 16: 'r20', 17: 'r20', 18: 'r20', 19: 'r20'},
            12: {1: 'r13', 4: 'r13', 5: 'r13', 6: 'r13', 7: 'r13', 8: 'r13', 9: 'r13', 10: 'r13', 11: 'r13', 12: 'r13', 13: 'r13', 14: 'r13', 15: 'r13', 16: 'r13', 17: 'r13', 18: 'r13', 19: 'r13'},
            13: {1: 'r36', 4: 'r36', 5: 'r36', 6: 'r36', 7: 'r36', 8: 'r36', 9: 'r36', 10: 'r36', 11: 'r36', 12: 'r36', 13: 'r36', 14: 'r36', 15: 'r36', 16: 'r36', 17: 'r36', 18: 'r36', 19: 'r36'},
            14: {1: 'r38', 4: 'r38', 5: 'r38', 6: 'r38', 7: 'r38', 8: 'r38', 9: 'r38', 10: 'r38', 11: 'r38', 12: 'r38', 13: 'r38', 14: 'r38', 15: 'r38', 16: 'r38', 17: 'r38', 18: 'r38', 19: 'r38'},
            15: {3: 's21', 6: 'r14', 7: 'r14', 9: 'r14', 15: 'r14'},
            16: {1: 'r31', 4: 'r31', 5: 'r31', 6: 'r31', 7: 'r31', 8: 'r31', 9: 'r31', 11: 'r31', 12: 'r31', 13: 'r31', 15: 'r31', 16: 'r31', 17: 'r31', 18: 'r31', 19: 'r31'},
            17: {1: 's7', 4: 's17', 5: 's16', 6: 's13', 7: 's12', 9: 's14', 15: 's10', 16: 's15'},
            18: {19: 's19'},
            19: {1: 'r32', 4: 'r32', 5: 'r32', 6: 'r32', 7: 'r32', 8: 'r32', 9: 'r32', 11: 'r32', 12: 'r32', 13: 'r32', 15: 'r32', 16: 'r32', 17: 'r32', 18: 'r32', 19: 'r32'},
            20: {6: 'r7', 7: 'r7', 9: 'r7', 15: 'r7'},
            21: {6: 'r16', 7: 'r16', 9: 'r16', 15: 'r16'},
            22: {6: 's13', 7: 's12', 9: 's14', 15: 's10'},
            23: {6: 's13', 7: 's12', 9: 's14', 14: 's29', 15: 's10'},
            24: {6: 'r20', 7: 'r20', 9: 'r20', 10: 's27', 14: 'r20', 15: 'r20'},
            25: {6: 'r23', 7: 'r23', 9: 'r23', 14: 'r23', 15: 'r23'},
            26: {6: 'r17', 7: 'r17', 9: 'r17', 14: 'r17', 15: 'r17'},
            27: {6: 's13', 7: 's12', 9: 's14'},
            28: {6: 'r22', 7: 'r22', 9: 'r22', 14: 'r22', 15: 'r22'},
            29: {1: 'r9', 4: 'r9', 5: 'r9', 6: 'r9', 7: 'r9', 8: 'r9', 9: 'r9', 11: 'r9', 12: 'r9', 13: 'r9', 15: 'r9', 16: 'r9', 17: 'r9', 18: 'r9', 19: 'r9'},
            30: {6: 'r39', 7: 'r39', 9: 'r39', 14: 'r39', 15: 'r39'},
            31: {1: 'r10', 4: 'r10', 5: 'r10', 6: 'r10', 7: 'r10', 9: 'r10', 13: 'r10', 15: 'r10', 16: 'r10', 17: 'r10', 19: 'r10'},
            32: {1: 'r1', 4: 'r1', 5: 'r1', 6: 'r1', 7: 'r1', 9: 'r1', 13: 'r1', 15: 'r1', 16: 'r1', 17: 'r1', 19: 'r1'},
            33: {1: 'r3', 4: 'r3', 5: 'r3', 6: 'r3', 7: 'r3', 9: 'r3', 13: 'r3', 15: 'r3', 16: 'r3', 17: 'r3', 19: 'r3'},
            34: {1: 'r6', 4: 'r6', 5: 'r6', 6: 'r6', 7: 'r6', 9: 'r6', 13: 'r6', 15: 'r6', 16: 'r6', 17: 'r6', 19: 'r6'},
            35: {1: 'r26', 4: 'r26', 5: 'r26', 6: 'r26', 7: 'r26', 9: 'r26', 13: 'r26', 15: 'r26', 16: 'r26', 17: 'r26', 19: 'r26'},
            36: {1: 'r34', 4: 'r34', 5: 'r34', 6: 'r34', 7: 'r34', 9: 'r34', 13: 'r34', 15: 'r34', 16: 'r34', 17: 'r34', 19: 'r34'},
            37: {6: 's40'},
            38: {0: 's42', 2: 's43'},
            39: {0: 'r33', 2: 'r33', 6: 's41'},
            40: {0: 'r21', 2: 'r21', 6: 'r21'},
            41: {0: 'r5', 2: 'r5', 6: 'r5'},
            42: {1: 'r37', 4: 'r37', 5: 'r37', 6: 'r37', 7: 'r37', 9: 'r37', 13: 'r37', 15: 'r37', 16: 'r37', 17: 'r37', 19: 'r37'},
            43: {0: 'r8', 6: 's40'},
            44: {0: 's47'},
            45: {0: 'r24'},
            46: {0: 'r11'},
            47: {1: 'r40', 4: 'r40', 5: 'r40', 6: 'r40', 7: 'r40', 9: 'r40', 13: 'r40', 15: 'r40', 16: 'r40', 17: 'r40', 19: 'r40'},
            48: {1: 'r25', 4: 'r25', 5: 'r25', 6: 'r25', 7: 'r25', 9: 'r25', 13: 'r25', 15: 'r25', 16: 'r25', 17: 'r25', 19: 'r25'},
            49: {13: 's50', 17: 'r12', 19: 'r12'},
            50: {1: 's7', 4: 's17', 5: 's16', 6: 's13', 7: 's12', 9: 's14', 15: 's10', 16: 's15'},
            51: {13: 'r27', 17: 'r27', 19: 'r27'},
            52: {13: 'r35', 17: 'r35', 19: 'r35'}
        }
        self.__sparse_goto_table: Dict[int, Dict[int, int]] = {
            0: {8: 9, 10: 11, 11: 2, 13: 1, 14: 3, 16: 8, 18: 6, 21: 4, 22: 5},
            3: {6: 49},
            4: {8: 9, 10: 11, 16: 8, 18: 6, 22: 48},
            6: {7: 32, 15: 36, 20: 31},
            15: {3: 22, 17: 20},
            17: {8: 9, 10: 11, 11: 18, 14: 3, 16: 8, 18: 6, 21: 4, 22: 5},
            22: {0: 23, 1: 25, 8: 26, 10: 24},
            23: {1: 30, 8: 26, 10: 24},
            27: {10: 28},
            37: {9: 39, 12: 38},
            43: {2: 44, 5: 45, 9: 39, 12: 46},
            49: {19: 51},
            50: {8: 9, 10: 11, 14: 52, 16: 8, 18: 6, 21: 4, 22: 5}
        }
        self.__sentence_index_grammar_tuple_mapping: Dict[int, Tuple[str, ...]] = {
            33: ('*0',),
            5: ('*0', '1'),
            37: ('1', '1'),
            40: ('1', '*3'),
            8: (),
            24: ('*0',),
            22: ('0', '2'),
            31: ('0',),
            32: ('1',),
            9: ('*1', '2'),
            39: ('*0', '1'),
            14: (),
            7: ('*0',),
            38: ('0',),
            18: (),
            28: ('0',),
            30: ('0',),
            34: ('0', '*1'),
            29: (),
            10: ('*0',),
            41: ('*0',),
            25: ('*0', '1'),
            12: ('0', '*1'),
            35: ('1',),
            15: (),
            27: ('*0', '*1'),
            19: ('0',)
        }
        self.__reduce_symbol_count: List[int] = [1, 1, 1, 1, 1, 2, 1, 1, 0, 4, 1, 1, 2, 1, 0, 0, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 2, 1, 0, 1, 1, 3, 1, 2, 2, 1, 3, 1, 2, 5, 1]
        self.__reduce_non_terminal_index: List[int] = [4, 20, 8, 7, 21, 9, 7, 3, 2, 16, 15, 5, 11, 10, 3, 6, 17, 1, 18, 13, 8, 9, 1, 0, 2, 21, 7, 6, 18, 15, 18, 16, 16, 12, 22, 19, 10, 7, 10, 0, 7, 14]

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
                elif statement_index in {0, 1, 2, 3, 4, 36, 6, 11, 13, 16, 17, 20, 21, 23, 26}:
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
