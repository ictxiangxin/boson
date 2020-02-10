class RegularExpressionToken:
    text: str
    line: int
    symbol: str

    def __init__(self, text: str, line: int, symbol: str):
        self.text = text
        self.line = line
        self.symbol = symbol


class BosonGrammar:
    def __init__(self):
        self.__grammar_tree = None
        self.__error_index = None

    def get_grammar_tree(self):
        return self.__grammar_tree

    def set_grammar_tree(self, grammar_tree: tuple):
        self.__grammar_tree = grammar_tree

    grammar_tree = property(get_grammar_tree, set_grammar_tree)

    def get_error_index(self):
        return self.__error_index

    def set_error_index(self, error_index: int):
        self.__error_index = error_index

    error_index = property(get_error_index, set_error_index)


class BosonGrammarNode:
    def __init__(self):
        self.reduce_number = -1
        self.__data = []

    def __getitem__(self, item):
        return self.__data[item]

    def __iadd__(self, other):
        self.__data += other
        return self

    def append(self, item):
        self.__data.append(item)

    def insert(self, index, item):
        self.__data.insert(index, item)

    def data(self):
        return self.__data


class RegularExpressionAnalyzer:
    def __init__(self):
        self.__terminal_index = {
            'reverse': 0,
            'bracket_r': 1,
            'escape_character': 2,
            'star': 3,
            'brace_l': 4,
            'single_number': 5,
            'plus': 6,
            'parentheses_l': 7,
            'bracket_l': 8,
            'question_mark': 9,
            'to': 10,
            'or': 11,
            'normal_character': 12,
            'wildcard_character': 13,
            'brace_r': 14,
            'comma': 15,
            'parentheses_r': 16,
            '$': 17
        }
        self.__action_table = {
            0: {2: 's7', 5: 's1', 7: 's14', 8: 's13', 12: 's12', 13: 's11'},
            1: {1: 'r24', 2: 'r24', 3: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 7: 'r24', 8: 'r24', 9: 'r24', 10: 'r24', 11: 'r24', 12: 'r24', 13: 'r24', 16: 'r24', 17: 'r24'},
            2: {17: 'a'},
            3: {2: 'r27', 3: 'r27', 4: 'r27', 5: 'r27', 6: 'r27', 7: 'r27', 8: 'r27', 9: 'r27', 11: 'r27', 12: 'r27', 13: 'r27', 16: 'r27', 17: 'r27'},
            4: {2: 'r28', 3: 'r28', 4: 'r28', 5: 'r28', 6: 'r28', 7: 'r28', 8: 'r28', 9: 'r28', 11: 'r28', 12: 'r28', 13: 'r28', 16: 'r28', 17: 'r28'},
            5: {2: 'r10', 5: 'r10', 7: 'r10', 8: 'r10', 11: 'r10', 12: 'r10', 13: 'r10', 16: 'r10', 17: 'r10'},
            6: {17: 'r37'},
            7: {1: 'r41', 2: 'r41', 3: 'r41', 4: 'r41', 5: 'r41', 6: 'r41', 7: 'r41', 8: 'r41', 9: 'r41', 11: 'r41', 12: 'r41', 13: 'r41', 16: 'r41', 17: 'r41'},
            8: {11: 'r3', 16: 'r3', 17: 'r3'},
            9: {2: 's7', 5: 's1', 7: 's14', 8: 's13', 11: 'r22', 12: 's12', 13: 's11', 16: 'r22', 17: 'r22'},
            10: {2: 'r40', 3: 'r40', 4: 'r40', 5: 'r40', 6: 'r40', 7: 'r40', 8: 'r40', 9: 'r40', 11: 'r40', 12: 'r40', 13: 'r40', 16: 'r40', 17: 'r40'},
            11: {2: 'r29', 3: 'r29', 4: 'r29', 5: 'r29', 6: 'r29', 7: 'r29', 8: 'r29', 9: 'r29', 11: 'r29', 12: 'r29', 13: 'r29', 16: 'r29', 17: 'r29'},
            12: {1: 'r23', 2: 'r23', 3: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 8: 'r23', 9: 'r23', 10: 'r23', 11: 'r23', 12: 'r23', 13: 'r23', 16: 'r23', 17: 'r23'},
            13: {0: 's18', 2: 'r16', 5: 'r16', 12: 'r16'},
            14: {2: 's7', 5: 's1', 7: 's14', 8: 's13', 12: 's12', 13: 's11'},
            15: {2: 'r13', 3: 's28', 4: 's26', 5: 'r13', 6: 's27', 7: 'r13', 8: 'r13', 9: 's23', 11: 'r13', 12: 'r13', 13: 'r13', 16: 'r13', 17: 'r13'},
            16: {11: 's29', 16: 'r30', 17: 'r30'},
            17: {2: 'r9', 5: 'r9', 7: 'r9', 8: 'r9', 11: 'r9', 12: 'r9', 13: 'r9', 16: 'r9', 17: 'r9'},
            18: {2: 'r14', 5: 'r14', 12: 'r14'},
            19: {2: 's7', 5: 's1', 12: 's12'},
            20: {2: 'r15', 5: 'r15', 12: 'r15'},
            21: {16: 's35'},
            22: {2: 'r11', 5: 'r11', 7: 'r11', 8: 'r11', 11: 'r11', 12: 'r11', 13: 'r11', 16: 'r11', 17: 'r11'},
            23: {2: 'r35', 5: 'r35', 7: 'r35', 8: 'r35', 11: 'r35', 12: 'r35', 13: 'r35', 16: 'r35', 17: 'r35'},
            24: {2: 'r12', 5: 'r12', 7: 'r12', 8: 'r12', 11: 'r12', 12: 'r12', 13: 'r12', 16: 'r12', 17: 'r12'},
            25: {2: 'r31', 5: 'r31', 7: 'r31', 8: 'r31', 11: 'r31', 12: 'r31', 13: 'r31', 16: 'r31', 17: 'r31'},
            26: {5: 's36', 15: 'r21'},
            27: {2: 'r34', 5: 'r34', 7: 'r34', 8: 'r34', 11: 'r34', 12: 'r34', 13: 'r34', 16: 'r34', 17: 'r34'},
            28: {2: 'r36', 5: 'r36', 7: 'r36', 8: 'r36', 11: 'r36', 12: 'r36', 13: 'r36', 16: 'r36', 17: 'r36'},
            29: {2: 's7', 5: 's1', 7: 's14', 8: 's13', 12: 's12', 13: 's11'},
            30: {11: 'r2', 16: 'r2', 17: 'r2'},
            31: {1: 's42', 2: 's7', 5: 's1', 12: 's12'},
            32: {1: 'r18', 2: 'r18', 5: 'r18', 12: 'r18'},
            33: {1: 'r40', 2: 'r40', 5: 'r40', 10: 's44', 12: 'r40'},
            34: {1: 'r39', 2: 'r39', 5: 'r39', 12: 'r39'},
            35: {2: 'r26', 3: 'r26', 4: 'r26', 5: 'r26', 6: 'r26', 7: 'r26', 8: 'r26', 9: 'r26', 11: 'r26', 12: 'r26', 13: 'r26', 16: 'r26', 17: 'r26'},
            36: {5: 'r8', 14: 'r8', 15: 'r8'},
            37: {5: 's45', 14: 'r32', 15: 'r32'},
            38: {15: 'r19'},
            39: {15: 'r20'},
            40: {15: 's46'},
            41: {11: 'r1', 16: 'r1', 17: 'r1'},
            42: {2: 'r25', 3: 'r25', 4: 'r25', 5: 'r25', 6: 'r25', 7: 'r25', 8: 'r25', 9: 'r25', 11: 'r25', 12: 'r25', 13: 'r25', 16: 'r25', 17: 'r25'},
            43: {1: 'r17', 2: 'r17', 5: 'r17', 12: 'r17'},
            44: {5: 's1', 12: 's12'},
            45: {5: 'r7', 14: 'r7', 15: 'r7'},
            46: {5: 's36', 14: 'r6'},
            47: {1: 'r38', 2: 'r38', 5: 'r38', 12: 'r38'},
            48: {14: 's51'},
            49: {14: 'r5'},
            50: {14: 'r4'},
            51: {2: 'r33', 5: 'r33', 7: 'r33', 8: 'r33', 11: 'r33', 12: 'r33', 13: 'r33', 16: 'r33', 17: 'r33'}
        }
        self.__goto_table = {
            0: {1: 5, 3: 10, 9: 3, 12: 8, 13: 15, 14: 9, 15: 4, 18: 6, 20: 2},
            8: {8: 16},
            9: {1: 17, 3: 10, 9: 3, 13: 15, 15: 4},
            13: {10: 20, 22: 19},
            14: {1: 5, 3: 10, 9: 3, 12: 8, 13: 15, 14: 9, 15: 4, 18: 21},
            15: {11: 25, 17: 22, 19: 24},
            16: {16: 30},
            19: {3: 33, 4: 32, 15: 34, 21: 31},
            26: {2: 37, 5: 40, 6: 39, 7: 38},
            29: {1: 5, 3: 10, 9: 3, 12: 41, 13: 15, 14: 9, 15: 4},
            31: {3: 33, 4: 43, 15: 34},
            44: {3: 47},
            46: {0: 49, 2: 37, 7: 50, 24: 48}
        }
        self.__node_table = {
            36: ('0',),
            1: ('*0', '1'),
            2: (),
            29: ('0', ('*1', ('1',))),
            8: ('*0', '1'),
            21: ('*0',),
            12: (),
            30: ('0', ('*1', ('0',))),
            27: ('0',),
            26: ('0',),
            28: ('0',),
            15: (),
            16: ('*0', '1'),
            24: (('*1', ('0',)), '2'),
            25: ('1',),
            37: ('0', '2'),
            20: (),
            5: (),
            32: (('*1', ('0',)), ('*3', ('0',))),
            6: ('*0', '1'),
            31: ('*0',)
        }
        self.__reduce_symbol_sum = [2, 2, 0, 1, 1, 0, 2, 1, 2, 1, 1, 1, 0, 1, 1, 0, 2, 1, 1, 1, 0, 1, 1, 1, 4, 3, 1, 1, 1, 2, 2, 1, 5, 1, 1, 1, 1, 3, 1, 1, 1]
        self.__reduce_to_non_terminal_index = [16, 8, 8, 0, 24, 24, 2, 2, 14, 14, 19, 11, 11, 10, 22, 22, 21, 21, 6, 5, 5, 12, 3, 3, 9, 9, 13, 13, 13, 18, 1, 7, 17, 17, 17, 17, 20, 4, 4, 15, 15]

    def __generate_grammar_tuple(self, statement_index: int, node_tuple: tuple, symbol_package: list):
        grammar_node = BosonGrammarNode()
        for i in node_tuple:
            if isinstance(i, str):
                if i == '$':
                    grammar_node.append(statement_index)
                elif i == '?':
                    grammar_node += symbol_package
                else:
                    if symbol_package:
                        if i[0] == '*':
                            grammar_node += symbol_package[int(i[1:])]
                        else:
                            grammar_node.append(symbol_package[int(i)])
            else:
                if symbol_package:
                    if i[0][0] == '*':
                        for node in symbol_package[int(i[0][1:])]:
                            grammar_node += self.__generate_grammar_tuple(-1, i[1], node)
                    else:
                        for node in symbol_package[int(i[0])]:
                            grammar_node.append(self.__generate_grammar_tuple(-1, i[1], node))
        grammar_node.reduce_number = statement_index
        return grammar_node

    def grammar_analysis(self, token_list):
        grammar = BosonGrammar()
        analysis_stack = [0]
        symbol_stack = []
        token_index = 0
        while token_index < len(token_list):
            token = token_list[token_index]
            current_state = analysis_stack[-1]
            operation = self.__action_table.get(current_state, {}).get(self.__terminal_index[token.symbol], 'e')
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
                statement_index = int(operation[1:]) - 1
                reduce_sum = self.__reduce_symbol_sum[statement_index]
                for _ in range(reduce_sum):
                    analysis_stack.pop()
                current_state = analysis_stack[-1]
                current_non_terminal_index = self.__reduce_to_non_terminal_index[statement_index]
                goto_next_state = self.__goto_table.get(current_state, {}).get(current_non_terminal_index, -1)
                if goto_next_state == -1:
                    raise ValueError('Invalid goto action: state={}, non-terminal={}'.format(current_state, current_non_terminal_index))
                analysis_stack.append(goto_next_state)
                if statement_index in self.__node_table:
                    symbol_package = []
                    for _ in range(reduce_sum):
                        symbol_package.insert(0, symbol_stack.pop())
                    symbol_stack.append(self.__generate_grammar_tuple(statement_index, self.__node_table[statement_index], symbol_package))
                elif statement_index in [0, 3, 4, 7, 9, 10, 11, 13, 14, 17, 18, 19, 22, 23, 33, 34, 35, 38, 39, 40]:
                    grammar_node = BosonGrammarNode()
                    for _ in range(reduce_sum):
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


class RegularExpressionSemanticsAnalyzer:
    def __init__(self):
        self.__reduce_number_to_grammar_name = {
            36: 'regular_expression',
            29: 'expression',
            21: 'branch',
            30: 'group',
            27: 'simple_construct',
            26: 'complex_construct',
            28: 'wildcard_character',
            24: 'select',
            25: 'sub_expression',
            32: 'count_range',
            31: 'construct_number'
        }
        self.__reduce_number_to_grammar_number = {
            39: 7,
            40: 8,
            22: 9,
            23: 10,
            38: 13,
            37: 14,
            33: 15,
            35: 16,
            34: 17
        }
        self.__naive_reduce_number = {33, 34, 35, 36, 38, 39, 40, 22, 23, 26, 27, 28}
        self.__semantics_entity = {}

    @staticmethod
    def __default_semantics_entity(grammar_entity):
        return grammar_entity

    @staticmethod
    def __naive_semantics_entity(grammar_entity):
        if len(grammar_entity) == 0:
            return None
        elif len(grammar_entity) == 1:
            return grammar_entity[0]
        else:
            return grammar_entity

    def __semantics_analysis(self, grammar_tree: BosonGrammarNode):
        if grammar_tree.reduce_number in self.__reduce_number_to_grammar_name:
            grammar_name = self.__reduce_number_to_grammar_name[grammar_tree.reduce_number]
        elif grammar_tree.reduce_number in self.__reduce_number_to_grammar_number:
            grammar_name = '!grammar_{}'.format(self.__reduce_number_to_grammar_number[grammar_tree.reduce_number])
        else:
            grammar_name = '!grammar_hidden'
        grammar_entity = list(map(lambda g: self.__semantics_analysis(g) if isinstance(g, BosonGrammarNode) else g, grammar_tree.data()))
        if grammar_name in self.__semantics_entity:
            return self.__semantics_entity[grammar_name](grammar_entity)
        elif grammar_tree.reduce_number in self.__naive_reduce_number:
            return self.__naive_semantics_entity(grammar_entity)
        else:
            return self.__default_semantics_entity(grammar_entity)

    def semantics_analysis(self, grammar_tree: BosonGrammarNode):
        return self.__semantics_analysis(grammar_tree)

    def semantics_entity(self, sign):
        def decorator(f):
            if isinstance(sign, int):
                name = '!grammar_{}'.format(sign)
            elif isinstance(sign, str):
                name = sign
            else:
                raise ValueError('Invalid grammar sign: {}'.format(sign))
            self.__semantics_entity[name] = f
            return f
        return decorator
