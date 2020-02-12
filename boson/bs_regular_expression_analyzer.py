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
        self.__move_table = {
            0: [
                [0, set(), [('0', '9')], 1],
                [1, set(), [], 2],
                [0, {'('}, [], 3],
                [0, {'{'}, [], 4],
                [0, {'*'}, [], 5],
                [0, {'['}, [], 6],
                [0, {'\\'}, [], 7],
                [0, {'}'}, [], 8],
                [0, {')'}, [], 9],
                [0, {']'}, [], 10],
                [0, {'|'}, [], 11],
                [0, {'?'}, [], 12],
                [0, {'^'}, [], 13],
                [0, {'.'}, [], 14],
                [0, {'-'}, [], 15],
                [0, {','}, [], 16],
                [0, {'+'}, [], 17]
            ],
            7: [
                [2, set(), [], 18]
            ]
        }
        self.__character_set = {'3', '(', '{', '0', '*', '[', '\\', '}', '1', '8', ']', ')', '6', '9', '|', '4', '7', '5', '?', '^', '.', '2', '-', ',', '+'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18}
        self.__lexical_symbol_mapping = {
            1: 'single_number',
            2: 'normal_character',
            3: '!symbol_6',
            4: '!symbol_12',
            5: '!symbol_10',
            6: '!symbol_3',
            8: '!symbol_14',
            9: '!symbol_7',
            10: '!symbol_5',
            11: '!symbol_1',
            12: '!symbol_11',
            13: '!symbol_4',
            14: '!symbol_2',
            15: '!symbol_8',
            16: '!symbol_13',
            17: '!symbol_9',
            18: 'escape_character'
        }
        self.__symbol_function_mapping = {
        }
        self.__lexical_function = {}

    def _invoke_lexical_function(self, symbol: str, token_string):
        if symbol in self.__symbol_function_mapping:
            for function in self.__symbol_function_mapping[symbol]:
                if function in self.__lexical_function:
                    token_string = self.__lexical_function[function](token_string)
                elif function == 'skip':
                    token_string = None
                elif function == 'newline':
                    self.__line += 1
        return token_string

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
            generate_token = False
            if state in self.__move_table:
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
                        self.__error_line = self.__line
                        return self.__error_line
            else:
                if state in self.__end_state_set:
                    generate_token = True
                else:
                    raise ValueError('Invalid state: state={}'.format(state))
            if generate_token:
                symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
                token_string = self._invoke_lexical_function(symbol, token_string)
                if token_string is not None:
                    self.__token_list.append(RegularExpressionToken(token_string, self.__line, symbol))
                token_string = ''
                state = self.__start_state
                index -= 1
        if state in self.__end_state_set:
            symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
            token_string = self._invoke_lexical_function(symbol, token_string)
            if token_string is not None:
                self.__token_list.append(RegularExpressionToken(token_string, self.__line, symbol))
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
            '!symbol_3': 0,
            '$': 1,
            '!symbol_2': 2,
            '!symbol_10': 3,
            '!symbol_8': 4,
            '!symbol_9': 5,
            '!symbol_6': 6,
            '!symbol_14': 7,
            '!symbol_1': 8,
            'escape_character': 9,
            '!symbol_5': 10,
            'single_number': 11,
            '!symbol_7': 12,
            '!symbol_4': 13,
            '!symbol_13': 14,
            '!symbol_11': 15,
            'normal_character': 16,
            '!symbol_12': 17
        }
        self.__action_table = {
            0: {0: 's4', 2: 's2', 6: 's14', 9: 's6', 11: 's10', 16: 's13'},
            1: {0: 'r29', 1: 'r29', 2: 'r29', 3: 'r29', 5: 'r29', 6: 'r29', 8: 'r29', 9: 'r29', 11: 'r29', 12: 'r29', 15: 'r29', 16: 'r29', 17: 'r29'},
            2: {0: 'r27', 1: 'r27', 2: 'r27', 3: 'r27', 5: 'r27', 6: 'r27', 8: 'r27', 9: 'r27', 11: 'r27', 12: 'r27', 15: 'r27', 16: 'r27', 17: 'r27'},
            3: {0: 's4', 1: 'r22', 2: 's2', 6: 's14', 8: 'r22', 9: 's6', 11: 's10', 12: 'r22', 16: 's13'},
            4: {9: 'r16', 11: 'r16', 13: 's18', 16: 'r16'},
            5: {1: 'r3', 8: 'r3', 12: 'r3'},
            6: {0: 'r41', 1: 'r41', 2: 'r41', 3: 'r41', 5: 'r41', 6: 'r41', 8: 'r41', 9: 'r41', 10: 'r41', 11: 'r41', 12: 'r41', 15: 'r41', 16: 'r41', 17: 'r41'},
            7: {0: 'r13', 1: 'r13', 2: 'r13', 3: 's24', 5: 's25', 6: 'r13', 8: 'r13', 9: 'r13', 11: 'r13', 12: 'r13', 15: 's21', 16: 'r13', 17: 's26'},
            8: {1: 'a'},
            9: {0: 'r40', 1: 'r40', 2: 'r40', 3: 'r40', 5: 'r40', 6: 'r40', 8: 'r40', 9: 'r40', 11: 'r40', 12: 'r40', 15: 'r40', 16: 'r40', 17: 'r40'},
            10: {0: 'r24', 1: 'r24', 2: 'r24', 3: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 8: 'r24', 9: 'r24', 10: 'r24', 11: 'r24', 12: 'r24', 15: 'r24', 16: 'r24', 17: 'r24'},
            11: {0: 'r10', 1: 'r10', 2: 'r10', 6: 'r10', 8: 'r10', 9: 'r10', 11: 'r10', 12: 'r10', 16: 'r10'},
            12: {0: 'r28', 1: 'r28', 2: 'r28', 3: 'r28', 5: 'r28', 6: 'r28', 8: 'r28', 9: 'r28', 11: 'r28', 12: 'r28', 15: 'r28', 16: 'r28', 17: 'r28'},
            13: {0: 'r23', 1: 'r23', 2: 'r23', 3: 'r23', 4: 'r23', 5: 'r23', 6: 'r23', 8: 'r23', 9: 'r23', 10: 'r23', 11: 'r23', 12: 'r23', 15: 'r23', 16: 'r23', 17: 'r23'},
            14: {0: 's4', 2: 's2', 6: 's14', 9: 's6', 11: 's10', 16: 's13'},
            15: {1: 'r37'},
            16: {0: 'r9', 1: 'r9', 2: 'r9', 6: 'r9', 8: 'r9', 9: 'r9', 11: 'r9', 12: 'r9', 16: 'r9'},
            17: {9: 's6', 11: 's10', 16: 's13'},
            18: {9: 'r14', 11: 'r14', 16: 'r14'},
            19: {9: 'r15', 11: 'r15', 16: 'r15'},
            20: {1: 'r30', 8: 's34', 12: 'r30'},
            21: {0: 'r34', 1: 'r34', 2: 'r34', 6: 'r34', 8: 'r34', 9: 'r34', 11: 'r34', 12: 'r34', 16: 'r34'},
            22: {0: 'r11', 1: 'r11', 2: 'r11', 6: 'r11', 8: 'r11', 9: 'r11', 11: 'r11', 12: 'r11', 16: 'r11'},
            23: {0: 'r12', 1: 'r12', 2: 'r12', 6: 'r12', 8: 'r12', 9: 'r12', 11: 'r12', 12: 'r12', 16: 'r12'},
            24: {0: 'r33', 1: 'r33', 2: 'r33', 6: 'r33', 8: 'r33', 9: 'r33', 11: 'r33', 12: 'r33', 16: 'r33'},
            25: {0: 'r36', 1: 'r36', 2: 'r36', 6: 'r36', 8: 'r36', 9: 'r36', 11: 'r36', 12: 'r36', 16: 'r36'},
            26: {11: 's37', 14: 'r21'},
            27: {0: 'r31', 1: 'r31', 2: 'r31', 6: 'r31', 8: 'r31', 9: 'r31', 11: 'r31', 12: 'r31', 16: 'r31'},
            28: {12: 's40'},
            29: {9: 's6', 10: 's42', 11: 's10', 16: 's13'},
            30: {9: 'r39', 10: 'r39', 11: 'r39', 16: 'r39'},
            31: {4: 's43', 9: 'r40', 10: 'r40', 11: 'r40', 16: 'r40'},
            32: {9: 'r18', 10: 'r18', 11: 'r18', 16: 'r18'},
            33: {1: 'r2', 8: 'r2', 12: 'r2'},
            34: {0: 's4', 2: 's2', 6: 's14', 9: 's6', 11: 's10', 16: 's13'},
            35: {7: 'r32', 11: 's45', 14: 'r32'},
            36: {14: 's46'},
            37: {7: 'r8', 11: 'r8', 14: 'r8'},
            38: {14: 'r19'},
            39: {14: 'r20'},
            40: {0: 'r26', 1: 'r26', 2: 'r26', 3: 'r26', 5: 'r26', 6: 'r26', 8: 'r26', 9: 'r26', 11: 'r26', 12: 'r26', 15: 'r26', 16: 'r26', 17: 'r26'},
            41: {9: 'r17', 10: 'r17', 11: 'r17', 16: 'r17'},
            42: {0: 'r25', 1: 'r25', 2: 'r25', 3: 'r25', 5: 'r25', 6: 'r25', 8: 'r25', 9: 'r25', 11: 'r25', 12: 'r25', 15: 'r25', 16: 'r25', 17: 'r25'},
            43: {11: 's10', 16: 's13'},
            44: {1: 'r1', 8: 'r1', 12: 'r1'},
            45: {7: 'r7', 11: 'r7', 14: 'r7'},
            46: {7: 'r6', 11: 's37'},
            47: {9: 'r38', 10: 'r38', 11: 'r38', 16: 'r38'},
            48: {7: 'r4'},
            49: {7: 'r5'},
            50: {7: 's51'},
            51: {0: 'r35', 1: 'r35', 2: 'r35', 6: 'r35', 8: 'r35', 9: 'r35', 11: 'r35', 12: 'r35', 16: 'r35'}
        }
        self.__goto_table = {
            0: {1: 5, 2: 3, 4: 15, 6: 11, 11: 1, 14: 9, 18: 12, 21: 7, 22: 8},
            3: {6: 16, 11: 1, 14: 9, 18: 12, 21: 7},
            4: {0: 19, 8: 17},
            5: {23: 20},
            7: {9: 22, 13: 23, 16: 27},
            14: {1: 5, 2: 3, 4: 28, 6: 11, 11: 1, 14: 9, 18: 12, 21: 7},
            17: {7: 32, 11: 30, 12: 29, 14: 31},
            20: {5: 33},
            26: {3: 38, 10: 35, 15: 39, 20: 36},
            29: {7: 41, 11: 30, 14: 31},
            34: {1: 44, 2: 3, 6: 11, 11: 1, 14: 9, 18: 12, 21: 7},
            43: {14: 47},
            46: {3: 48, 10: 35, 17: 49, 19: 50}
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
        self.__reduce_to_non_terminal_index = [5, 23, 23, 17, 19, 19, 10, 10, 2, 2, 13, 16, 16, 0, 8, 8, 12, 12, 15, 20, 20, 1, 14, 14, 18, 18, 21, 21, 21, 4, 6, 3, 9, 9, 9, 9, 22, 7, 7, 11, 11]

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
