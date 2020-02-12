class RegularExpressionToken:
    text: str
    line: int
    symbol: str

    def __init__(self, text: str, line: int, symbol: str):
        self.text = text
        self.line = line
        self.symbol = symbol


class RegularExpressionLexicalAnalyzer:
    def __init__(self):
        self.__move_table = {
            0: [
                [False, set(), [('0', '9')], 1],
                [False, {True}, [], 2],
                [False, {'.'}, [], 3],
                [False, {'^'}, [], 4],
                [False, {')'}, [], 5],
                [False, {'\\'}, [], 6],
                [False, {'}'}, [], 7],
                [False, {'|'}, [], 8],
                [False, {'('}, [], 9],
                [False, {'*'}, [], 10],
                [False, {'+'}, [], 11],
                [False, {'{'}, [], 12],
                [False, {'?'}, [], 13],
                [False, {'-'}, [], 14],
                [False, {']'}, [], 15],
                [False, {'['}, [], 16],
                [False, {','}, [], 17]
            ],
            6: [
                [True, set(), [], 18]
            ]
        }
        self.__character_set = {'8', '.', '3', '^', ')', '\\', '9', '}', '(', '|', '*', '+', '{', '2', '1', '?', '-', '4', ']', '7', '[', '5', ',', '6', '0'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18}
        self.__lexical_symbol_mapping = {
            1: 'single_number',
            2: 'normal_character',
            3: '!symbol_2',
            4: '!symbol_4',
            5: '!symbol_7',
            7: '!symbol_14',
            8: '!symbol_1',
            9: '!symbol_6',
            10: '!symbol_10',
            11: '!symbol_9',
            12: '!symbol_12',
            13: '!symbol_11',
            14: '!symbol_8',
            15: '!symbol_5',
            16: '!symbol_3',
            17: '!symbol_13',
            18: 'escape_character'
        }
        self.__symbol_function_mapping = {
        }
        self.__lexical_function = {
            'skip': self._lexical_function_skip,
            'newline': self._lexical_function_newline,
        }
        self.__line = 0

    def _lexical_function_skip(self, token_string):
        return None

    def _lexical_function_newline(self, token_string):
        self.__line += 1
        return token_string

    def invoke_lexical_function(self, symbol: str, token):
        if symbol in self.__symbol_function_mapping:
            for function in self.__symbol_function_mapping[symbol]:
                if function in self.__lexical_function:
                    token = self.__lexical_function[function](token)
        return token

    def tokenize(self, text: str):
        token_list = []
        self.__line = 0
        state = self.__start_state
        token_string = ''
        index = 0
        while index < len(text):
            character = text[index]
            index += 1
            generate_token = False
            if state in self.__move_table:
                for reverse, character_set, range_list, next_state in self.__move_table[state]:
                    if reverse:
                        condition = character not in character_set
                        for min_character, max_character in range_list:
                            condition &= character < min_character or character > max_character
                    else:
                        condition = character in character_set
                        if True in character_set and character not in self.__character_set:
                            condition = True
                        for min_character, max_character in range_list:
                            if condition or min_character <= character <= max_character:
                                condition = True
                                break
                    if condition:
                        if state in self.__end_state_set and next_state not in self.__end_state_set:
                            generate_token = True
                            break
                        token_string += character
                        state = next_state
                        break
                else:
                    if state in self.__end_state_set:
                        generate_token = True
                    else:
                        raise ValueError('[Line: {}] Invalid character: {}[{}]'.format(self.__line, token_string, character))
            else:
                if state in self.__end_state_set:
                    generate_token = True
                else:
                    raise ValueError('Invalid state: state={}'.format(state))
            if generate_token:
                symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
                token_string = self.invoke_lexical_function(symbol, token_string)
                if token_string is not None:
                    token_list.append(RegularExpressionToken(token_string, self.__line, symbol))
                token_string = ''
                state = self.__start_state
                index -= 1
        if state in self.__end_state_set:
            symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
            token_string = self.invoke_lexical_function(symbol, token_string)
            if token_string is not None:
                token_list.append(RegularExpressionToken(token_string, self.__line, symbol))
        else:
            raise ValueError('Invalid state: state={}'.format(state))
        token_list.append(RegularExpressionToken('', self.__line, '$'))
        return token_list

    def lexical_function(self, function_name):
        def decorator(f):
            self.__lexical_function[function_name] = f
            return f
        return decorator


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
            '!symbol_1': 0,
            '!symbol_2': 1,
            'single_number': 2,
            '!symbol_7': 3,
            '!symbol_9': 4,
            '!symbol_5': 5,
            '!symbol_11': 6,
            '!symbol_8': 7,
            '$': 8,
            '!symbol_6': 9,
            '!symbol_10': 10,
            '!symbol_14': 11,
            '!symbol_4': 12,
            '!symbol_13': 13,
            '!symbol_3': 14,
            '!symbol_12': 15,
            'escape_character': 16,
            'normal_character': 17
        }
        self.__action_table = {
            0: {1: 's10', 2: 's14', 9: 's12', 14: 's15', 16: 's3', 17: 's9'},
            1: {0: 'r22', 1: 's10', 2: 's14', 3: 'r22', 8: 'r22', 9: 's12', 14: 's15', 16: 's3', 17: 's9'},
            2: {8: 'a'},
            3: {0: 'r41', 1: 'r41', 2: 'r41', 3: 'r41', 4: 'r41', 5: 'r41', 6: 'r41', 8: 'r41', 9: 'r41', 10: 'r41', 14: 'r41', 15: 'r41', 16: 'r41', 17: 'r41'},
            4: {0: 'r29', 1: 'r29', 2: 'r29', 3: 'r29', 4: 'r29', 6: 'r29', 8: 'r29', 9: 'r29', 10: 'r29', 14: 'r29', 15: 'r29', 16: 'r29', 17: 'r29'},
            5: {0: 'r40', 1: 'r40', 2: 'r40', 3: 'r40', 4: 'r40', 6: 'r40', 8: 'r40', 9: 'r40', 10: 'r40', 14: 'r40', 15: 'r40', 16: 'r40', 17: 'r40'},
            6: {0: 'r28', 1: 'r28', 2: 'r28', 3: 'r28', 4: 'r28', 6: 'r28', 8: 'r28', 9: 'r28', 10: 'r28', 14: 'r28', 15: 'r28', 16: 'r28', 17: 'r28'},
            7: {0: 'r3', 3: 'r3', 8: 'r3'},
            8: {8: 'r37'},
            9: {0: 'r23', 1: 'r23', 2: 'r23', 3: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 8: 'r23', 9: 'r23', 10: 'r23', 14: 'r23', 15: 'r23', 16: 'r23', 17: 'r23'},
            10: {0: 'r27', 1: 'r27', 2: 'r27', 3: 'r27', 4: 'r27', 6: 'r27', 8: 'r27', 9: 'r27', 10: 'r27', 14: 'r27', 15: 'r27', 16: 'r27', 17: 'r27'},
            11: {0: 'r13', 1: 'r13', 2: 'r13', 3: 'r13', 4: 's19', 6: 's20', 8: 'r13', 9: 'r13', 10: 's18', 14: 'r13', 15: 's24', 16: 'r13', 17: 'r13'},
            12: {1: 's10', 2: 's14', 9: 's12', 14: 's15', 16: 's3', 17: 's9'},
            13: {0: 'r10', 1: 'r10', 2: 'r10', 3: 'r10', 8: 'r10', 9: 'r10', 14: 'r10', 16: 'r10', 17: 'r10'},
            14: {0: 'r24', 1: 'r24', 2: 'r24', 3: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 7: 'r24', 8: 'r24', 9: 'r24', 10: 'r24', 14: 'r24', 15: 'r24', 16: 'r24', 17: 'r24'},
            15: {2: 'r16', 12: 's26', 16: 'r16', 17: 'r16'},
            16: {0: 'r9', 1: 'r9', 2: 'r9', 3: 'r9', 8: 'r9', 9: 'r9', 14: 'r9', 16: 'r9', 17: 'r9'},
            17: {0: 's29', 3: 'r30', 8: 'r30'},
            18: {0: 'r33', 1: 'r33', 2: 'r33', 3: 'r33', 8: 'r33', 9: 'r33', 14: 'r33', 16: 'r33', 17: 'r33'},
            19: {0: 'r36', 1: 'r36', 2: 'r36', 3: 'r36', 8: 'r36', 9: 'r36', 14: 'r36', 16: 'r36', 17: 'r36'},
            20: {0: 'r34', 1: 'r34', 2: 'r34', 3: 'r34', 8: 'r34', 9: 'r34', 14: 'r34', 16: 'r34', 17: 'r34'},
            21: {0: 'r31', 1: 'r31', 2: 'r31', 3: 'r31', 8: 'r31', 9: 'r31', 14: 'r31', 16: 'r31', 17: 'r31'},
            22: {0: 'r12', 1: 'r12', 2: 'r12', 3: 'r12', 8: 'r12', 9: 'r12', 14: 'r12', 16: 'r12', 17: 'r12'},
            23: {0: 'r11', 1: 'r11', 2: 'r11', 3: 'r11', 8: 'r11', 9: 'r11', 14: 'r11', 16: 'r11', 17: 'r11'},
            24: {2: 's35', 13: 'r21'},
            25: {3: 's36'},
            26: {2: 'r14', 16: 'r14', 17: 'r14'},
            27: {2: 's14', 16: 's3', 17: 's9'},
            28: {2: 'r15', 16: 'r15', 17: 'r15'},
            29: {1: 's10', 2: 's14', 9: 's12', 14: 's15', 16: 's3', 17: 's9'},
            30: {0: 'r2', 3: 'r2', 8: 'r2'},
            31: {13: 'r20'},
            32: {2: 's42', 11: 'r32', 13: 'r32'},
            33: {13: 's43'},
            34: {13: 'r19'},
            35: {2: 'r8', 11: 'r8', 13: 'r8'},
            36: {0: 'r26', 1: 'r26', 2: 'r26', 3: 'r26', 4: 'r26', 6: 'r26', 8: 'r26', 9: 'r26', 10: 'r26', 14: 'r26', 15: 'r26', 16: 'r26', 17: 'r26'},
            37: {2: 'r40', 5: 'r40', 7: 's44', 16: 'r40', 17: 'r40'},
            38: {2: 'r39', 5: 'r39', 16: 'r39', 17: 'r39'},
            39: {2: 's14', 5: 's45', 16: 's3', 17: 's9'},
            40: {2: 'r18', 5: 'r18', 16: 'r18', 17: 'r18'},
            41: {0: 'r1', 3: 'r1', 8: 'r1'},
            42: {2: 'r7', 11: 'r7', 13: 'r7'},
            43: {2: 's35', 11: 'r6'},
            44: {2: 's14', 17: 's9'},
            45: {0: 'r25', 1: 'r25', 2: 'r25', 3: 'r25', 4: 'r25', 6: 'r25', 8: 'r25', 9: 'r25', 10: 'r25', 14: 'r25', 15: 'r25', 16: 'r25', 17: 'r25'},
            46: {2: 'r17', 5: 'r17', 16: 'r17', 17: 'r17'},
            47: {11: 'r5'},
            48: {11: 's51'},
            49: {11: 'r4'},
            50: {2: 'r38', 5: 'r38', 16: 'r38', 17: 'r38'},
            51: {0: 'r35', 1: 'r35', 2: 'r35', 3: 'r35', 8: 'r35', 9: 'r35', 14: 'r35', 16: 'r35', 17: 'r35'}
        }
        self.__goto_table = {
            0: {1: 5, 4: 7, 6: 4, 9: 2, 10: 13, 13: 8, 14: 11, 15: 6, 23: 1},
            1: {1: 5, 6: 4, 10: 16, 14: 11, 15: 6},
            7: {0: 17},
            11: {16: 23, 22: 21, 24: 22},
            12: {1: 5, 4: 7, 6: 4, 10: 13, 13: 25, 14: 11, 15: 6, 23: 1},
            15: {12: 28, 19: 27},
            17: {3: 30},
            24: {5: 34, 7: 32, 20: 33, 21: 31},
            27: {1: 37, 2: 40, 6: 38, 8: 39},
            29: {1: 5, 4: 41, 6: 4, 10: 13, 14: 11, 15: 6, 23: 1},
            39: {1: 37, 2: 46, 6: 38},
            43: {5: 49, 7: 32, 11: 47, 18: 48},
            44: {1: 50}
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
            28: ('0',),
            27: ('0',),
            26: ('0',),
            15: (),
            16: ('*0', '1'),
            24: (('*1', ('0',)), '2'),
            25: ('1',),
            37: ('0', '2'),
            20: (),
            5: (),
            34: (('*1', ('0',)), ('*3', ('0',))),
            6: ('*0', '1'),
            31: ('*0',)
        }
        self.__reduce_symbol_sum = [2, 2, 0, 1, 1, 0, 2, 1, 2, 1, 1, 1, 0, 1, 1, 0, 2, 1, 1, 1, 0, 1, 1, 1, 4, 3, 1, 1, 1, 2, 2, 1, 1, 1, 5, 1, 1, 3, 1, 1, 1]
        self.__reduce_to_non_terminal_index = [3, 0, 0, 11, 18, 18, 7, 7, 23, 23, 24, 22, 22, 12, 19, 19, 8, 8, 21, 20, 20, 4, 1, 1, 15, 15, 14, 14, 14, 13, 10, 5, 16, 16, 16, 16, 9, 2, 2, 6, 6]

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
                elif statement_index in [0, 3, 4, 7, 9, 10, 11, 13, 14, 17, 18, 19, 22, 23, 32, 33, 35, 38, 39, 40]:
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
            28: 'simple_construct',
            27: 'complex_construct',
            26: 'wildcard_character',
            24: 'select',
            25: 'sub_expression',
            34: 'count_range',
            31: 'construct_number'
        }
        self.__reduce_number_to_grammar_number = {
            39: 7,
            40: 8,
            22: 9,
            23: 10,
            38: 13,
            37: 14,
            35: 15,
            32: 16,
            33: 17
        }
        self.__naive_reduce_number = {32, 33, 35, 36, 38, 39, 40, 22, 23, 26, 27, 28}
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
