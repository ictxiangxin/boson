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
            'literal': 0,
            'command': 1,
            'star': 2,
            'or': 3,
            'parentheses_l': 4,
            'comma': 5,
            'assign': 6,
            'parentheses_r': 7,
            'node': 8,
            'plus': 9,
            'reduce': 10,
            '$': 11,
            'end': 12,
            'name': 13,
            'bracket_r': 14,
            'bracket_l': 15,
            'null': 16
        }
        self.__action_table = {
            0: {1: 's6', 13: 's7'},
            1: {1: 's6', 11: 'r50', 13: 's7'},
            2: {11: 'a'},
            3: {1: 'r55', 11: 'r55', 13: 'r55'},
            4: {1: 'r56', 11: 'r56', 13: 'r56'},
            5: {1: 'r2', 11: 'r2', 13: 'r2'},
            6: {0: 's10', 13: 's11'},
            7: {10: 's13'},
            8: {1: 'r1', 11: 'r1', 13: 'r1'},
            9: {0: 's10', 12: 's14', 13: 's11'},
            10: {0: 'r35', 12: 'r35', 13: 'r35'},
            11: {0: 'r36', 12: 'r36', 13: 'r36'},
            12: {0: 'r4', 12: 'r4', 13: 'r4'},
            13: {0: 's16', 3: 'r45', 4: 's21', 6: 'r45', 12: 'r45', 13: 's18', 15: 's22', 16: 's26'},
            14: {1: 'r39', 11: 'r39', 13: 'r39'},
            15: {0: 'r3', 12: 'r3', 13: 'r3'},
            16: {0: 'r48', 3: 'r48', 4: 'r48', 6: 'r48', 7: 'r48', 12: 'r48', 13: 'r48', 14: 'r48', 15: 'r48'},
            17: {3: 'r31', 6: 's29', 12: 'r31'},
            18: {0: 'r15', 2: 's31', 3: 'r15', 4: 'r15', 6: 'r15', 7: 'r15', 9: 's34', 12: 'r15', 13: 'r15', 14: 'r15', 15: 'r15'},
            19: {0: 'r33', 3: 'r33', 4: 'r33', 6: 'r33', 12: 'r33', 13: 'r33', 15: 'r33'},
            20: {0: 'r47', 3: 'r47', 4: 'r47', 6: 'r47', 7: 'r47', 12: 'r47', 13: 'r47', 14: 'r47', 15: 'r47'},
            21: {0: 's16', 4: 's21', 13: 's18', 15: 's22'},
            22: {0: 's16', 4: 's21', 13: 's18', 15: 's22'},
            23: {3: 'r25', 12: 'r25'},
            24: {12: 's40'},
            25: {0: 's16', 3: 'r43', 4: 's21', 6: 'r43', 12: 'r43', 13: 's18', 15: 's22'},
            26: {3: 'r44', 6: 'r44', 12: 'r44'},
            27: {3: 'r42', 12: 'r42'},
            28: {3: 'r30', 12: 'r30'},
            29: {4: 'r28', 13: 's42'},
            30: {0: 'r49', 3: 'r49', 4: 'r49', 6: 'r49', 7: 'r49', 12: 'r49', 13: 'r49', 14: 'r49', 15: 'r49'},
            31: {0: 'r38', 3: 'r38', 4: 'r38', 6: 'r38', 7: 'r38', 12: 'r38', 13: 'r38', 14: 'r38', 15: 'r38'},
            32: {0: 'r14', 3: 'r14', 4: 'r14', 6: 'r14', 7: 'r14', 12: 'r14', 13: 'r14', 14: 'r14', 15: 'r14'},
            33: {0: 'r13', 3: 'r13', 4: 'r13', 6: 'r13', 7: 'r13', 12: 'r13', 13: 'r13', 14: 'r13', 15: 'r13'},
            34: {0: 'r37', 3: 'r37', 4: 'r37', 6: 'r37', 7: 'r37', 12: 'r37', 13: 'r37', 14: 'r37', 15: 'r37'},
            35: {0: 's16', 4: 's21', 7: 's46', 13: 's18', 15: 's22'},
            36: {0: 'r17', 4: 'r17', 7: 'r17', 13: 'r17', 15: 'r17'},
            37: {0: 'r23', 4: 'r23', 13: 'r23', 14: 'r23', 15: 'r23'},
            38: {0: 's16', 4: 's21', 13: 's18', 14: 's48', 15: 's22'},
            39: {3: 's50', 12: 'r46'},
            40: {1: 'r54', 11: 'r54', 13: 'r54'},
            41: {0: 'r32', 3: 'r32', 4: 'r32', 6: 'r32', 12: 'r32', 13: 'r32', 15: 'r32'},
            42: {4: 'r26'},
            43: {4: 'r27'},
            44: {4: 's52'},
            45: {0: 'r16', 4: 'r16', 7: 'r16', 13: 'r16', 15: 'r16'},
            46: {0: 'r20', 2: 's31', 3: 'r20', 4: 'r20', 6: 'r20', 7: 'r20', 9: 's34', 12: 'r20', 13: 'r20', 14: 'r20', 15: 'r20'},
            47: {0: 'r22', 4: 'r22', 13: 'r22', 14: 'r22', 15: 'r22'},
            48: {0: 'r40', 3: 'r40', 4: 'r40', 6: 'r40', 7: 'r40', 12: 'r40', 13: 'r40', 14: 'r40', 15: 'r40'},
            49: {3: 'r24', 12: 'r24'},
            50: {0: 's16', 3: 'r45', 4: 's21', 6: 'r45', 12: 'r45', 13: 's18', 15: 's22', 16: 's26'},
            51: {3: 'r29', 12: 'r29'},
            52: {2: 's57', 8: 'r9'},
            53: {0: 'r41', 3: 'r41', 4: 'r41', 6: 'r41', 7: 'r41', 12: 'r41', 13: 'r41', 14: 'r41', 15: 'r41'},
            54: {0: 'r19', 3: 'r19', 4: 'r19', 6: 'r19', 7: 'r19', 12: 'r19', 13: 'r19', 14: 'r19', 15: 'r19'},
            55: {0: 'r18', 3: 'r18', 4: 'r18', 6: 'r18', 7: 'r18', 12: 'r18', 13: 'r18', 14: 'r18', 15: 'r18'},
            56: {3: 'r21', 12: 'r21'},
            57: {8: 'r7'},
            58: {8: 'r8'},
            59: {5: 'r6', 7: 'r6'},
            60: {8: 's63'},
            61: {7: 's64'},
            62: {5: 's66', 7: 'r53'},
            63: {4: 's52', 5: 'r12', 7: 'r12'},
            64: {3: 'r51', 5: 'r51', 7: 'r51', 12: 'r51'},
            65: {5: 'r5', 7: 'r5'},
            66: {2: 's57', 8: 'r9'},
            67: {5: 'r10', 7: 'r10'},
            68: {5: 'r11', 7: 'r11'},
            69: {5: 'r52', 7: 'r52'},
            70: {5: 'r34', 7: 'r34'}
        }
        self.__goto_table = {
            0: {3: 2, 19: 3, 24: 4, 28: 5, 34: 1},
            1: {19: 3, 24: 4, 28: 8},
            6: {8: 12, 25: 9},
            9: {8: 15},
            13: {5: 20, 6: 19, 14: 17, 20: 25, 31: 23, 32: 24},
            17: {9: 27, 17: 28},
            18: {4: 32, 11: 33, 16: 30},
            21: {5: 20, 6: 36, 13: 35},
            22: {5: 20, 6: 37, 23: 38},
            23: {10: 39},
            25: {5: 20, 6: 41},
            29: {12: 44, 18: 43},
            35: {5: 20, 6: 45},
            38: {5: 20, 6: 47},
            39: {15: 49},
            44: {1: 51},
            46: {11: 55, 27: 54, 29: 53},
            50: {5: 20, 6: 19, 14: 17, 20: 25, 31: 56},
            52: {2: 60, 7: 58, 22: 61, 26: 59},
            59: {21: 62},
            62: {0: 65},
            63: {1: 67, 30: 69, 35: 68},
            66: {2: 60, 7: 58, 26: 70}
        }
        self.__node_table = {
            0: ('*0', '1'),
            1: ('0',),
            49: ('*0',),
            2: ('*0', '1'),
            3: ('0',),
            38: ('0', '*1'),
            53: ('0', '2'),
            20: ('?',),
            23: ('*0', '1'),
            24: (),
            45: ('0', ('*1', ('1',))),
            25: ('?',),
            26: ('0',),
            27: (),
            28: ('?',),
            29: ('0',),
            30: (),
            41: ('0', ('*1', (('*1', ('?',)), '2'))),
            31: ('*0', '1'),
            32: ('0',),
            42: ('*0',),
            50: ('*1',),
            33: ('?',),
            4: ('*0', '1'),
            5: (),
            52: ('0', ('*1', ('1',))),
            6: ('?',),
            7: ('0',),
            8: (),
            9: ('?',),
            10: ('0',),
            11: (),
            51: (('*0', ('?',)), '1', ('*2', ('?',))),
            12: ('?',),
            13: ('0',),
            14: (),
            48: ('0', ('*1', ('?',))),
            47: ('0',),
            15: ('*0', '1'),
            16: ('0',),
            17: ('?',),
            18: ('0',),
            19: (),
            21: ('*0', '1'),
            22: ('0',),
            40: ('*1', ('*3', ('?',))),
            39: ('*1',)
        }
        self.__reduce_symbol_sum = [2, 1, 2, 1, 2, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 2, 1, 1, 1, 0, 2, 2, 1, 2, 0, 1, 1, 0, 3, 1, 0, 2, 1, 2, 1, 1, 1, 1, 3, 3, 4, 2, 1, 1, 0, 2, 1, 1, 2, 1, 3, 3, 2, 4, 1, 1]
        self.__reduce_to_non_terminal_index = [34, 34, 25, 25, 21, 21, 7, 2, 2, 35, 30, 30, 4, 16, 16, 13, 13, 27, 29, 29, 15, 23, 23, 10, 10, 18, 12, 12, 17, 9, 9, 20, 20, 0, 8, 8, 11, 11, 19, 5, 5, 31, 14, 14, 14, 32, 6, 6, 6, 3, 1, 26, 22, 24, 28, 28]

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
                elif statement_index in [34, 35, 36, 37, 43, 44, 46, 54, 55]:
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
            38: 'command',
            53: 'reduce',
            51: 'grammar_node',
            48: 'name_closure',
            47: 'literal',
            40: 'complex_closure',
            39: 'complex_optional'
        }
        self.__reduce_number_to_grammar_number = {
            49: 0,
            54: 1,
            55: 2,
            35: 4,
            34: 5,
            45: 7,
            41: 8,
            42: 9,
            43: 10,
            44: 11,
            50: 12,
            52: 13,
            46: 15,
            36: 20,
            37: 21
        }
        self.__naive_reduce_number = {34, 35, 36, 37, 42, 43, 44, 46, 47, 49, 54, 55}
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
        if grammar_tree.reduce_number in self.__naive_reduce_number:
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
