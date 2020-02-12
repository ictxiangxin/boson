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
        self.__token_list = []
        self.__line = 1
        self.__error_line = -1
        self.__no_error_line = -1
        self.__skip = False
        self.__move_table = {
            0: [
                [1, set(), [], 1],
                [0, set(), [('0', '9')], 2],
                [0, {'['}, [], 3],
                [0, {']'}, [], 4],
                [0, {'^'}, [], 5],
                [0, {'('}, [], 6],
                [0, {'+'}, [], 7],
                [0, {'*'}, [], 8],
                [0, {'|'}, [], 9],
                [0, {'-'}, [], 10],
                [0, {','}, [], 11],
                [0, {'}'}, [], 12],
                [0, {'.'}, [], 13],
                [0, {'\\'}, [], 14],
                [0, {'{'}, [], 15],
                [0, {')'}, [], 16],
                [0, {'?'}, [], 17]
            ],
            14: [
                [2, set(), [], 18]
            ]
        }
        self.__character_set = {'4', '[', '3', '2', ']', '(', '^', '9', '5', '*', '|', '1', '-', '0', '6', ',', '}', '8', '.', '\\', '{', '+', '7', '?', ')'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18}
        self.__lexical_symbol_mapping = {
            1: 'normal_character',
            2: 'single_number',
            3: '!symbol_3',
            4: '!symbol_5',
            5: '!symbol_4',
            6: '!symbol_6',
            7: '!symbol_9',
            8: '!symbol_10',
            9: '!symbol_1',
            10: '!symbol_8',
            11: '!symbol_13',
            12: '!symbol_14',
            13: '!symbol_2',
            15: '!symbol_12',
            16: '!symbol_7',
            17: '!symbol_11',
            18: 'escape_character'
        }
        self.__non_greedy_state_set = set()
        self.__symbol_function_mapping = {
        }
        self.__lexical_function = {}

    def _invoke_lexical_function(self, symbol: str, token_string: str):
        self.__skip = False
        if symbol in self.__symbol_function_mapping:
            for function in self.__symbol_function_mapping[symbol]:
                if function in self.__lexical_function:
                    token_string = self.__lexical_function[function](token_string)
                elif function == 'skip':
                    self.skip()
                elif function == 'newline':
                    self.newline()
        return token_string

    def _generate_token(self, state: int, token_string: str):
        symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
        token_string = self._invoke_lexical_function(symbol, token_string)
        if not self.__skip:
            self.__token_list.append(RegularExpressionToken(token_string, self.__line, symbol))

    def skip(self):
        self.__skip = True

    def newline(self):
        self.__line += 1

    def token_list(self):
        return self.__token_list

    def error_line(self):
        return self.__error_line

    def no_error_line(self):
        return self.__no_error_line

    def tokenize(self, text: str):
        self.__token_list = []
        self.__error_line = self.__no_error_line
        self.__line = 1
        state = self.__start_state
        token_string = ''
        index = 0
        while index < len(text):
            character = text[index]
            index += 1
            get_token = False
            if state in self.__non_greedy_state_set:
                get_token = True
            if not get_token and state in self.__move_table:
                for attribute, character_set, range_list, next_state in self.__move_table[state]:
                    if attribute == 2:
                        condition = character not in character_set
                        for min_character, max_character in range_list:
                            condition &= character < min_character or character > max_character
                    else:
                        condition = character in character_set
                        if attribute == 1 and character not in self.__character_set:
                            condition = True
                        for min_character, max_character in range_list:
                            if condition or min_character <= character <= max_character:
                                condition = True
                                break
                    if condition:
                        token_string += character
                        state = next_state
                        break
                else:
                    if state in self.__end_state_set:
                        get_token = True
                    else:
                        self.__error_line = self.__line
                        return self.__error_line
            else:
                if get_token or state in self.__end_state_set:
                    get_token = True
                else:
                    raise ValueError('Invalid state: state={}'.format(state))
            if get_token:
                self._generate_token(state, token_string)
                token_string = ''
                state = self.__start_state
                index -= 1
        if state in self.__end_state_set:
            self._generate_token(state, token_string)
        else:
            raise ValueError('Invalid state: state={}'.format(state))
        self.__token_list.append(RegularExpressionToken('', self.__line, '$'))
        return self.__error_line

    def lexical_function_entity(self, function_name):
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
            '!symbol_9': 0,
            'normal_character': 1,
            '!symbol_5': 2,
            '!symbol_6': 3,
            '$': 4,
            '!symbol_8': 5,
            'escape_character': 6,
            '!symbol_11': 7,
            'single_number': 8,
            '!symbol_4': 9,
            '!symbol_7': 10,
            '!symbol_12': 11,
            '!symbol_14': 12,
            '!symbol_13': 13,
            '!symbol_3': 14,
            '!symbol_2': 15,
            '!symbol_10': 16,
            '!symbol_1': 17
        }
        self.__action_table = {
            0: {1: 's1', 3: 's2', 6: 's6', 8: 's5', 14: 's3', 15: 's14'},
            1: {0: 'r23', 1: 'r23', 2: 'r23', 3: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 8: 'r23', 10: 'r23', 11: 'r23', 14: 'r23', 15: 'r23', 16: 'r23', 17: 'r23'},
            2: {1: 's1', 3: 's2', 6: 's6', 8: 's5', 14: 's3', 15: 's14'},
            3: {1: 'r16', 6: 'r16', 8: 'r16', 9: 's18'},
            4: {0: 'r29', 1: 'r29', 3: 'r29', 4: 'r29', 6: 'r29', 7: 'r29', 8: 'r29', 10: 'r29', 11: 'r29', 14: 'r29', 15: 'r29', 16: 'r29', 17: 'r29'},
            5: {0: 'r24', 1: 'r24', 2: 'r24', 3: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 7: 'r24', 8: 'r24', 10: 'r24', 11: 'r24', 14: 'r24', 15: 'r24', 16: 'r24', 17: 'r24'},
            6: {0: 'r41', 1: 'r41', 2: 'r41', 3: 'r41', 4: 'r41', 6: 'r41', 7: 'r41', 8: 'r41', 10: 'r41', 11: 'r41', 14: 'r41', 15: 'r41', 16: 'r41', 17: 'r41'},
            7: {4: 'r37'},
            8: {0: 's25', 1: 'r13', 3: 'r13', 4: 'r13', 6: 'r13', 7: 's22', 8: 'r13', 10: 'r13', 11: 's24', 14: 'r13', 15: 'r13', 16: 's20', 17: 'r13'},
            9: {0: 'r40', 1: 'r40', 3: 'r40', 4: 'r40', 6: 'r40', 7: 'r40', 8: 'r40', 10: 'r40', 11: 'r40', 14: 'r40', 15: 'r40', 16: 'r40', 17: 'r40'},
            10: {4: 'r3', 10: 'r3', 17: 'r3'},
            11: {1: 's1', 3: 's2', 4: 'r22', 6: 's6', 8: 's5', 10: 'r22', 14: 's3', 15: 's14', 17: 'r22'},
            12: {1: 'r10', 3: 'r10', 4: 'r10', 6: 'r10', 8: 'r10', 10: 'r10', 14: 'r10', 15: 'r10', 17: 'r10'},
            13: {0: 'r28', 1: 'r28', 3: 'r28', 4: 'r28', 6: 'r28', 7: 'r28', 8: 'r28', 10: 'r28', 11: 'r28', 14: 'r28', 15: 'r28', 16: 'r28', 17: 'r28'},
            14: {0: 'r27', 1: 'r27', 3: 'r27', 4: 'r27', 6: 'r27', 7: 'r27', 8: 'r27', 10: 'r27', 11: 'r27', 14: 'r27', 15: 'r27', 16: 'r27', 17: 'r27'},
            15: {4: 'a'},
            16: {10: 's29'},
            17: {1: 's1', 6: 's6', 8: 's5'},
            18: {1: 'r14', 6: 'r14', 8: 'r14'},
            19: {1: 'r15', 6: 'r15', 8: 'r15'},
            20: {1: 'r33', 3: 'r33', 4: 'r33', 6: 'r33', 8: 'r33', 10: 'r33', 14: 'r33', 15: 'r33', 17: 'r33'},
            21: {1: 'r31', 3: 'r31', 4: 'r31', 6: 'r31', 8: 'r31', 10: 'r31', 14: 'r31', 15: 'r31', 17: 'r31'},
            22: {1: 'r34', 3: 'r34', 4: 'r34', 6: 'r34', 8: 'r34', 10: 'r34', 14: 'r34', 15: 'r34', 17: 'r34'},
            23: {1: 'r11', 3: 'r11', 4: 'r11', 6: 'r11', 8: 'r11', 10: 'r11', 14: 'r11', 15: 'r11', 17: 'r11'},
            24: {8: 's34', 13: 'r21'},
            25: {1: 'r36', 3: 'r36', 4: 'r36', 6: 'r36', 8: 'r36', 10: 'r36', 14: 'r36', 15: 'r36', 17: 'r36'},
            26: {1: 'r12', 3: 'r12', 4: 'r12', 6: 'r12', 8: 'r12', 10: 'r12', 14: 'r12', 15: 'r12', 17: 'r12'},
            27: {4: 'r30', 10: 'r30', 17: 's39'},
            28: {1: 'r9', 3: 'r9', 4: 'r9', 6: 'r9', 8: 'r9', 10: 'r9', 14: 'r9', 15: 'r9', 17: 'r9'},
            29: {0: 'r26', 1: 'r26', 3: 'r26', 4: 'r26', 6: 'r26', 7: 'r26', 8: 'r26', 10: 'r26', 11: 'r26', 14: 'r26', 15: 'r26', 16: 'r26', 17: 'r26'},
            30: {1: 'r40', 2: 'r40', 5: 's41', 6: 'r40', 8: 'r40'},
            31: {1: 'r18', 2: 'r18', 6: 'r18', 8: 'r18'},
            32: {1: 's1', 2: 's42', 6: 's6', 8: 's5'},
            33: {1: 'r39', 2: 'r39', 6: 'r39', 8: 'r39'},
            34: {8: 'r8', 12: 'r8', 13: 'r8'},
            35: {13: 's44'},
            36: {8: 's45', 12: 'r32', 13: 'r32'},
            37: {13: 'r20'},
            38: {13: 'r19'},
            39: {1: 's1', 3: 's2', 6: 's6', 8: 's5', 14: 's3', 15: 's14'},
            40: {4: 'r2', 10: 'r2', 17: 'r2'},
            41: {1: 's1', 8: 's5'},
            42: {0: 'r25', 1: 'r25', 3: 'r25', 4: 'r25', 6: 'r25', 7: 'r25', 8: 'r25', 10: 'r25', 11: 'r25', 14: 'r25', 15: 'r25', 16: 'r25', 17: 'r25'},
            43: {1: 'r17', 2: 'r17', 6: 'r17', 8: 'r17'},
            44: {8: 's34', 12: 'r6'},
            45: {8: 'r7', 12: 'r7', 13: 'r7'},
            46: {4: 'r1', 10: 'r1', 17: 'r1'},
            47: {1: 'r38', 2: 'r38', 6: 'r38', 8: 'r38'},
            48: {12: 'r4'},
            49: {12: 'r5'},
            50: {12: 's51'},
            51: {1: 'r35', 3: 'r35', 4: 'r35', 6: 'r35', 8: 'r35', 10: 'r35', 14: 'r35', 15: 'r35', 17: 'r35'}
        }
        self.__goto_table = {
            0: {1: 15, 2: 9, 3: 7, 4: 11, 10: 4, 17: 12, 18: 13, 20: 10, 23: 8},
            2: {2: 9, 3: 16, 4: 11, 10: 4, 17: 12, 18: 13, 20: 10, 23: 8},
            3: {13: 19, 21: 17},
            8: {6: 23, 8: 26, 24: 21},
            10: {22: 27},
            11: {2: 9, 10: 4, 17: 28, 18: 13, 23: 8},
            17: {2: 30, 9: 32, 10: 33, 14: 31},
            24: {5: 38, 7: 35, 11: 36, 15: 37},
            27: {16: 40},
            32: {2: 30, 10: 33, 14: 43},
            39: {2: 9, 4: 11, 10: 4, 17: 12, 18: 13, 20: 46, 23: 8},
            41: {2: 47},
            44: {0: 50, 5: 48, 11: 36, 12: 49}
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
        self.__reduce_to_non_terminal_index = [16, 22, 22, 12, 0, 0, 11, 11, 4, 4, 8, 24, 24, 13, 21, 21, 9, 9, 15, 7, 7, 20, 2, 2, 18, 18, 23, 23, 23, 3, 17, 5, 6, 6, 6, 6, 1, 14, 14, 10, 10]

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
