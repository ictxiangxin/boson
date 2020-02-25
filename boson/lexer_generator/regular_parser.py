class RegularToken:
    text: str
    line: int
    symbol: str

    def __init__(self, text: str, line: int, symbol: str):
        self.text = text
        self.line = line
        self.symbol = symbol


class RegularLexicalAnalyzer:
    def __init__(self):
        self.__token_list = []
        self.__line = 1
        self.__error_line = -1
        self.__no_error_line = -1
        self.__skip = False
        self.__move_table = {
            0: [
                [2, {'?'}, [('(', '.'), ('0', '9'), ('[', '^'), ('{', '}')], 1],
                [0, {'.'}, [], 2],
                [0, set(), [('0', '9')], 3],
                [0, {'*'}, [], 4],
                [0, {'+'}, [], 5],
                [0, {'['}, [], 6],
                [0, {'|'}, [], 7],
                [0, {'^'}, [], 8],
                [0, {'{'}, [], 9],
                [0, {']'}, [], 10],
                [0, {','}, [], 11],
                [0, {'\\'}, [], 12],
                [0, {')'}, [], 13],
                [0, {'-'}, [], 14],
                [0, {'}'}, [], 15],
                [0, {'('}, [], 16],
                [0, {'?'}, [], 17]
            ],
            12: [
                [2, set(), [], 18]
            ],
            9: [
                [0, {'_'}, [('A', 'Z'), ('a', 'z')], 19]
            ],
            19: [
                [0, {'_'}, [('0', '9'), ('A', 'Z'), ('a', 'z')], 19],
                [0, {'}'}, [], 20]
            ]
        }
        self.__character_set = {'.', 'V', '_', '7', 'b', '4', 'f', 'S', 'g', '*', 'U', 'B', 'u', 'A', 'Q', 'e', 'z', '0', '+', 'a', 'i', 'J', 'N', 'o', 'P', '[', 'm', 't', '|', '^', 'x', '2', 'F', '{', 'p', 'D', ']', 'r', ',', 'T', 'h', 'y', '9', 'W', '8', 'd', '\\', 'I', '1', 'M', 'R', '6', 'c', 'G', 'L', 'O', 'Z', ')', 'l', '-', 'k', '5', 'w', '}', 'X', 'Y', 'C', 'v', '3', 'H', '(', 'K', '?', 's', 'q', 'j', 'E', 'n'}
        self.__start_state = 0
        self.__end_state_set = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 20}
        self.__lexical_symbol_mapping = {
            1: 'normal_character',
            2: '!symbol_2',
            3: 'single_number',
            4: '!symbol_10',
            5: '!symbol_9',
            6: '!symbol_3',
            7: '!symbol_1',
            8: '!symbol_4',
            9: '!symbol_12',
            10: '!symbol_5',
            11: '!symbol_13',
            13: '!symbol_7',
            14: '!symbol_8',
            15: '!symbol_14',
            16: '!symbol_6',
            17: '!symbol_11',
            18: 'escape_character',
            20: 'reference'
        }
        self.__non_greedy_state_set = set()
        self.__symbol_function_mapping = {
            'reference': ['reference']
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
            self.__token_list.append(RegularToken(token_string, self.__line, symbol))

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
        self.__token_list.append(RegularToken('', self.__line, '$'))
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


class RegularAnalyzer:
    def __init__(self):
        self.__terminal_index = {
            '!symbol_14': 0,
            '!symbol_1': 1,
            '!symbol_7': 2,
            'single_number': 3,
            '!symbol_4': 4,
            '$': 5,
            '!symbol_5': 6,
            '!symbol_11': 7,
            '!symbol_8': 8,
            '!symbol_10': 9,
            '!symbol_9': 10,
            '!symbol_2': 11,
            'reference': 12,
            'escape_character': 13,
            '!symbol_3': 14,
            '!symbol_6': 15,
            '!symbol_12': 16,
            'normal_character': 17,
            '!symbol_13': 18
        }
        self.__action_table = {
            0: {3: 's9', 11: 's12', 12: 's15', 13: 's7', 14: 's10', 15: 's11', 17: 's16'},
            1: {1: 'r41', 2: 'r41', 3: 'r41', 5: 'r41', 7: 'r41', 9: 'r41', 10: 'r41', 11: 'r41', 12: 'r41', 13: 'r41', 14: 'r41', 15: 'r41', 16: 'r41', 17: 'r41'},
            2: {1: 'r13', 2: 'r13', 3: 'r13', 5: 'r13', 7: 's20', 9: 's22', 10: 's17', 11: 'r13', 12: 'r13', 13: 'r13', 14: 'r13', 15: 'r13', 16: 's18', 17: 'r13'},
            3: {5: 'r38'},
            4: {1: 'r30', 2: 'r30', 3: 'r30', 5: 'r30', 7: 'r30', 9: 'r30', 10: 'r30', 11: 'r30', 12: 'r30', 13: 'r30', 14: 'r30', 15: 'r30', 16: 'r30', 17: 'r30'},
            5: {1: 'r22', 2: 'r22', 3: 's9', 5: 'r22', 11: 's12', 12: 's15', 13: 's7', 14: 's10', 15: 's11', 17: 's16'},
            6: {1: 'r10', 2: 'r10', 3: 'r10', 5: 'r10', 11: 'r10', 12: 'r10', 13: 'r10', 14: 'r10', 15: 'r10', 17: 'r10'},
            7: {1: 'r42', 2: 'r42', 3: 'r42', 5: 'r42', 6: 'r42', 7: 'r42', 9: 'r42', 10: 'r42', 11: 'r42', 12: 'r42', 13: 'r42', 14: 'r42', 15: 'r42', 16: 'r42', 17: 'r42'},
            8: {1: 'r29', 2: 'r29', 3: 'r29', 5: 'r29', 7: 'r29', 9: 'r29', 10: 'r29', 11: 'r29', 12: 'r29', 13: 'r29', 14: 'r29', 15: 'r29', 16: 'r29', 17: 'r29'},
            9: {1: 'r24', 2: 'r24', 3: 'r24', 5: 'r24', 6: 'r24', 7: 'r24', 8: 'r24', 9: 'r24', 10: 'r24', 11: 'r24', 12: 'r24', 13: 'r24', 14: 'r24', 15: 'r24', 16: 'r24', 17: 'r24'},
            10: {3: 'r16', 4: 's27', 13: 'r16', 17: 'r16'},
            11: {3: 's9', 11: 's12', 12: 's15', 13: 's7', 14: 's10', 15: 's11', 17: 's16'},
            12: {1: 'r28', 2: 'r28', 3: 'r28', 5: 'r28', 7: 'r28', 9: 'r28', 10: 'r28', 11: 'r28', 12: 'r28', 13: 'r28', 14: 'r28', 15: 'r28', 16: 'r28', 17: 'r28'},
            13: {5: 'a'},
            14: {1: 'r3', 2: 'r3', 5: 'r3'},
            15: {1: 'r27', 2: 'r27', 3: 'r27', 5: 'r27', 7: 'r27', 9: 'r27', 10: 'r27', 11: 'r27', 12: 'r27', 13: 'r27', 14: 'r27', 15: 'r27', 16: 'r27', 17: 'r27'},
            16: {1: 'r23', 2: 'r23', 3: 'r23', 5: 'r23', 6: 'r23', 7: 'r23', 8: 'r23', 9: 'r23', 10: 'r23', 11: 'r23', 12: 'r23', 13: 'r23', 14: 'r23', 15: 'r23', 16: 'r23', 17: 'r23'},
            17: {1: 'r37', 2: 'r37', 3: 'r37', 5: 'r37', 11: 'r37', 12: 'r37', 13: 'r37', 14: 'r37', 15: 'r37', 17: 'r37'},
            18: {3: 's34', 18: 'r21'},
            19: {1: 'r32', 2: 'r32', 3: 'r32', 5: 'r32', 11: 'r32', 12: 'r32', 13: 'r32', 14: 'r32', 15: 'r32', 17: 'r32'},
            20: {1: 'r35', 2: 'r35', 3: 'r35', 5: 'r35', 11: 'r35', 12: 'r35', 13: 'r35', 14: 'r35', 15: 'r35', 17: 'r35'},
            21: {1: 'r12', 2: 'r12', 3: 'r12', 5: 'r12', 11: 'r12', 12: 'r12', 13: 'r12', 14: 'r12', 15: 'r12', 17: 'r12'},
            22: {1: 'r34', 2: 'r34', 3: 'r34', 5: 'r34', 11: 'r34', 12: 'r34', 13: 'r34', 14: 'r34', 15: 'r34', 17: 'r34'},
            23: {1: 'r11', 2: 'r11', 3: 'r11', 5: 'r11', 11: 'r11', 12: 'r11', 13: 'r11', 14: 'r11', 15: 'r11', 17: 'r11'},
            24: {1: 'r9', 2: 'r9', 3: 'r9', 5: 'r9', 11: 'r9', 12: 'r9', 13: 'r9', 14: 'r9', 15: 'r9', 17: 'r9'},
            25: {3: 's9', 13: 's7', 17: 's16'},
            26: {3: 'r15', 13: 'r15', 17: 'r15'},
            27: {3: 'r14', 13: 'r14', 17: 'r14'},
            28: {2: 's39'},
            29: {1: 's40', 2: 'r31', 5: 'r31'},
            30: {0: 'r33', 3: 's42', 18: 'r33'},
            31: {18: 'r19'},
            32: {18: 'r20'},
            33: {18: 's43'},
            34: {0: 'r8', 3: 'r8', 18: 'r8'},
            35: {3: 'r40', 6: 'r40', 13: 'r40', 17: 'r40'},
            36: {3: 'r41', 6: 'r41', 8: 's44', 13: 'r41', 17: 'r41'},
            37: {3: 'r18', 6: 'r18', 13: 'r18', 17: 'r18'},
            38: {3: 's9', 6: 's46', 13: 's7', 17: 's16'},
            39: {1: 'r26', 2: 'r26', 3: 'r26', 5: 'r26', 7: 'r26', 9: 'r26', 10: 'r26', 11: 'r26', 12: 'r26', 13: 'r26', 14: 'r26', 15: 'r26', 16: 'r26', 17: 'r26'},
            40: {3: 's9', 11: 's12', 12: 's15', 13: 's7', 14: 's10', 15: 's11', 17: 's16'},
            41: {1: 'r2', 2: 'r2', 5: 'r2'},
            42: {0: 'r7', 3: 'r7', 18: 'r7'},
            43: {0: 'r6', 3: 's34'},
            44: {3: 's9', 17: 's16'},
            45: {3: 'r17', 6: 'r17', 13: 'r17', 17: 'r17'},
            46: {1: 'r25', 2: 'r25', 3: 'r25', 5: 'r25', 7: 'r25', 9: 'r25', 10: 'r25', 11: 'r25', 12: 'r25', 13: 'r25', 14: 'r25', 15: 'r25', 16: 'r25', 17: 'r25'},
            47: {1: 'r1', 2: 'r1', 5: 'r1'},
            48: {0: 'r4'},
            49: {0: 'r5'},
            50: {0: 's52'},
            51: {3: 'r39', 6: 'r39', 13: 'r39', 17: 'r39'},
            52: {1: 'r36', 2: 'r36', 3: 'r36', 5: 'r36', 11: 'r36', 12: 'r36', 13: 'r36', 14: 'r36', 15: 'r36', 17: 'r36'}
        }
        self.__goto_table = {
            0: {0: 14, 1: 6, 9: 3, 12: 5, 14: 4, 16: 2, 17: 1, 18: 13, 24: 8},
            2: {4: 21, 20: 23, 21: 19},
            5: {1: 24, 14: 4, 16: 2, 17: 1, 24: 8},
            10: {2: 26, 3: 25},
            11: {0: 14, 1: 6, 9: 28, 12: 5, 14: 4, 16: 2, 17: 1, 24: 8},
            14: {22: 29},
            18: {5: 32, 8: 33, 10: 31, 15: 30},
            25: {13: 37, 14: 35, 17: 36, 19: 38},
            29: {23: 41},
            38: {13: 45, 14: 35, 17: 36},
            40: {0: 47, 1: 6, 12: 5, 14: 4, 16: 2, 17: 1, 24: 8},
            43: {6: 50, 10: 48, 11: 49, 15: 30},
            44: {17: 51}
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
        self.__reduce_to_non_terminal_index = [23, 22, 22, 11, 6, 6, 15, 15, 12, 12, 4, 21, 21, 2, 3, 3, 19, 19, 5, 8, 8, 0, 17, 17, 24, 24, 24, 16, 16, 16, 9, 1, 10, 20, 20, 20, 20, 18, 13, 13, 14, 14]

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


class RegularSemanticsAnalyzer:
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
