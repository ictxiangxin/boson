from typing import Dict, List, Tuple

from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: Dict[str, int] = {
            '!symbol_12': 0,
            '!symbol_7': 1,
            '!symbol_11': 2,
            '!symbol_15': 3,
            '!symbol_14': 4,
            '!symbol_13': 5,
            '!symbol_5': 6,
            '!symbol_3': 7,
            '!symbol_2': 8,
            'reference': 9,
            '!symbol_4': 10,
            '!symbol_1': 11,
            '!symbol_18': 12,
            '!symbol_16': 13,
            '!symbol_9': 14,
            '$': 15,
            '!symbol_10': 16,
            '!symbol_8': 17,
            '!symbol_17': 18,
            '!symbol_6': 19
        }
        self.__sparse_action_table: Dict[int, Dict[int, str]] = {
            0: {1: 's12', 6: 's14', 7: 's16', 8: 's7', 9: 's10', 10: 's13', 16: 's11', 19: 's15'},
            1: {15: 'a'},
            2: {15: 'r9'},
            3: {2: 'r31', 11: 'r31', 15: 'r31'},
            4: {1: 's12', 2: 'r25', 6: 's14', 7: 's16', 8: 's7', 9: 's10', 10: 's13', 11: 'r25', 15: 'r25', 16: 's11', 19: 's15'},
            5: {1: 'r26', 2: 'r26', 6: 'r26', 7: 'r26', 8: 'r26', 9: 'r26', 10: 'r26', 11: 'r26', 15: 'r26', 16: 'r26', 19: 'r26'},
            6: {1: 'r22', 2: 'r22', 3: 's33', 4: 's35', 5: 's37', 6: 'r22', 7: 'r22', 8: 'r22', 9: 'r22', 10: 'r22', 11: 'r22', 13: 's34', 15: 'r22', 16: 'r22', 19: 'r22'},
            7: {1: 'r2', 2: 'r2', 3: 'r2', 4: 'r2', 5: 'r2', 6: 'r2', 7: 'r2', 8: 'r2', 9: 'r2', 10: 'r2', 11: 'r2', 13: 'r2', 15: 'r2', 16: 'r2', 19: 'r2'},
            8: {1: 'r16', 2: 'r16', 3: 'r16', 4: 'r16', 5: 'r16', 6: 'r16', 7: 'r16', 8: 'r16', 9: 'r16', 10: 'r16', 11: 'r16', 13: 'r16', 15: 'r16', 16: 'r16', 19: 'r16'},
            9: {1: 'r37', 2: 'r37', 3: 'r37', 4: 'r37', 5: 'r37', 6: 'r37', 7: 'r37', 8: 'r37', 9: 'r37', 10: 'r37', 11: 'r37', 13: 'r37', 15: 'r37', 16: 'r37', 19: 'r37'},
            10: {1: 'r18', 2: 'r18', 3: 'r18', 4: 'r18', 5: 'r18', 6: 'r18', 7: 'r18', 8: 'r18', 9: 'r18', 10: 'r18', 11: 'r18', 13: 'r18', 15: 'r18', 16: 'r18', 19: 'r18'},
            11: {1: 's12', 6: 's14', 7: 's16', 8: 's7', 9: 's10', 10: 's13', 16: 's11', 19: 's15'},
            12: {6: 'r39', 7: 'r39', 10: 'r39', 17: 's19', 19: 'r39'},
            13: {0: 'r6', 1: 'r6', 2: 'r6', 3: 'r6', 4: 'r6', 5: 'r6', 6: 'r6', 7: 'r6', 8: 'r6', 9: 'r6', 10: 'r6', 11: 'r6', 13: 'r6', 14: 'r6', 15: 'r6', 16: 'r6', 19: 'r6'},
            14: {0: 'r10', 1: 'r10', 2: 'r10', 3: 'r10', 4: 'r10', 5: 'r10', 6: 'r10', 7: 'r10', 8: 'r10', 9: 'r10', 10: 'r10', 11: 'r10', 13: 'r10', 14: 'r10', 15: 'r10', 16: 'r10', 19: 'r10'},
            15: {0: 'r20', 1: 'r20', 2: 'r20', 3: 'r20', 4: 'r20', 5: 'r20', 6: 'r20', 7: 'r20', 8: 'r20', 9: 'r20', 10: 'r20', 11: 'r20', 13: 'r20', 14: 'r20', 15: 'r20', 16: 'r20', 19: 'r20'},
            16: {1: 'r8', 2: 'r8', 3: 'r8', 4: 'r8', 5: 'r8', 6: 'r8', 7: 'r8', 8: 'r8', 9: 'r8', 10: 'r8', 11: 'r8', 13: 'r8', 14: 'r8', 15: 'r8', 16: 'r8', 19: 'r8'},
            17: {1: 'r23', 2: 'r23', 3: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 8: 'r23', 9: 'r23', 10: 'r23', 11: 'r23', 13: 'r23', 15: 'r23', 16: 'r23', 19: 'r23'},
            18: {6: 'r4', 7: 'r4', 10: 'r4', 19: 'r4'},
            19: {6: 'r32', 7: 'r32', 10: 'r32', 19: 'r32'},
            20: {6: 's14', 7: 's16', 10: 's13', 19: 's15'},
            21: {6: 's14', 7: 's16', 10: 's13', 14: 's27', 19: 's15'},
            22: {6: 'r28', 7: 'r28', 10: 'r28', 14: 'r28', 19: 'r28'},
            23: {6: 'r13', 7: 'r13', 10: 'r13', 14: 'r13', 19: 'r13'},
            24: {0: 's25', 6: 'r23', 7: 'r23', 10: 'r23', 14: 'r23', 19: 'r23'},
            25: {6: 's14', 10: 's13', 19: 's15'},
            26: {6: 'r29', 7: 'r29', 10: 'r29', 14: 'r29', 19: 'r29'},
            27: {1: 'r33', 2: 'r33', 3: 'r33', 4: 'r33', 5: 'r33', 6: 'r33', 7: 'r33', 8: 'r33', 9: 'r33', 10: 'r33', 11: 'r33', 13: 'r33', 15: 'r33', 16: 'r33', 19: 'r33'},
            28: {6: 'r11', 7: 'r11', 10: 'r11', 14: 'r11', 19: 'r11'},
            29: {2: 's30'},
            30: {1: 'r24', 2: 'r24', 3: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 7: 'r24', 8: 'r24', 9: 'r24', 10: 'r24', 11: 'r24', 13: 'r24', 15: 'r24', 16: 'r24', 19: 'r24'},
            31: {1: 'r38', 2: 'r38', 6: 'r38', 7: 'r38', 8: 'r38', 9: 'r38', 10: 'r38', 11: 'r38', 15: 'r38', 16: 'r38', 19: 'r38'},
            32: {1: 'r3', 2: 'r3', 6: 'r3', 7: 'r3', 8: 'r3', 9: 'r3', 10: 'r3', 11: 'r3', 15: 'r3', 16: 'r3', 19: 'r3'},
            33: {1: 'r1', 2: 'r1', 6: 'r1', 7: 'r1', 8: 'r1', 9: 'r1', 10: 'r1', 11: 'r1', 15: 'r1', 16: 'r1', 19: 'r1'},
            34: {19: 's40'},
            35: {1: 'r14', 2: 'r14', 6: 'r14', 7: 'r14', 8: 'r14', 9: 'r14', 10: 'r14', 11: 'r14', 15: 'r14', 16: 'r14', 19: 'r14'},
            36: {1: 'r17', 2: 'r17', 6: 'r17', 7: 'r17', 8: 'r17', 9: 'r17', 10: 'r17', 11: 'r17', 15: 'r17', 16: 'r17', 19: 'r17'},
            37: {1: 'r19', 2: 'r19', 6: 'r19', 7: 'r19', 8: 'r19', 9: 'r19', 10: 'r19', 11: 'r19', 15: 'r19', 16: 'r19', 19: 'r19'},
            38: {12: 's42', 18: 's43'},
            39: {12: 'r27', 18: 'r27', 19: 's41'},
            40: {12: 'r36', 18: 'r36', 19: 'r36'},
            41: {12: 'r12', 18: 'r12', 19: 'r12'},
            42: {1: 'r7', 2: 'r7', 6: 'r7', 7: 'r7', 8: 'r7', 9: 'r7', 10: 'r7', 11: 'r7', 15: 'r7', 16: 'r7', 19: 'r7'},
            43: {12: 'r40', 19: 's40'},
            44: {12: 's47'},
            45: {12: 'r34'},
            46: {12: 'r15'},
            47: {1: 'r21', 2: 'r21', 6: 'r21', 7: 'r21', 8: 'r21', 9: 'r21', 10: 'r21', 11: 'r21', 15: 'r21', 16: 'r21', 19: 'r21'},
            48: {1: 'r35', 2: 'r35', 6: 'r35', 7: 'r35', 8: 'r35', 9: 'r35', 10: 'r35', 11: 'r35', 15: 'r35', 16: 'r35', 19: 'r35'},
            49: {2: 'r30', 11: 's50', 15: 'r30'},
            50: {1: 's12', 6: 's14', 7: 's16', 8: 's7', 9: 's10', 10: 's13', 16: 's11', 19: 's15'},
            51: {2: 'r41', 11: 'r41', 15: 'r41'},
            52: {2: 'r5', 11: 'r5', 15: 'r5'}
        }
        self.__sparse_goto_table: Dict[int, Dict[int, int]] = {
            0: {2: 9, 4: 17, 13: 3, 14: 4, 17: 5, 19: 8, 20: 6, 21: 1, 22: 2},
            3: {11: 49},
            4: {2: 9, 4: 17, 17: 48, 19: 8, 20: 6},
            6: {6: 32, 9: 36, 18: 31},
            11: {2: 9, 4: 17, 13: 3, 14: 4, 17: 5, 19: 8, 20: 6, 22: 29},
            12: {0: 18, 5: 20},
            20: {4: 24, 7: 21, 12: 22, 19: 23},
            21: {4: 24, 12: 28, 19: 23},
            25: {4: 26},
            34: {10: 38, 15: 39},
            43: {8: 44, 10: 46, 15: 39, 16: 45},
            49: {1: 51},
            50: {2: 9, 4: 17, 13: 52, 14: 4, 17: 5, 19: 8, 20: 6}
        }
        self.__sentence_index_grammar_tuple_mapping: Dict[int, Tuple[str, ...]] = {
            27: ('*0',),
            12: ('*0', '1'),
            7: ('1', '1'),
            21: ('1', '*3'),
            40: (),
            34: ('*0',),
            29: ('0', '2'),
            18: ('0',),
            24: ('1',),
            33: ('*1', '2'),
            11: ('*0', '1'),
            39: (),
            4: ('*0',),
            10: ('0',),
            2: (),
            37: ('0',),
            16: ('0',),
            17: ('0', '*1'),
            22: (),
            38: ('*0',),
            25: ('*0',),
            35: ('*0', '1'),
            30: ('0', '*1'),
            5: ('1',),
            31: (),
            41: ('*0', '*1'),
            9: ('0',)
        }
        self.__reduce_symbol_count: List[int] = [1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 5, 0, 1, 3, 1, 1, 1, 1, 3, 2, 0, 1, 4, 1, 2, 1, 1, 1, 0, 0, 2]
        self.__reduce_non_terminal_index: List[int] = [3, 6, 20, 18, 5, 1, 4, 6, 19, 21, 4, 7, 15, 12, 6, 16, 20, 17, 2, 6, 4, 6, 9, 19, 2, 13, 14, 10, 7, 12, 22, 11, 0, 2, 8, 14, 15, 20, 9, 5, 8, 11]

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
                    raise ValueError(f'Invalid goto action: state={current_state}, non-terminal={current_non_terminal_index}')
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
                elif statement_index in {0, 1, 32, 3, 36, 6, 8, 13, 14, 15, 19, 20, 23, 26, 28}:
                    grammar_node: BosonGrammarNode = BosonGrammarNode()
                    for _ in range(reduce_count):
                        grammar_node.insert(0, symbol_stack.pop())
                    grammar_node.set_reduce_number(statement_index)
                    symbol_stack.append(grammar_node)
                else:
                    raise ValueError(f'Invalid reduce number: reduce={statement_index}')
            elif operation_flag == 'a':
                grammar.grammar_tree = symbol_stack[0]
                return grammar
            else:
                raise ValueError(f'Invalid action: action={operation}')
        raise RuntimeError('Analyzer unusual exit.')
