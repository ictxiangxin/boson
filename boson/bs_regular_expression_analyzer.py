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
                [2, {'}', '?', '{'}, [('(', '.'), ('0', '9'), ('[', '^')], 14],
                [0, {'('}, [], 1],
                [0, set(), [('0', '9')], 2],
                [0, {'\\'}, [], 3],
                [0, {','}, [], 4],
                [0, {']'}, [], 5],
                [0, {'?'}, [], 6],
                [0, {'-'}, [], 7],
                [0, {'{'}, [], 8],
                [0, {'^'}, [], 9],
                [0, {')'}, [], 10],
                [0, {'}'}, [], 11],
                [0, {'*'}, [], 12],
                [0, {'.'}, [], 13],
                [0, {'['}, [], 15],
                [0, {'+'}, [], 16]
            ],
            8: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 17]
            ],
            17: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 17],
                [0, {'}'}, [], 18]
            ],
            3: [
                [2, set(), [], 19]
            ]
        }
        self.__character_set = {'A', 'O', '(', 'l', 'k', '3', '1', 'e', '\\', 'V', 'r', 'Q', 'q', 's', '6', 'a', 'J', 'c', ',', 'w', 'p', 'i', 'o', '8', 'K', 'Z', 'N', 'm', '4', 'F', 'g', ']', 'j', 'I', 'y', 'S', '7', '?', 'W', 't', '-', '{', '2', 'h', 'M', 'T', 'L', 'G', '^', ')', 'E', 'v', 'D', 'C', '}', '9', 'n', '5', '0', '*', '.', 'z', 'u', 'd', 'b', 'H', 'B', 'x', 'X', 'f', '_', 'U', 'Y', 'R', 'P', '|', '[', '+'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19}
        self.__lexical_symbol_mapping = {
            1: '!symbol_6',
            2: 'single_number',
            4: '!symbol_13',
            5: '!symbol_5',
            6: '!symbol_11',
            7: '!symbol_8',
            8: '!symbol_12',
            9: '!symbol_4',
            10: '!symbol_7',
            11: '!symbol_14',
            12: '!symbol_10',
            13: '!symbol_2',
            14: 'normal_character',
            15: '!symbol_3',
            16: '!symbol_9',
            18: 'reference',
            19: 'escape_character'
        }
        self.__non_greedy_state_set = set()
        self.__symbol_function_mapping = {
        }
        self.__lexical_function = {}

    def _invoke_lexical_function(self, symbol: str, token_string: str) -> str:
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

    def _generate_token(self, state: int, token_string: str) -> None:
        symbol = self.__lexical_symbol_mapping.get(state, '!symbol')
        token_string = self._invoke_lexical_function(symbol, token_string)
        if not self.__skip:
            self.__token_list.append(RegularExpressionToken(token_string, self.__line, symbol))

    def skip(self) -> None:
        self.__skip = True

    def newline(self) -> None:
        self.__line += 1

    def token_list(self) -> list:
        return self.__token_list

    def error_line(self) -> int:
        return self.__error_line

    def no_error_line(self) -> int:
        return self.__no_error_line

    def tokenize(self, text: str) -> int:
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
            '!symbol_11': 0,
            '!symbol_5': 1,
            '!symbol_3': 2,
            '!symbol_8': 3,
            '!symbol_4': 4,
            '$': 5,
            'reference': 6,
            '!symbol_10': 7,
            '!symbol_1': 8,
            '!symbol_13': 9,
            'single_number': 10,
            '!symbol_7': 11,
            'normal_character': 12,
            '!symbol_12': 13,
            'escape_character': 14,
            '!symbol_14': 15,
            '!symbol_2': 16,
            '!symbol_6': 17,
            '!symbol_9': 18
        }
        self.__action_table = {
            0: {2: 's9', 6: 's11', 10: 's6', 12: 's3', 14: 's7', 16: 's13', 17: 's12'},
            1: {2: 's9', 5: 'r22', 6: 's11', 8: 'r22', 10: 's6', 11: 'r22', 12: 's3', 14: 's7', 16: 's13', 17: 's12'},
            2: {5: 'r3', 8: 'r3', 11: 'r3'},
            3: {0: 'r23', 1: 'r23', 2: 'r23', 3: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 8: 'r23', 10: 'r23', 11: 'r23', 12: 'r23', 13: 'r23', 14: 'r23', 16: 'r23', 17: 'r23', 18: 'r23'},
            4: {0: 'r29', 2: 'r29', 5: 'r29', 6: 'r29', 7: 'r29', 8: 'r29', 10: 'r29', 11: 'r29', 12: 'r29', 13: 'r29', 14: 'r29', 16: 'r29', 17: 'r29', 18: 'r29'},
            5: {5: 'a'},
            6: {0: 'r24', 1: 'r24', 2: 'r24', 3: 'r24', 5: 'r24', 6: 'r24', 7: 'r24', 8: 'r24', 10: 'r24', 11: 'r24', 12: 'r24', 13: 'r24', 14: 'r24', 16: 'r24', 17: 'r24', 18: 'r24'},
            7: {0: 'r42', 1: 'r42', 2: 'r42', 5: 'r42', 6: 'r42', 7: 'r42', 8: 'r42', 10: 'r42', 11: 'r42', 12: 'r42', 13: 'r42', 14: 'r42', 16: 'r42', 17: 'r42', 18: 'r42'},
            8: {0: 's22', 2: 'r13', 5: 'r13', 6: 'r13', 7: 's20', 8: 'r13', 10: 'r13', 11: 'r13', 12: 'r13', 13: 's25', 14: 'r13', 16: 'r13', 17: 'r13', 18: 's23'},
            9: {4: 's28', 10: 'r16', 12: 'r16', 14: 'r16'},
            10: {5: 'r38'},
            11: {0: 'r27', 2: 'r27', 5: 'r27', 6: 'r27', 7: 'r27', 8: 'r27', 10: 'r27', 11: 'r27', 12: 'r27', 13: 'r27', 14: 'r27', 16: 'r27', 17: 'r27', 18: 'r27'},
            12: {2: 's9', 6: 's11', 10: 's6', 12: 's3', 14: 's7', 16: 's13', 17: 's12'},
            13: {0: 'r28', 2: 'r28', 5: 'r28', 6: 'r28', 7: 'r28', 8: 'r28', 10: 'r28', 11: 'r28', 12: 'r28', 13: 'r28', 14: 'r28', 16: 'r28', 17: 'r28', 18: 'r28'},
            14: {2: 'r10', 5: 'r10', 6: 'r10', 8: 'r10', 10: 'r10', 11: 'r10', 12: 'r10', 14: 'r10', 16: 'r10', 17: 'r10'},
            15: {0: 'r30', 2: 'r30', 5: 'r30', 6: 'r30', 7: 'r30', 8: 'r30', 10: 'r30', 11: 'r30', 12: 'r30', 13: 'r30', 14: 'r30', 16: 'r30', 17: 'r30', 18: 'r30'},
            16: {0: 'r41', 2: 'r41', 5: 'r41', 6: 'r41', 7: 'r41', 8: 'r41', 10: 'r41', 11: 'r41', 12: 'r41', 13: 'r41', 14: 'r41', 16: 'r41', 17: 'r41', 18: 'r41'},
            17: {2: 'r9', 5: 'r9', 6: 'r9', 8: 'r9', 10: 'r9', 11: 'r9', 12: 'r9', 14: 'r9', 16: 'r9', 17: 'r9'},
            18: {5: 'r31', 8: 's30', 11: 'r31'},
            19: {2: 'r12', 5: 'r12', 6: 'r12', 8: 'r12', 10: 'r12', 11: 'r12', 12: 'r12', 14: 'r12', 16: 'r12', 17: 'r12'},
            20: {2: 'r34', 5: 'r34', 6: 'r34', 8: 'r34', 10: 'r34', 11: 'r34', 12: 'r34', 14: 'r34', 16: 'r34', 17: 'r34'},
            21: {2: 'r11', 5: 'r11', 6: 'r11', 8: 'r11', 10: 'r11', 11: 'r11', 12: 'r11', 14: 'r11', 16: 'r11', 17: 'r11'},
            22: {2: 'r35', 5: 'r35', 6: 'r35', 8: 'r35', 10: 'r35', 11: 'r35', 12: 'r35', 14: 'r35', 16: 'r35', 17: 'r35'},
            23: {2: 'r37', 5: 'r37', 6: 'r37', 8: 'r37', 10: 'r37', 11: 'r37', 12: 'r37', 14: 'r37', 16: 'r37', 17: 'r37'},
            24: {2: 'r32', 5: 'r32', 6: 'r32', 8: 'r32', 10: 'r32', 11: 'r32', 12: 'r32', 14: 'r32', 16: 'r32', 17: 'r32'},
            25: {9: 'r21', 10: 's35'},
            26: {10: 's6', 12: 's3', 14: 's7'},
            27: {10: 'r15', 12: 'r15', 14: 'r15'},
            28: {10: 'r14', 12: 'r14', 14: 'r14'},
            29: {11: 's41'},
            30: {2: 's9', 6: 's11', 10: 's6', 12: 's3', 14: 's7', 16: 's13', 17: 's12'},
            31: {5: 'r2', 8: 'r2', 11: 'r2'},
            32: {9: 'r19'},
            33: {9: 's43'},
            34: {9: 'r33', 10: 's44', 15: 'r33'},
            35: {9: 'r8', 10: 'r8', 15: 'r8'},
            36: {9: 'r20'},
            37: {1: 'r18', 10: 'r18', 12: 'r18', 14: 'r18'},
            38: {1: 'r40', 10: 'r40', 12: 'r40', 14: 'r40'},
            39: {1: 'r41', 3: 's45', 10: 'r41', 12: 'r41', 14: 'r41'},
            40: {1: 's47', 10: 's6', 12: 's3', 14: 's7'},
            41: {0: 'r26', 2: 'r26', 5: 'r26', 6: 'r26', 7: 'r26', 8: 'r26', 10: 'r26', 11: 'r26', 12: 'r26', 13: 'r26', 14: 'r26', 16: 'r26', 17: 'r26', 18: 'r26'},
            42: {5: 'r1', 8: 'r1', 11: 'r1'},
            43: {10: 's35', 15: 'r6'},
            44: {9: 'r7', 10: 'r7', 15: 'r7'},
            45: {10: 's6', 12: 's3'},
            46: {1: 'r17', 10: 'r17', 12: 'r17', 14: 'r17'},
            47: {0: 'r25', 2: 'r25', 5: 'r25', 6: 'r25', 7: 'r25', 8: 'r25', 10: 'r25', 11: 'r25', 12: 'r25', 13: 'r25', 14: 'r25', 16: 'r25', 17: 'r25', 18: 'r25'},
            48: {15: 'r4'},
            49: {15: 's52'},
            50: {15: 'r5'},
            51: {1: 'r39', 10: 'r39', 12: 'r39', 14: 'r39'},
            52: {2: 'r36', 5: 'r36', 6: 'r36', 8: 'r36', 10: 'r36', 11: 'r36', 12: 'r36', 14: 'r36', 16: 'r36', 17: 'r36'}
        }
        self.__goto_table = {
            0: {1: 14, 4: 15, 7: 2, 9: 4, 12: 10, 15: 16, 18: 8, 20: 5, 21: 1},
            1: {1: 17, 4: 15, 9: 4, 15: 16, 18: 8},
            2: {16: 18},
            8: {13: 19, 22: 24, 23: 21},
            9: {8: 26, 14: 27},
            12: {1: 14, 4: 15, 7: 2, 9: 4, 12: 29, 15: 16, 18: 8, 21: 1},
            18: {11: 31},
            25: {0: 36, 5: 34, 17: 33, 19: 32},
            26: {4: 38, 10: 40, 15: 39, 24: 37},
            30: {1: 14, 4: 15, 7: 42, 9: 4, 15: 16, 18: 8, 21: 1},
            40: {4: 38, 15: 39, 24: 46},
            43: {2: 49, 3: 50, 5: 34, 19: 48},
            45: {15: 51}
        }
        self.__node_table = {
            37: ('0',),
            1: ('*0', '1'),
            2: (),
            30: ('0', ('*1', ('1',))),
            8: ('*0', '1'),
            21: ('*0',),
            12: (),
            31: ('0', ('*1', ('0',))),
            29: ('0',),
            28: ('0',),
            27: ('0',),
            15: (),
            16: ('*0', '1'),
            24: (('*1', ('0',)), '2'),
            25: ('1',),
            26: ('0',),
            38: ('0', '2'),
            20: (),
            5: (),
            35: (('*1', ('0',)), ('*3', ('0',))),
            6: ('*0', '1'),
            32: ('*0',)
        }
        self.__reduce_symbol_sum = [2, 2, 0, 1, 1, 0, 2, 1, 2, 1, 1, 1, 0, 1, 1, 0, 2, 1, 1, 1, 0, 1, 1, 1, 4, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 5, 1, 1, 3, 1, 1, 1]
        self.__reduce_to_non_terminal_index = [11, 16, 16, 3, 2, 2, 5, 5, 21, 21, 13, 22, 22, 14, 8, 8, 10, 10, 0, 17, 17, 7, 15, 15, 9, 9, 9, 18, 18, 18, 12, 1, 19, 23, 23, 23, 23, 20, 24, 24, 4, 4]

    def __generate_grammar_tuple(self, statement_index: int, node_tuple: tuple, symbol_package: list) -> BosonGrammarNode:
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

    def grammar_analysis(self, token_list: list) -> BosonGrammar:
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
                elif statement_index in [0, 3, 4, 7, 9, 10, 11, 13, 14, 17, 18, 19, 22, 23, 33, 34, 36, 39, 40, 41]:
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
            37: 'regular_expression',
            30: 'expression',
            21: 'branch',
            31: 'group',
            29: 'simple_construct',
            28: 'complex_construct',
            27: 'wildcard_character',
            24: 'select',
            25: 'sub_expression',
            26: 'reference',
            35: 'count_range',
            32: 'construct_number'
        }
        self.__reduce_number_to_grammar_number = {
            40: 7,
            41: 8,
            22: 9,
            23: 10,
            39: 14,
            38: 15,
            36: 16,
            33: 17,
            34: 18
        }
        self.__naive_reduce_number = {33, 34, 36, 37, 39, 40, 41, 22, 23, 26, 27, 28, 29}
        self.__semantics_entity = {}

    @staticmethod
    def __default_semantics_entity(grammar_entity: list) -> list:
        return grammar_entity

    @staticmethod
    def __naive_semantics_entity(grammar_entity: list):
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

    def semantics_entity(self, sign: (int, str)) -> callable:
        def decorator(f: callable):
            if isinstance(sign, int):
                name = '!grammar_{}'.format(sign)
            elif isinstance(sign, str):
                name = sign
            else:
                raise ValueError('Invalid grammar sign: {}'.format(sign))
            self.__semantics_entity[name] = f
            return f
        return decorator
