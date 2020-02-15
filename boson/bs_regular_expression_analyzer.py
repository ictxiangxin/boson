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
                [0, {']'}, [], 1],
                [1, set(), [], 2],
                [0, {'\\'}, [], 3],
                [0, set(), [('0', '9')], 4],
                [0, {'('}, [], 5],
                [0, {'-'}, [], 6],
                [0, {'.'}, [], 7],
                [0, {'}'}, [], 8],
                [0, {'['}, [], 9],
                [0, {'?'}, [], 10],
                [0, {'{'}, [], 11],
                [0, {','}, [], 12],
                [0, {')'}, [], 13],
                [0, {'*'}, [], 14],
                [0, {'+'}, [], 15],
                [0, {'^'}, [], 16],
                [0, {'|'}, [], 17]
            ],
            3: [
                [2, set(), [], 18]
            ]
        }
        self.__character_set = {']', '\\', '3', '5', '(', '8', '6', '9', '}', '.', '-', '[', '?', '{', ',', '0', ')', '7', '1', '*', '+', '^', '2', '|', '4'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18}
        self.__lexical_symbol_mapping = {
            1: '!symbol_5',
            2: 'normal_character',
            4: 'single_number',
            5: '!symbol_6',
            6: '!symbol_8',
            7: '!symbol_2',
            8: '!symbol_14',
            9: '!symbol_3',
            10: '!symbol_11',
            11: '!symbol_12',
            12: '!symbol_13',
            13: '!symbol_7',
            14: '!symbol_10',
            15: '!symbol_9',
            16: '!symbol_4',
            17: '!symbol_1',
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
            'single_number': 0,
            '$': 1,
            '!symbol_12': 2,
            'normal_character': 3,
            '!symbol_9': 4,
            '!symbol_10': 5,
            '!symbol_13': 6,
            '!symbol_11': 7,
            '!symbol_4': 8,
            '!symbol_7': 9,
            '!symbol_1': 10,
            'escape_character': 11,
            '!symbol_5': 12,
            '!symbol_14': 13,
            '!symbol_8': 14,
            '!symbol_2': 15,
            '!symbol_6': 16,
            '!symbol_3': 17
        }
        self.__action_table = {
            0: {0: 's10', 3: 's15', 11: 's3', 15: 's9', 16: 's11', 17: 's2'},
            1: {0: 's10', 1: 'r22', 3: 's15', 9: 'r22', 10: 'r22', 11: 's3', 15: 's9', 16: 's11', 17: 's2'},
            2: {0: 'r16', 3: 'r16', 8: 's19', 11: 'r16'},
            3: {0: 'r41', 1: 'r41', 2: 'r41', 3: 'r41', 4: 'r41', 5: 'r41', 7: 'r41', 9: 'r41', 10: 'r41', 11: 'r41', 12: 'r41', 15: 'r41', 16: 'r41', 17: 'r41'},
            4: {0: 'r29', 1: 'r29', 2: 'r29', 3: 'r29', 4: 'r29', 5: 'r29', 7: 'r29', 9: 'r29', 10: 'r29', 11: 'r29', 15: 'r29', 16: 'r29', 17: 'r29'},
            5: {0: 'r13', 1: 'r13', 2: 's23', 3: 'r13', 4: 's25', 5: 's26', 7: 's24', 9: 'r13', 10: 'r13', 11: 'r13', 15: 'r13', 16: 'r13', 17: 'r13'},
            6: {0: 'r10', 1: 'r10', 3: 'r10', 9: 'r10', 10: 'r10', 11: 'r10', 15: 'r10', 16: 'r10', 17: 'r10'},
            7: {1: 'a'},
            8: {1: 'r3', 9: 'r3', 10: 'r3'},
            9: {0: 'r27', 1: 'r27', 2: 'r27', 3: 'r27', 4: 'r27', 5: 'r27', 7: 'r27', 9: 'r27', 10: 'r27', 11: 'r27', 15: 'r27', 16: 'r27', 17: 'r27'},
            10: {0: 'r24', 1: 'r24', 2: 'r24', 3: 'r24', 4: 'r24', 5: 'r24', 7: 'r24', 9: 'r24', 10: 'r24', 11: 'r24', 12: 'r24', 14: 'r24', 15: 'r24', 16: 'r24', 17: 'r24'},
            11: {0: 's10', 3: 's15', 11: 's3', 15: 's9', 16: 's11', 17: 's2'},
            12: {0: 'r28', 1: 'r28', 2: 'r28', 3: 'r28', 4: 'r28', 5: 'r28', 7: 'r28', 9: 'r28', 10: 'r28', 11: 'r28', 15: 'r28', 16: 'r28', 17: 'r28'},
            13: {0: 'r40', 1: 'r40', 2: 'r40', 3: 'r40', 4: 'r40', 5: 'r40', 7: 'r40', 9: 'r40', 10: 'r40', 11: 'r40', 15: 'r40', 16: 'r40', 17: 'r40'},
            14: {1: 'r37'},
            15: {0: 'r23', 1: 'r23', 2: 'r23', 3: 'r23', 4: 'r23', 5: 'r23', 7: 'r23', 9: 'r23', 10: 'r23', 11: 'r23', 12: 'r23', 14: 'r23', 15: 'r23', 16: 'r23', 17: 'r23'},
            16: {0: 'r9', 1: 'r9', 3: 'r9', 9: 'r9', 10: 'r9', 11: 'r9', 15: 'r9', 16: 'r9', 17: 'r9'},
            17: {0: 's10', 3: 's15', 11: 's3'},
            18: {0: 'r15', 3: 'r15', 11: 'r15'},
            19: {0: 'r14', 3: 'r14', 11: 'r14'},
            20: {0: 'r12', 1: 'r12', 3: 'r12', 9: 'r12', 10: 'r12', 11: 'r12', 15: 'r12', 16: 'r12', 17: 'r12'},
            21: {0: 'r11', 1: 'r11', 3: 'r11', 9: 'r11', 10: 'r11', 11: 'r11', 15: 'r11', 16: 'r11', 17: 'r11'},
            22: {0: 'r31', 1: 'r31', 3: 'r31', 9: 'r31', 10: 'r31', 11: 'r31', 15: 'r31', 16: 'r31', 17: 'r31'},
            23: {0: 's34', 6: 'r21'},
            24: {0: 'r34', 1: 'r34', 3: 'r34', 9: 'r34', 10: 'r34', 11: 'r34', 15: 'r34', 16: 'r34', 17: 'r34'},
            25: {0: 'r36', 1: 'r36', 3: 'r36', 9: 'r36', 10: 'r36', 11: 'r36', 15: 'r36', 16: 'r36', 17: 'r36'},
            26: {0: 'r33', 1: 'r33', 3: 'r33', 9: 'r33', 10: 'r33', 11: 'r33', 15: 'r33', 16: 'r33', 17: 'r33'},
            27: {1: 'r30', 9: 'r30', 10: 's38'},
            28: {9: 's40'},
            29: {0: 's10', 3: 's15', 11: 's3', 12: 's41'},
            30: {0: 'r18', 3: 'r18', 11: 'r18', 12: 'r18'},
            31: {0: 'r40', 3: 'r40', 11: 'r40', 12: 'r40', 14: 's43'},
            32: {0: 'r39', 3: 'r39', 11: 'r39', 12: 'r39'},
            33: {0: 's44', 6: 'r32', 13: 'r32'},
            34: {0: 'r8', 6: 'r8', 13: 'r8'},
            35: {6: 'r20'},
            36: {6: 's45'},
            37: {6: 'r19'},
            38: {0: 's10', 3: 's15', 11: 's3', 15: 's9', 16: 's11', 17: 's2'},
            39: {1: 'r2', 9: 'r2', 10: 'r2'},
            40: {0: 'r26', 1: 'r26', 2: 'r26', 3: 'r26', 4: 'r26', 5: 'r26', 7: 'r26', 9: 'r26', 10: 'r26', 11: 'r26', 15: 'r26', 16: 'r26', 17: 'r26'},
            41: {0: 'r25', 1: 'r25', 2: 'r25', 3: 'r25', 4: 'r25', 5: 'r25', 7: 'r25', 9: 'r25', 10: 'r25', 11: 'r25', 15: 'r25', 16: 'r25', 17: 'r25'},
            42: {0: 'r17', 3: 'r17', 11: 'r17', 12: 'r17'},
            43: {0: 's10', 3: 's15'},
            44: {0: 'r7', 6: 'r7', 13: 'r7'},
            45: {0: 's34', 13: 'r6'},
            46: {1: 'r1', 9: 'r1', 10: 'r1'},
            47: {0: 'r38', 3: 'r38', 11: 'r38', 12: 'r38'},
            48: {13: 's51'},
            49: {13: 'r5'},
            50: {13: 'r4'},
            51: {0: 'r35', 1: 'r35', 3: 'r35', 9: 'r35', 10: 'r35', 11: 'r35', 15: 'r35', 16: 'r35', 17: 'r35'}
        }
        self.__goto_table = {
            0: {0: 6, 5: 5, 9: 13, 10: 12, 12: 14, 14: 1, 16: 8, 17: 7, 21: 4},
            1: {0: 16, 5: 5, 9: 13, 10: 12, 21: 4},
            2: {13: 18, 23: 17},
            5: {4: 20, 8: 22, 15: 21},
            8: {20: 27},
            11: {0: 6, 5: 5, 9: 13, 10: 12, 12: 28, 14: 1, 16: 8, 21: 4},
            17: {2: 30, 7: 29, 9: 31, 21: 32},
            23: {1: 35, 11: 33, 18: 36, 22: 37},
            27: {24: 39},
            29: {2: 42, 9: 31, 21: 32},
            38: {0: 6, 5: 5, 9: 13, 10: 12, 14: 1, 16: 46, 21: 4},
            43: {9: 47},
            45: {3: 48, 11: 33, 19: 49, 22: 50}
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
        self.__reduce_to_non_terminal_index = [24, 20, 20, 19, 3, 3, 11, 11, 14, 14, 4, 8, 8, 13, 23, 23, 7, 7, 1, 18, 18, 16, 9, 9, 10, 10, 5, 5, 5, 12, 0, 22, 15, 15, 15, 15, 17, 2, 2, 21, 21]

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
