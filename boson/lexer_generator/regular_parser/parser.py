from typing import Dict, List, Tuple

from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: Dict[str, int] = {
            '!symbol_14': 0,
            'unicode_character': 1,
            '!symbol_5': 2,
            '!symbol_6': 3,
            '!symbol_12': 4,
            '!symbol_9': 5,
            '!symbol_3': 6,
            '!symbol_11': 7,
            '!symbol_8': 8,
            '!symbol_7': 9,
            '!symbol_4': 10,
            '$': 11,
            '!symbol_13': 12,
            'single_number': 13,
            '!symbol_1': 14,
            'normal_character': 15,
            '!symbol_2': 16,
            'reference': 17,
            'escape_character': 18,
            '!symbol_10': 19
        }
        self.__sparse_action_table: Dict[int, Dict[int, str]] = {
            0: {1: 's14', 3: 's13', 6: 's11', 13: 's16', 15: 's15', 16: 's10', 17: 's12', 18: 's17'},
            1: {1: 'r20', 3: 'r20', 4: 'r20', 5: 'r20', 6: 'r20', 7: 'r20', 9: 'r20', 11: 'r20', 13: 'r20', 14: 'r20', 15: 'r20', 16: 'r20', 17: 'r20', 18: 'r20', 19: 'r20'},
            2: {11: 'a'},
            3: {11: 'r1'},
            4: {9: 'r7', 11: 'r7', 14: 'r7'},
            5: {1: 's14', 3: 's13', 6: 's11', 9: 'r17', 11: 'r17', 13: 's16', 14: 'r17', 15: 's15', 16: 's10', 17: 's12', 18: 's17'},
            6: {1: 'r4', 3: 'r4', 6: 'r4', 9: 'r4', 11: 'r4', 13: 'r4', 14: 'r4', 15: 'r4', 16: 'r4', 17: 'r4', 18: 'r4'},
            7: {1: 'r19', 3: 'r19', 4: 's34', 5: 's33', 6: 'r19', 7: 's37', 9: 'r19', 11: 'r19', 13: 'r19', 14: 'r19', 15: 'r19', 16: 'r19', 17: 'r19', 18: 'r19', 19: 's36'},
            8: {1: 'r28', 3: 'r28', 4: 'r28', 5: 'r28', 6: 'r28', 7: 'r28', 9: 'r28', 11: 'r28', 13: 'r28', 14: 'r28', 15: 'r28', 16: 'r28', 17: 'r28', 18: 'r28', 19: 'r28'},
            9: {1: 'r32', 3: 'r32', 4: 'r32', 5: 'r32', 6: 'r32', 7: 'r32', 9: 'r32', 11: 'r32', 13: 'r32', 14: 'r32', 15: 'r32', 16: 'r32', 17: 'r32', 18: 'r32', 19: 'r32'},
            10: {1: 'r39', 3: 'r39', 4: 'r39', 5: 'r39', 6: 'r39', 7: 'r39', 9: 'r39', 11: 'r39', 13: 'r39', 14: 'r39', 15: 'r39', 16: 'r39', 17: 'r39', 18: 'r39', 19: 'r39'},
            11: {1: 'r12', 10: 's22', 13: 'r12', 15: 'r12', 18: 'r12'},
            12: {1: 'r13', 3: 'r13', 4: 'r13', 5: 'r13', 6: 'r13', 7: 'r13', 9: 'r13', 11: 'r13', 13: 'r13', 14: 'r13', 15: 'r13', 16: 'r13', 17: 'r13', 18: 'r13', 19: 'r13'},
            13: {1: 's14', 3: 's13', 6: 's11', 13: 's16', 15: 's15', 16: 's10', 17: 's12', 18: 's17'},
            14: {1: 'r29', 2: 'r29', 3: 'r29', 4: 'r29', 5: 'r29', 6: 'r29', 7: 'r29', 8: 'r29', 9: 'r29', 11: 'r29', 13: 'r29', 14: 'r29', 15: 'r29', 16: 'r29', 17: 'r29', 18: 'r29', 19: 'r29'},
            15: {1: 'r35', 2: 'r35', 3: 'r35', 4: 'r35', 5: 'r35', 6: 'r35', 7: 'r35', 8: 'r35', 9: 'r35', 11: 'r35', 13: 'r35', 14: 'r35', 15: 'r35', 16: 'r35', 17: 'r35', 18: 'r35', 19: 'r35'},
            16: {1: 'r36', 2: 'r36', 3: 'r36', 4: 'r36', 5: 'r36', 6: 'r36', 7: 'r36', 8: 'r36', 9: 'r36', 11: 'r36', 13: 'r36', 14: 'r36', 15: 'r36', 16: 'r36', 17: 'r36', 18: 'r36', 19: 'r36'},
            17: {1: 'r15', 2: 'r15', 3: 'r15', 4: 'r15', 5: 'r15', 6: 'r15', 7: 'r15', 9: 'r15', 11: 'r15', 13: 'r15', 14: 'r15', 15: 'r15', 16: 'r15', 17: 'r15', 18: 'r15', 19: 'r15'},
            18: {9: 's19'},
            19: {1: 'r21', 3: 'r21', 4: 'r21', 5: 'r21', 6: 'r21', 7: 'r21', 9: 'r21', 11: 'r21', 13: 'r21', 14: 'r21', 15: 'r21', 16: 'r21', 17: 'r21', 18: 'r21', 19: 'r21'},
            20: {1: 's14', 13: 's16', 15: 's15', 18: 's17'},
            21: {1: 'r24', 13: 'r24', 15: 'r24', 18: 'r24'},
            22: {1: 'r40', 13: 'r40', 15: 'r40', 18: 'r40'},
            23: {1: 'r20', 2: 'r20', 8: 's29', 13: 'r20', 15: 'r20', 18: 'r20'},
            24: {1: 's14', 2: 's27', 13: 's16', 15: 's15', 18: 's17'},
            25: {1: 'r18', 2: 'r18', 13: 'r18', 15: 'r18', 18: 'r18'},
            26: {1: 'r10', 2: 'r10', 13: 'r10', 15: 'r10', 18: 'r10'},
            27: {1: 'r6', 3: 'r6', 4: 'r6', 5: 'r6', 6: 'r6', 7: 'r6', 9: 'r6', 11: 'r6', 13: 'r6', 14: 'r6', 15: 'r6', 16: 'r6', 17: 'r6', 18: 'r6', 19: 'r6'},
            28: {1: 'r25', 2: 'r25', 13: 'r25', 15: 'r25', 18: 'r25'},
            29: {1: 's14', 13: 's16', 15: 's15'},
            30: {1: 'r30', 2: 'r30', 13: 'r30', 15: 'r30', 18: 'r30'},
            31: {1: 'r5', 3: 'r5', 6: 'r5', 9: 'r5', 11: 'r5', 13: 'r5', 14: 'r5', 15: 'r5', 16: 'r5', 17: 'r5', 18: 'r5'},
            32: {1: 'r41', 3: 'r41', 6: 'r41', 9: 'r41', 11: 'r41', 13: 'r41', 14: 'r41', 15: 'r41', 16: 'r41', 17: 'r41', 18: 'r41'},
            33: {1: 'r2', 3: 'r2', 6: 'r2', 9: 'r2', 11: 'r2', 13: 'r2', 14: 'r2', 15: 'r2', 16: 'r2', 17: 'r2', 18: 'r2'},
            34: {13: 's40'},
            35: {1: 'r16', 3: 'r16', 6: 'r16', 9: 'r16', 11: 'r16', 13: 'r16', 14: 'r16', 15: 'r16', 16: 'r16', 17: 'r16', 18: 'r16'},
            36: {1: 'r22', 3: 'r22', 6: 'r22', 9: 'r22', 11: 'r22', 13: 'r22', 14: 'r22', 15: 'r22', 16: 'r22', 17: 'r22', 18: 'r22'},
            37: {1: 'r37', 3: 'r37', 6: 'r37', 9: 'r37', 11: 'r37', 13: 'r37', 14: 'r37', 15: 'r37', 16: 'r37', 17: 'r37', 18: 'r37'},
            38: {0: 's42', 12: 's43'},
            39: {0: 'r34', 12: 'r34', 13: 's41'},
            40: {0: 'r33', 12: 'r33', 13: 'r33'},
            41: {0: 'r27', 12: 'r27', 13: 'r27'},
            42: {1: 'r9', 3: 'r9', 6: 'r9', 9: 'r9', 11: 'r9', 13: 'r9', 14: 'r9', 15: 'r9', 16: 'r9', 17: 'r9', 18: 'r9'},
            43: {0: 'r23', 13: 's40'},
            44: {0: 's47'},
            45: {0: 'r8'},
            46: {0: 'r38'},
            47: {1: 'r14', 3: 'r14', 6: 'r14', 9: 'r14', 11: 'r14', 13: 'r14', 14: 'r14', 15: 'r14', 16: 'r14', 17: 'r14', 18: 'r14'},
            48: {1: 'r3', 3: 'r3', 6: 'r3', 9: 'r3', 11: 'r3', 13: 'r3', 14: 'r3', 15: 'r3', 16: 'r3', 17: 'r3', 18: 'r3'},
            49: {9: 'r31', 11: 'r31', 14: 's50'},
            50: {1: 's14', 3: 's13', 6: 's11', 13: 's16', 15: 's15', 16: 's10', 17: 's12', 18: 's17'},
            51: {9: 'r11', 11: 'r11', 14: 'r11'},
            52: {9: 'r26', 11: 'r26', 14: 'r26'}
        }
        self.__sparse_goto_table: Dict[int, Dict[int, int]] = {
            0: {7: 6, 11: 3, 13: 1, 17: 2, 18: 4, 19: 5, 20: 7, 21: 8, 22: 9},
            4: {1: 49},
            5: {7: 48, 13: 1, 20: 7, 21: 8, 22: 9},
            7: {2: 32, 6: 31, 10: 35},
            11: {12: 20, 15: 21},
            13: {7: 6, 11: 18, 13: 1, 18: 4, 19: 5, 20: 7, 21: 8, 22: 9},
            20: {9: 25, 13: 23, 16: 24, 21: 26},
            24: {9: 28, 13: 23, 21: 26},
            29: {13: 30},
            34: {5: 39, 8: 38},
            43: {3: 45, 4: 44, 5: 39, 8: 46},
            49: {0: 51},
            50: {7: 6, 13: 1, 18: 52, 19: 5, 20: 7, 21: 8, 22: 9}
        }
        self.__sentence_index_grammar_tuple_mapping: Dict[int, Tuple[str, ...]] = {
            34: ('*0',),
            27: ('*0', '1'),
            9: ('1', '1'),
            14: ('1', '*3'),
            38: ('0',),
            23: (),
            8: ('*0',),
            30: ('0', '2'),
            13: ('0',),
            21: ('1',),
            6: ('*1', '2'),
            40: ('0',),
            25: ('*0', '1'),
            12: (),
            24: ('*0',),
            29: ('0',),
            39: (),
            32: ('0',),
            28: ('0',),
            16: ('0', '*1'),
            41: ('0',),
            19: (),
            5: ('*0',),
            17: ('*0',),
            3: ('*0', '1'),
            31: ('0', '*1'),
            26: ('1',),
            7: (),
            11: ('*0', '*1'),
            1: ('0',)
        }
        self.__reduce_symbol_count: List[int] = [1, 1, 1, 2, 1, 1, 4, 0, 1, 3, 1, 2, 0, 1, 5, 1, 2, 1, 1, 0, 1, 3, 1, 0, 1, 2, 2, 2, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.__reduce_non_terminal_index: List[int] = [14, 17, 2, 19, 19, 10, 22, 1, 4, 2, 9, 1, 12, 22, 2, 21, 7, 18, 16, 10, 21, 22, 2, 4, 12, 16, 0, 5, 20, 13, 9, 11, 20, 5, 8, 13, 13, 2, 3, 20, 15, 6]

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
                elif statement_index in {0, 33, 2, 35, 4, 36, 37, 10, 15, 18, 20, 22}:
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
