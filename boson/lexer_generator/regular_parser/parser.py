from typing import Dict, List, Tuple

from .token import RegularToken
from .grammar_node import BosonGrammarNode
from .grammar import BosonGrammar


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: Dict[str, int] = {
            '!symbol_2': 0,
            '!symbol_5': 1,
            '!symbol_8': 2,
            '!symbol_1': 3,
            '!symbol_13': 4,
            '!symbol_6': 5,
            'reference': 6,
            '!symbol_12': 7,
            '!symbol_7': 8,
            '!symbol_10': 9,
            '!symbol_17': 10,
            '!symbol_18': 11,
            '!symbol_4': 12,
            '!symbol_14': 13,
            '!symbol_15': 14,
            '!symbol_9': 15,
            '!symbol_3': 16,
            '!symbol_16': 17,
            '$': 18,
            '!symbol_11': 19
        }
        self.__sparse_action_table: Dict[int, Dict[int, str]] = {
            0: {0: 's8', 1: 's15', 5: 's13', 6: 's11', 8: 's10', 9: 's12', 12: 's14', 16: 's16'},
            1: {18: 'a'},
            2: {18: 'r16'},
            3: {3: 'r6', 18: 'r6', 19: 'r6'},
            4: {0: 's8', 1: 's15', 3: 'r37', 5: 's13', 6: 's11', 8: 's10', 9: 's12', 12: 's14', 16: 's16', 18: 'r37', 19: 'r37'},
            5: {0: 'r28', 1: 'r28', 3: 'r28', 5: 'r28', 6: 'r28', 8: 'r28', 9: 'r28', 12: 'r28', 16: 'r28', 18: 'r28', 19: 'r28'},
            6: {0: 'r10', 1: 'r10', 3: 'r10', 4: 's33', 5: 'r10', 6: 'r10', 8: 'r10', 9: 'r10', 12: 'r10', 13: 's32', 14: 's34', 16: 'r10', 17: 's31', 18: 'r10', 19: 'r10'},
            7: {0: 'r2', 1: 'r2', 3: 'r2', 4: 'r2', 5: 'r2', 6: 'r2', 8: 'r2', 9: 'r2', 12: 'r2', 13: 'r2', 14: 'r2', 16: 'r2', 17: 'r2', 18: 'r2', 19: 'r2'},
            8: {0: 'r7', 1: 'r7', 3: 'r7', 4: 'r7', 5: 'r7', 6: 'r7', 8: 'r7', 9: 'r7', 12: 'r7', 13: 'r7', 14: 'r7', 16: 'r7', 17: 'r7', 18: 'r7', 19: 'r7'},
            9: {0: 'r20', 1: 'r20', 3: 'r20', 4: 'r20', 5: 'r20', 6: 'r20', 8: 'r20', 9: 'r20', 12: 'r20', 13: 'r20', 14: 'r20', 16: 'r20', 17: 'r20', 18: 'r20', 19: 'r20'},
            10: {1: 'r1', 2: 's21', 5: 'r1', 12: 'r1', 16: 'r1'},
            11: {0: 'r21', 1: 'r21', 3: 'r21', 4: 'r21', 5: 'r21', 6: 'r21', 8: 'r21', 9: 'r21', 12: 'r21', 13: 'r21', 14: 'r21', 16: 'r21', 17: 'r21', 18: 'r21', 19: 'r21'},
            12: {0: 's8', 1: 's15', 5: 's13', 6: 's11', 8: 's10', 9: 's12', 12: 's14', 16: 's16'},
            13: {0: 'r8', 1: 'r8', 3: 'r8', 4: 'r8', 5: 'r8', 6: 'r8', 7: 'r8', 8: 'r8', 9: 'r8', 12: 'r8', 13: 'r8', 14: 'r8', 15: 'r8', 16: 'r8', 17: 'r8', 18: 'r8', 19: 'r8'},
            14: {0: 'r23', 1: 'r23', 3: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 8: 'r23', 9: 'r23', 12: 'r23', 13: 'r23', 14: 'r23', 15: 'r23', 16: 'r23', 17: 'r23', 18: 'r23', 19: 'r23'},
            15: {0: 'r32', 1: 'r32', 3: 'r32', 4: 'r32', 5: 'r32', 6: 'r32', 7: 'r32', 8: 'r32', 9: 'r32', 12: 'r32', 13: 'r32', 14: 'r32', 15: 'r32', 16: 'r32', 17: 'r32', 18: 'r32', 19: 'r32'},
            16: {0: 'r15', 1: 'r15', 3: 'r15', 4: 'r15', 5: 'r15', 6: 'r15', 8: 'r15', 9: 'r15', 12: 'r15', 13: 'r15', 14: 'r15', 15: 'r15', 16: 'r15', 17: 'r15', 18: 'r15', 19: 'r15'},
            17: {0: 'r33', 1: 'r33', 3: 'r33', 4: 'r33', 5: 'r33', 6: 'r33', 8: 'r33', 9: 'r33', 12: 'r33', 13: 'r33', 14: 'r33', 16: 'r33', 17: 'r33', 18: 'r33', 19: 'r33'},
            18: {19: 's19'},
            19: {0: 'r29', 1: 'r29', 3: 'r29', 4: 'r29', 5: 'r29', 6: 'r29', 8: 'r29', 9: 'r29', 12: 'r29', 13: 'r29', 14: 'r29', 16: 'r29', 17: 'r29', 18: 'r29', 19: 'r29'},
            20: {1: 's15', 5: 's13', 12: 's14', 16: 's16'},
            21: {1: 'r27', 5: 'r27', 12: 'r27', 16: 'r27'},
            22: {1: 's15', 5: 's13', 12: 's14', 15: 's28', 16: 's16'},
            23: {1: 'r19', 5: 'r19', 12: 'r19', 15: 'r19', 16: 'r19'},
            24: {1: 'r30', 5: 'r30', 12: 'r30', 15: 'r30', 16: 'r30'},
            25: {1: 'r33', 5: 'r33', 7: 's26', 12: 'r33', 15: 'r33', 16: 'r33'},
            26: {1: 's15', 5: 's13', 12: 's14'},
            27: {1: 'r31', 5: 'r31', 12: 'r31', 15: 'r31', 16: 'r31'},
            28: {0: 'r17', 1: 'r17', 3: 'r17', 4: 'r17', 5: 'r17', 6: 'r17', 8: 'r17', 9: 'r17', 12: 'r17', 13: 'r17', 14: 'r17', 16: 'r17', 17: 'r17', 18: 'r17', 19: 'r17'},
            29: {1: 'r25', 5: 'r25', 12: 'r25', 15: 'r25', 16: 'r25'},
            30: {0: 'r12', 1: 'r12', 3: 'r12', 5: 'r12', 6: 'r12', 8: 'r12', 9: 'r12', 12: 'r12', 16: 'r12', 18: 'r12', 19: 'r12'},
            31: {5: 's38'},
            32: {0: 'r26', 1: 'r26', 3: 'r26', 5: 'r26', 6: 'r26', 8: 'r26', 9: 'r26', 12: 'r26', 16: 'r26', 18: 'r26', 19: 'r26'},
            33: {0: 'r34', 1: 'r34', 3: 'r34', 5: 'r34', 6: 'r34', 8: 'r34', 9: 'r34', 12: 'r34', 16: 'r34', 18: 'r34', 19: 'r34'},
            34: {0: 'r36', 1: 'r36', 3: 'r36', 5: 'r36', 6: 'r36', 8: 'r36', 9: 'r36', 12: 'r36', 16: 'r36', 18: 'r36', 19: 'r36'},
            35: {0: 'r13', 1: 'r13', 3: 'r13', 5: 'r13', 6: 'r13', 8: 'r13', 9: 'r13', 12: 'r13', 16: 'r13', 18: 'r13', 19: 'r13'},
            36: {10: 's41', 11: 's40'},
            37: {5: 's39', 10: 'r18', 11: 'r18'},
            38: {5: 'r5', 10: 'r5', 11: 'r5'},
            39: {5: 'r4', 10: 'r4', 11: 'r4'},
            40: {0: 'r22', 1: 'r22', 3: 'r22', 5: 'r22', 6: 'r22', 8: 'r22', 9: 'r22', 12: 'r22', 16: 'r22', 18: 'r22', 19: 'r22'},
            41: {5: 's38', 11: 'r24'},
            42: {11: 'r35'},
            43: {11: 's44'},
            44: {0: 'r11', 1: 'r11', 3: 'r11', 5: 'r11', 6: 'r11', 8: 'r11', 9: 'r11', 12: 'r11', 16: 'r11', 18: 'r11', 19: 'r11'},
            45: {0: 'r9', 1: 'r9', 3: 'r9', 5: 'r9', 6: 'r9', 8: 'r9', 9: 'r9', 12: 'r9', 16: 'r9', 18: 'r9', 19: 'r9'},
            46: {3: 's48', 18: 'r38', 19: 'r38'},
            47: {3: 'r14', 18: 'r14', 19: 'r14'},
            48: {0: 's8', 1: 's15', 5: 's13', 6: 's11', 8: 's10', 9: 's12', 12: 's14', 16: 's16'},
            49: {3: 'r3', 18: 'r3', 19: 'r3'}
        }
        self.__sparse_goto_table: Dict[int, Dict[int, int]] = {
            0: {1: 6, 2: 1, 5: 17, 8: 2, 9: 3, 11: 5, 16: 9, 18: 4, 19: 7},
            3: {4: 46},
            4: {1: 6, 5: 17, 11: 45, 16: 9, 19: 7},
            6: {0: 35, 7: 30},
            10: {6: 20},
            12: {1: 6, 5: 17, 8: 18, 9: 3, 11: 5, 16: 9, 18: 4, 19: 7},
            20: {5: 25, 10: 23, 17: 22, 19: 24},
            22: {5: 25, 10: 29, 19: 24},
            26: {5: 27},
            31: {13: 37, 15: 36},
            41: {13: 37, 14: 43, 15: 42},
            46: {12: 47},
            48: {1: 6, 5: 17, 9: 49, 11: 5, 16: 9, 18: 4, 19: 7}
        }
        self.__sentence_index_grammar_tuple_mapping: Dict[int, Tuple[str, ...]] = {
            18: ('*0',),
            4: ('*0', '1'),
            22: ('1', '1'),
            11: ('1', '*3'),
            24: (),
            35: ('0',),
            31: ('0', '2'),
            21: ('0',),
            29: ('1',),
            17: ('*1', '2'),
            25: ('*0', '1'),
            1: (),
            27: ('0',),
            32: ('0',),
            7: (),
            20: ('0',),
            2: ('0',),
            13: ('0', '*1'),
            10: (),
            12: ('0',),
            37: ('*0',),
            9: ('*0', '1'),
            38: ('0', '*1'),
            3: ('1',),
            6: (),
            14: ('*0', '*1'),
            16: ('0',)
        }
        self.__reduce_symbol_count: List[int] = [1, 0, 1, 2, 2, 1, 0, 1, 1, 2, 0, 5, 1, 2, 2, 1, 1, 4, 1, 1, 1, 1, 3, 1, 0, 2, 1, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1, 2]
        self.__reduce_non_terminal_index: List[int] = [3, 6, 1, 12, 13, 13, 4, 1, 5, 18, 0, 7, 0, 11, 4, 19, 2, 16, 15, 17, 1, 16, 7, 5, 14, 17, 7, 6, 18, 16, 10, 10, 5, 19, 7, 14, 7, 9, 8]

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
                elif statement_index in {0, 33, 34, 36, 5, 8, 15, 19, 23, 26, 28, 30}:
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
