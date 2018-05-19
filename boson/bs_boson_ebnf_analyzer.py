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
            'parentheses_l': 1,
            'end': 2,
            'name': 3,
            'plus': 4,
            'reduce': 5,
            'node': 6,
            'or': 7,
            'null': 8,
            'star': 9,
            'bracket_r': 10,
            'parentheses_r': 11,
            '$': 12,
            'assign': 13,
            'command': 14,
            'comma': 15,
            'bracket_l': 16
        }
        self.__action_table = {
            0: {3: 's7', 14: 's1'},
            1: {0: 's12', 3: 's11'},
            2: {3: 's7', 12: 'r52', 14: 's1'},
            3: {3: 'r57', 12: 'r57', 14: 'r57'},
            4: {12: 'a'},
            5: {3: 'r58', 12: 'r58', 14: 'r58'},
            6: {3: 'r2', 12: 'r2', 14: 'r2'},
            7: {5: 's14'},
            8: {0: 'r20', 2: 'r20', 3: 'r20'},
            9: {0: 's12', 2: 's16', 3: 's11'},
            10: {0: 'r28', 2: 'r28', 3: 'r28'},
            11: {0: 'r4', 2: 'r4', 3: 'r4'},
            12: {0: 'r3', 2: 'r3', 3: 'r3'},
            13: {3: 'r1', 12: 'r1', 14: 'r1'},
            14: {0: 's22', 1: 's25', 2: 'r47', 3: 's21', 7: 'r47', 8: 's18', 13: 'r47', 16: 's20'},
            15: {0: 'r29', 2: 'r29', 3: 'r29'},
            16: {3: 'r41', 12: 'r41', 14: 'r41'},
            17: {0: 's22', 1: 's25', 2: 'r45', 3: 's21', 7: 'r45', 13: 'r45', 16: 's20'},
            18: {2: 'r46', 7: 'r46', 13: 'r46'},
            19: {0: 'r49', 1: 'r49', 2: 'r49', 3: 'r49', 7: 'r49', 10: 'r49', 11: 'r49', 13: 'r49', 16: 'r49'},
            20: {0: 's22', 1: 's25', 3: 's21', 16: 's20'},
            21: {0: 'r18', 1: 'r18', 2: 'r18', 3: 'r18', 4: 's36', 7: 'r18', 9: 's34', 10: 'r18', 11: 'r18', 13: 'r18', 16: 'r18'},
            22: {0: 'r50', 1: 'r50', 2: 'r50', 3: 'r50', 7: 'r50', 10: 'r50', 11: 'r50', 13: 'r50', 16: 'r50'},
            23: {2: 'r38', 7: 'r38', 13: 's38'},
            24: {2: 'r32', 7: 'r32'},
            25: {0: 's22', 1: 's25', 3: 's21', 16: 's20'},
            26: {0: 'r6', 1: 'r6', 2: 'r6', 3: 'r6', 7: 'r6', 13: 'r6', 16: 'r6'},
            27: {2: 's42'},
            28: {0: 'r5', 1: 'r5', 2: 'r5', 3: 'r5', 7: 'r5', 13: 'r5', 16: 'r5'},
            29: {0: 'r24', 1: 'r24', 3: 'r24', 7: 's45', 10: 'r24', 11: 'r24', 16: 'r24'},
            30: {10: 's46'},
            31: {0: 's22', 1: 's25', 3: 's21', 10: 'r59', 11: 'r59', 16: 's20'},
            32: {0: 'r17', 1: 'r17', 2: 'r17', 3: 'r17', 7: 'r17', 10: 'r17', 11: 'r17', 13: 'r17', 16: 'r17'},
            33: {0: 'r16', 1: 'r16', 2: 'r16', 3: 'r16', 7: 'r16', 10: 'r16', 11: 'r16', 13: 'r16', 16: 'r16'},
            34: {0: 'r40', 1: 'r40', 2: 'r40', 3: 'r40', 7: 'r40', 10: 'r40', 11: 'r40', 13: 'r40', 16: 'r40'},
            35: {0: 'r51', 1: 'r51', 2: 'r51', 3: 'r51', 7: 'r51', 10: 'r51', 11: 'r51', 13: 'r51', 16: 'r51'},
            36: {0: 'r39', 1: 'r39', 2: 'r39', 3: 'r39', 7: 'r39', 10: 'r39', 11: 'r39', 13: 'r39', 16: 'r39'},
            37: {2: 'r44', 7: 'r44'},
            38: {1: 'r35', 3: 's48'},
            39: {2: 'r37', 7: 'r37'},
            40: {2: 'r48', 7: 's52'},
            41: {11: 's53'},
            42: {3: 'r56', 12: 'r56', 14: 'r56'},
            43: {7: 's45', 10: 'r60', 11: 'r60'},
            44: {7: 'r26', 10: 'r26', 11: 'r26'},
            45: {0: 's22', 1: 's25', 3: 's21', 16: 's20'},
            46: {0: 'r42', 1: 'r42', 2: 'r42', 3: 'r42', 7: 'r42', 10: 'r42', 11: 'r42', 13: 'r42', 16: 'r42'},
            47: {0: 'r23', 1: 'r23', 3: 'r23', 10: 'r23', 11: 'r23', 16: 'r23'},
            48: {1: 'r33'},
            49: {1: 's57'},
            50: {1: 'r34'},
            51: {2: 'r31', 7: 'r31'},
            52: {0: 's22', 1: 's25', 2: 'r47', 3: 's21', 7: 'r47', 8: 's18', 13: 'r47', 16: 's20'},
            53: {0: 'r22', 1: 'r22', 2: 'r22', 3: 'r22', 4: 's36', 7: 'r22', 9: 's34', 10: 'r22', 11: 'r22', 13: 'r22', 16: 'r22'},
            54: {7: 'r27', 10: 'r27', 11: 'r27'},
            55: {7: 'r25', 10: 'r25', 11: 'r25'},
            56: {2: 'r36', 7: 'r36'},
            57: {6: 'r12', 9: 's62'},
            58: {2: 'r30', 7: 'r30'},
            59: {0: 'r43', 1: 'r43', 2: 'r43', 3: 'r43', 7: 'r43', 10: 'r43', 11: 'r43', 13: 'r43', 16: 'r43'},
            60: {0: 'r19', 1: 'r19', 2: 'r19', 3: 'r19', 7: 'r19', 10: 'r19', 11: 'r19', 13: 'r19', 16: 'r19'},
            61: {0: 'r21', 1: 'r21', 2: 'r21', 3: 'r21', 7: 'r21', 10: 'r21', 11: 'r21', 13: 'r21', 16: 'r21'},
            62: {6: 'r10'},
            63: {11: 's67'},
            64: {6: 's68'},
            65: {6: 'r11'},
            66: {11: 'r9', 15: 'r9'},
            67: {2: 'r53', 7: 'r53', 11: 'r53', 15: 'r53'},
            68: {1: 's57', 11: 'r15', 15: 'r15'},
            69: {11: 'r55', 15: 's74'},
            70: {11: 'r13', 15: 'r13'},
            71: {11: 'r14', 15: 'r14'},
            72: {11: 'r54', 15: 'r54'},
            73: {11: 'r8', 15: 'r8'},
            74: {6: 'r12', 9: 's62'},
            75: {11: 'r7', 15: 'r7'}
        }
        self.__goto_table = {
            0: {17: 5, 21: 4, 22: 3, 30: 6, 36: 2},
            1: {0: 10, 6: 9, 14: 8},
            2: {17: 5, 22: 3, 30: 13},
            9: {0: 15, 14: 8},
            14: {2: 23, 7: 24, 12: 27, 13: 26, 23: 17, 34: 19},
            17: {13: 28, 34: 19},
            20: {9: 31, 13: 29, 26: 30, 34: 19},
            21: {16: 35, 29: 33, 32: 32},
            23: {10: 37, 33: 39},
            24: {4: 40},
            25: {9: 31, 13: 29, 26: 41, 34: 19},
            29: {8: 43, 38: 44},
            31: {13: 47, 34: 19},
            38: {11: 49, 31: 50},
            40: {20: 51},
            43: {38: 54},
            45: {13: 55, 34: 19},
            49: {5: 56},
            52: {2: 23, 7: 58, 13: 26, 23: 17, 34: 19},
            53: {18: 59, 27: 61, 29: 60},
            57: {3: 64, 19: 63, 25: 66, 35: 65},
            66: {15: 69},
            68: {5: 70, 28: 72, 37: 71},
            69: {1: 73},
            74: {3: 64, 25: 75, 35: 65}
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
        self.__reduce_to_non_terminal_index = [36, 36, 14, 14, 23, 23, 1, 15, 15, 35, 3, 3, 37, 28, 28, 32, 16, 16, 27, 0, 18, 18, 9, 9, 38, 8, 8, 6, 6, 20, 4, 4, 31, 11, 11, 33, 10, 10, 29, 29, 22, 34, 34, 7, 2, 2, 2, 12, 13, 13, 13, 21, 5, 25, 19, 17, 30, 30, 26, 26]

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
        self.__naive_reduce_number = {38, 39, 45, 46, 48, 49, 56, 57}
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
