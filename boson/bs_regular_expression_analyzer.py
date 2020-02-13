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
                [0, {'.'}, [], 3],
                [0, {'{'}, [], 4],
                [0, {'}'}, [], 5],
                [0, {'['}, [], 6],
                [0, {'|'}, [], 7],
                [0, {'('}, [], 8],
                [0, {'?'}, [], 9],
                [0, {'+'}, [], 10],
                [0, {'^'}, [], 11],
                [0, {'\\'}, [], 12],
                [0, {'-'}, [], 13],
                [0, {','}, [], 14],
                [0, {')'}, [], 15],
                [0, {']'}, [], 16],
                [0, {'*'}, [], 17]
            ],
            12: [
                [2, set(), [], 18]
            ]
        }
        self.__character_set = {'0', '1', '.', '{', '}', '[', '|', '8', '4', '(', '5', '2', '?', '+', '3', '^', '6', '\\', '-', ',', ')', ']', '*', '9', '7'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18}
        self.__lexical_symbol_mapping = {
            1: 'normal_character',
            2: 'single_number',
            3: '!symbol_2',
            4: '!symbol_12',
            5: '!symbol_14',
            6: '!symbol_3',
            7: '!symbol_1',
            8: '!symbol_6',
            9: '!symbol_11',
            10: '!symbol_9',
            11: '!symbol_4',
            13: '!symbol_8',
            14: '!symbol_13',
            15: '!symbol_7',
            16: '!symbol_5',
            17: '!symbol_10',
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
        self.__error_index = -1
        self.__no_error_index = -1

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

    def no_error_index(self):
        return self.__no_error_index


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
            '!symbol_12': 0,
            '!symbol_10': 1,
            '!symbol_13': 2,
            '!symbol_4': 3,
            '!symbol_6': 4,
            '!symbol_7': 5,
            'escape_character': 6,
            'single_number': 7,
            '!symbol_5': 8,
            '!symbol_2': 9,
            '!symbol_8': 10,
            'normal_character': 11,
            '!symbol_1': 12,
            '!symbol_11': 13,
            '!symbol_3': 14,
            '!symbol_14': 15,
            '!symbol_9': 16,
            '$': 17
        }
        self.__action_table = {
            0: {4: 's2', 6: 's10', 7: 's11', 9: 's3', 11: 's5', 14: 's9'},
            1: {4: 's2', 5: 'r22', 6: 's10', 7: 's11', 9: 's3', 11: 's5', 12: 'r22', 14: 's9', 17: 'r22'},
            2: {4: 's2', 6: 's10', 7: 's11', 9: 's3', 11: 's5', 14: 's9'},
            3: {0: 'r27', 1: 'r27', 4: 'r27', 5: 'r27', 6: 'r27', 7: 'r27', 9: 'r27', 11: 'r27', 12: 'r27', 13: 'r27', 14: 'r27', 16: 'r27', 17: 'r27'},
            4: {4: 'r10', 5: 'r10', 6: 'r10', 7: 'r10', 9: 'r10', 11: 'r10', 12: 'r10', 14: 'r10', 17: 'r10'},
            5: {0: 'r23', 1: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 8: 'r23', 9: 'r23', 10: 'r23', 11: 'r23', 12: 'r23', 13: 'r23', 14: 'r23', 16: 'r23', 17: 'r23'},
            6: {17: 'r37'},
            7: {0: 'r28', 1: 'r28', 4: 'r28', 5: 'r28', 6: 'r28', 7: 'r28', 9: 'r28', 11: 'r28', 12: 'r28', 13: 'r28', 14: 'r28', 16: 'r28', 17: 'r28'},
            8: {0: 'r29', 1: 'r29', 4: 'r29', 5: 'r29', 6: 'r29', 7: 'r29', 9: 'r29', 11: 'r29', 12: 'r29', 13: 'r29', 14: 'r29', 16: 'r29', 17: 'r29'},
            9: {3: 's19', 6: 'r16', 7: 'r16', 11: 'r16'},
            10: {0: 'r41', 1: 'r41', 4: 'r41', 5: 'r41', 6: 'r41', 7: 'r41', 8: 'r41', 9: 'r41', 11: 'r41', 12: 'r41', 13: 'r41', 14: 'r41', 16: 'r41', 17: 'r41'},
            11: {0: 'r24', 1: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 7: 'r24', 8: 'r24', 9: 'r24', 10: 'r24', 11: 'r24', 12: 'r24', 13: 'r24', 14: 'r24', 16: 'r24', 17: 'r24'},
            12: {5: 'r3', 12: 'r3', 17: 'r3'},
            13: {17: 'a'},
            14: {0: 'r40', 1: 'r40', 4: 'r40', 5: 'r40', 6: 'r40', 7: 'r40', 9: 'r40', 11: 'r40', 12: 'r40', 13: 'r40', 14: 'r40', 16: 'r40', 17: 'r40'},
            15: {0: 's24', 1: 's26', 4: 'r13', 5: 'r13', 6: 'r13', 7: 'r13', 9: 'r13', 11: 'r13', 12: 'r13', 13: 's27', 14: 'r13', 16: 's25', 17: 'r13'},
            16: {4: 'r9', 5: 'r9', 6: 'r9', 7: 'r9', 9: 'r9', 11: 'r9', 12: 'r9', 14: 'r9', 17: 'r9'},
            17: {5: 's29'},
            18: {6: 's10', 7: 's11', 11: 's5'},
            19: {6: 'r14', 7: 'r14', 11: 'r14'},
            20: {6: 'r15', 7: 'r15', 11: 'r15'},
            21: {5: 'r30', 12: 's34', 17: 'r30'},
            22: {4: 'r12', 5: 'r12', 6: 'r12', 7: 'r12', 9: 'r12', 11: 'r12', 12: 'r12', 14: 'r12', 17: 'r12'},
            23: {4: 'r11', 5: 'r11', 6: 'r11', 7: 'r11', 9: 'r11', 11: 'r11', 12: 'r11', 14: 'r11', 17: 'r11'},
            24: {2: 'r21', 7: 's39'},
            25: {4: 'r36', 5: 'r36', 6: 'r36', 7: 'r36', 9: 'r36', 11: 'r36', 12: 'r36', 14: 'r36', 17: 'r36'},
            26: {4: 'r33', 5: 'r33', 6: 'r33', 7: 'r33', 9: 'r33', 11: 'r33', 12: 'r33', 14: 'r33', 17: 'r33'},
            27: {4: 'r34', 5: 'r34', 6: 'r34', 7: 'r34', 9: 'r34', 11: 'r34', 12: 'r34', 14: 'r34', 17: 'r34'},
            28: {4: 'r31', 5: 'r31', 6: 'r31', 7: 'r31', 9: 'r31', 11: 'r31', 12: 'r31', 14: 'r31', 17: 'r31'},
            29: {0: 'r26', 1: 'r26', 4: 'r26', 5: 'r26', 6: 'r26', 7: 'r26', 9: 'r26', 11: 'r26', 12: 'r26', 13: 'r26', 14: 'r26', 16: 'r26', 17: 'r26'},
            30: {6: 'r40', 7: 'r40', 8: 'r40', 10: 's41', 11: 'r40'},
            31: {6: 'r18', 7: 'r18', 8: 'r18', 11: 'r18'},
            32: {6: 'r39', 7: 'r39', 8: 'r39', 11: 'r39'},
            33: {6: 's10', 7: 's11', 8: 's43', 11: 's5'},
            34: {4: 's2', 6: 's10', 7: 's11', 9: 's3', 11: 's5', 14: 's9'},
            35: {5: 'r2', 12: 'r2', 17: 'r2'},
            36: {2: 's45'},
            37: {2: 'r32', 7: 's46', 15: 'r32'},
            38: {2: 'r19'},
            39: {2: 'r8', 7: 'r8', 15: 'r8'},
            40: {2: 'r20'},
            41: {7: 's11', 11: 's5'},
            42: {6: 'r17', 7: 'r17', 8: 'r17', 11: 'r17'},
            43: {0: 'r25', 1: 'r25', 4: 'r25', 5: 'r25', 6: 'r25', 7: 'r25', 9: 'r25', 11: 'r25', 12: 'r25', 13: 'r25', 14: 'r25', 16: 'r25', 17: 'r25'},
            44: {5: 'r1', 12: 'r1', 17: 'r1'},
            45: {7: 's39', 15: 'r6'},
            46: {2: 'r7', 7: 'r7', 15: 'r7'},
            47: {6: 'r38', 7: 'r38', 8: 'r38', 11: 'r38'},
            48: {15: 'r4'},
            49: {15: 'r5'},
            50: {15: 's51'},
            51: {4: 'r35', 5: 'r35', 6: 'r35', 7: 'r35', 9: 'r35', 11: 'r35', 12: 'r35', 14: 'r35', 17: 'r35'}
        }
        self.__goto_table = {
            0: {4: 12, 7: 4, 8: 6, 13: 1, 14: 14, 20: 8, 22: 13, 23: 15, 24: 7},
            1: {7: 16, 14: 14, 20: 8, 23: 15, 24: 7},
            2: {4: 12, 7: 4, 8: 17, 13: 1, 14: 14, 20: 8, 23: 15, 24: 7},
            9: {6: 20, 19: 18},
            12: {10: 21},
            15: {0: 22, 3: 28, 9: 23},
            18: {1: 33, 12: 31, 14: 30, 20: 32},
            21: {2: 35},
            24: {5: 40, 11: 37, 18: 38, 21: 36},
            33: {12: 42, 14: 30, 20: 32},
            34: {4: 44, 7: 4, 13: 1, 14: 14, 20: 8, 23: 15, 24: 7},
            41: {14: 47},
            45: {11: 37, 15: 50, 17: 49, 18: 48}
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
        self.__reduce_to_non_terminal_index = [2, 10, 10, 17, 15, 15, 11, 11, 13, 13, 0, 3, 3, 6, 19, 19, 1, 1, 5, 21, 21, 4, 14, 14, 24, 24, 23, 23, 23, 8, 7, 18, 9, 9, 9, 9, 22, 12, 12, 20, 20]

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
