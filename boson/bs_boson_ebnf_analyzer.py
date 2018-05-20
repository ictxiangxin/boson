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


class BosonEBNFAnalyzer:
    def __init__(self):
        self.__terminal_index = {
            'bracket_l': 0,
            '$': 1,
            'or': 2,
            'parentheses_l': 3,
            'name': 4,
            'bracket_r': 5,
            'command': 6,
            'end': 7,
            'literal': 8,
            'plus': 9,
            'star': 10,
            'parentheses_r': 11,
            'comma': 12,
            'reduce': 13,
            'assign': 14,
            'null': 15,
            'node': 16
        }
        self.__action_table = {
            0: {4: 's4', 6: 's1'},
            1: {4: 's11', 8: 's10'},
            2: {1: 'r52', 4: 's4', 6: 's1'},
            3: {1: 'r2', 4: 'r2', 6: 'r2'},
            4: {13: 's14'},
            5: {1: 'r57', 4: 'r57', 6: 'r57'},
            6: {1: 'r58', 4: 'r58', 6: 'r58'},
            7: {1: 'a'},
            8: {4: 'r28', 7: 'r28', 8: 'r28'},
            9: {4: 'r20', 7: 'r20', 8: 'r20'},
            10: {4: 'r3', 7: 'r3', 8: 'r3'},
            11: {4: 'r4', 7: 'r4', 8: 'r4'},
            12: {4: 's11', 7: 's16', 8: 's10'},
            13: {1: 'r1', 4: 'r1', 6: 'r1'},
            14: {0: 's22', 2: 'r47', 3: 's21', 4: 's19', 7: 'r47', 8: 's27', 14: 'r47', 15: 's23'},
            15: {4: 'r29', 7: 'r29', 8: 'r29'},
            16: {1: 'r41', 4: 'r41', 6: 'r41'},
            17: {0: 'r6', 2: 'r6', 3: 'r6', 4: 'r6', 7: 'r6', 8: 'r6', 14: 'r6'},
            18: {2: 'r32', 7: 'r32'},
            19: {0: 'r18', 2: 'r18', 3: 'r18', 4: 'r18', 5: 'r18', 7: 'r18', 8: 'r18', 9: 's30', 10: 's29', 11: 'r18', 14: 'r18'},
            20: {0: 's22', 2: 'r45', 3: 's21', 4: 's19', 7: 'r45', 8: 's27', 14: 'r45'},
            21: {0: 's22', 3: 's21', 4: 's19', 8: 's27'},
            22: {0: 's22', 3: 's21', 4: 's19', 8: 's27'},
            23: {2: 'r46', 7: 'r46', 14: 'r46'},
            24: {2: 'r38', 7: 'r38', 14: 's41'},
            25: {7: 's42'},
            26: {0: 'r49', 2: 'r49', 3: 'r49', 4: 'r49', 5: 'r49', 7: 'r49', 8: 'r49', 11: 'r49', 14: 'r49'},
            27: {0: 'r50', 2: 'r50', 3: 'r50', 4: 'r50', 5: 'r50', 7: 'r50', 8: 'r50', 11: 'r50', 14: 'r50'},
            28: {2: 's43', 7: 'r48'},
            29: {0: 'r40', 2: 'r40', 3: 'r40', 4: 'r40', 5: 'r40', 7: 'r40', 8: 'r40', 11: 'r40', 14: 'r40'},
            30: {0: 'r39', 2: 'r39', 3: 'r39', 4: 'r39', 5: 'r39', 7: 'r39', 8: 'r39', 11: 'r39', 14: 'r39'},
            31: {0: 'r16', 2: 'r16', 3: 'r16', 4: 'r16', 5: 'r16', 7: 'r16', 8: 'r16', 11: 'r16', 14: 'r16'},
            32: {0: 'r17', 2: 'r17', 3: 'r17', 4: 'r17', 5: 'r17', 7: 'r17', 8: 'r17', 11: 'r17', 14: 'r17'},
            33: {0: 'r51', 2: 'r51', 3: 'r51', 4: 'r51', 5: 'r51', 7: 'r51', 8: 'r51', 11: 'r51', 14: 'r51'},
            34: {0: 'r5', 2: 'r5', 3: 'r5', 4: 'r5', 7: 'r5', 8: 'r5', 14: 'r5'},
            35: {0: 's22', 3: 's21', 4: 's19', 5: 'r59', 8: 's27', 11: 'r59'},
            36: {11: 's46'},
            37: {0: 'r24', 2: 's49', 3: 'r24', 4: 'r24', 5: 'r24', 8: 'r24', 11: 'r24'},
            38: {5: 's50'},
            39: {2: 'r37', 7: 'r37'},
            40: {2: 'r44', 7: 'r44'},
            41: {3: 'r35', 4: 's52'},
            42: {1: 'r56', 4: 'r56', 6: 'r56'},
            43: {0: 's22', 2: 'r47', 3: 's21', 4: 's19', 7: 'r47', 8: 's27', 14: 'r47', 15: 's23'},
            44: {2: 'r31', 7: 'r31'},
            45: {0: 'r23', 3: 'r23', 4: 'r23', 5: 'r23', 8: 'r23', 11: 'r23'},
            46: {0: 'r22', 2: 'r22', 3: 'r22', 4: 'r22', 5: 'r22', 7: 'r22', 8: 'r22', 9: 's30', 10: 's29', 11: 'r22', 14: 'r22'},
            47: {2: 's49', 5: 'r60', 11: 'r60'},
            48: {2: 'r26', 5: 'r26', 11: 'r26'},
            49: {0: 's22', 3: 's21', 4: 's19', 8: 's27'},
            50: {0: 'r42', 2: 'r42', 3: 'r42', 4: 'r42', 5: 'r42', 7: 'r42', 8: 'r42', 11: 'r42', 14: 'r42'},
            51: {3: 's60'},
            52: {3: 'r33'},
            53: {3: 'r34'},
            54: {2: 'r30', 7: 'r30'},
            55: {0: 'r19', 2: 'r19', 3: 'r19', 4: 'r19', 5: 'r19', 7: 'r19', 8: 'r19', 11: 'r19', 14: 'r19'},
            56: {0: 'r21', 2: 'r21', 3: 'r21', 4: 'r21', 5: 'r21', 7: 'r21', 8: 'r21', 11: 'r21', 14: 'r21'},
            57: {0: 'r43', 2: 'r43', 3: 'r43', 4: 'r43', 5: 'r43', 7: 'r43', 8: 'r43', 11: 'r43', 14: 'r43'},
            58: {2: 'r27', 5: 'r27', 11: 'r27'},
            59: {2: 'r25', 5: 'r25', 11: 'r25'},
            60: {10: 's65', 16: 'r12'},
            61: {2: 'r36', 7: 'r36'},
            62: {11: 's67'},
            63: {16: 's68'},
            64: {16: 'r11'},
            65: {16: 'r10'},
            66: {11: 'r9', 12: 'r9'},
            67: {2: 'r53', 7: 'r53', 11: 'r53', 12: 'r53'},
            68: {3: 's60', 11: 'r15', 12: 'r15'},
            69: {11: 'r55', 12: 's73'},
            70: {11: 'r14', 12: 'r14'},
            71: {11: 'r13', 12: 'r13'},
            72: {11: 'r54', 12: 'r54'},
            73: {10: 's65', 16: 'r12'},
            74: {11: 'r8', 12: 'r8'},
            75: {11: 'r7', 12: 'r7'}
        }
        self.__goto_table = {
            0: {12: 7, 13: 3, 19: 6, 32: 2, 36: 5},
            1: {10: 8, 18: 9, 27: 12},
            2: {13: 13, 19: 6, 36: 5},
            12: {10: 15, 18: 9},
            14: {3: 26, 9: 25, 15: 20, 31: 24, 33: 17, 35: 18},
            18: {37: 28},
            19: {7: 32, 22: 33, 28: 31},
            20: {3: 26, 33: 34},
            21: {3: 26, 14: 36, 16: 35, 33: 37},
            22: {3: 26, 14: 38, 16: 35, 33: 37},
            24: {30: 40, 38: 39},
            28: {21: 44},
            35: {3: 26, 33: 45},
            37: {4: 47, 34: 48},
            41: {8: 53, 23: 51},
            43: {3: 26, 15: 20, 31: 24, 33: 17, 35: 54},
            46: {2: 56, 26: 57, 28: 55},
            47: {34: 58},
            49: {3: 26, 33: 59},
            51: {25: 61},
            60: {5: 64, 11: 63, 24: 66, 29: 62},
            66: {6: 69},
            68: {0: 70, 1: 72, 25: 71},
            69: {20: 74},
            73: {5: 64, 11: 63, 24: 75}
        }
        self.__node_table = {
            0: ('*0', '1'),
            28: ('*0', '1'),
            40: ('0', ('*1', ('?',))),
            55: ('0', '2'),
            30: ('*0', '1'),
            31: (),
            47: ('0', ('*1', ('1',))),
            34: (),
            37: (),
            43: ('0', ('*1', (('*1', ('?',)), '2'))),
            4: ('*0', '1'),
            44: ('*0',),
            52: ('*1',),
            7: ('*0', '1'),
            8: (),
            54: ('0', ('*1', ('1',))),
            11: (),
            14: (),
            53: (('*0', ('?',)), '1', ('*2', ('?',))),
            17: (),
            50: ('0', ('*1', ('?',))),
            49: ('0',),
            21: (),
            42: ('1', ('*3', ('?',))),
            41: ('1',),
            22: ('*0', '1'),
            26: ('*0', '1'),
            58: ('*0',),
            59: ('0', ('*1', ('1',)))
        }
        self.__reduce_symbol_sum = [2, 1, 1, 1, 2, 1, 2, 2, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 2, 1, 2, 1, 2, 1, 2, 2, 2, 0, 1, 1, 0, 3, 1, 0, 1, 1, 3, 3, 4, 2, 1, 1, 0, 2, 1, 1, 2, 1, 3, 3, 2, 4, 1, 1, 1, 2]
        self.__reduce_to_non_terminal_index = [32, 32, 18, 18, 15, 15, 20, 6, 6, 5, 11, 11, 0, 1, 1, 7, 22, 22, 2, 10, 26, 26, 16, 16, 34, 4, 4, 27, 27, 21, 37, 37, 8, 23, 23, 38, 30, 30, 28, 28, 36, 3, 3, 35, 31, 31, 31, 9, 33, 33, 33, 12, 25, 24, 29, 19, 13, 13, 14, 14]

    def __generate_grammar_tuple(self, statement_index, symbol_package):
        grammar_node = BosonGrammarNode()
        if isinstance(statement_index, int):
            node_tuple = self.__node_table[statement_index]
        else:
            node_tuple = statement_index
            statement_index = -1
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
                            grammar_node += self.__generate_grammar_tuple(i[1], node)
                    else:
                        for node in symbol_package[int(i[0])]:
                            grammar_node.append(self.__generate_grammar_tuple(i[1], node))
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
                    symbol_stack.append(self.__generate_grammar_tuple(statement_index, symbol_package))
                elif statement_index in [1, 2, 3, 5, 6, 9, 10, 12, 13, 15, 16, 18, 19, 20, 23, 24, 25, 27, 29, 32, 33, 35, 36, 38, 39, 45, 46, 48, 51, 56, 57]:
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


class BosonSemanticsAnalyzer:
    def __init__(self):
        self.__reduce_number_to_grammar_name = {
            40: 'command',
            55: 'reduce',
            53: 'grammar_node',
            50: 'name_closure',
            49: 'literal',
            42: 'complex_closure',
            41: 'complex_optional',
            59: 'select'
        }
        self.__reduce_number_to_grammar_number = {
            51: 0,
            56: 1,
            57: 2,
            47: 5,
            43: 6,
            44: 7,
            45: 8,
            46: 9,
            52: 10,
            54: 11,
            48: 13,
            58: 18,
            38: 20,
            39: 21
        }
        self.__naive_reduce_number = {2, 3, 38, 39, 45, 46, 48, 49, 56, 57}
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
            grammar_name = '!grammar_{}'.format('hidden')
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
