class RegularToken:
    text: str
    line: int
    symbol: str

    def __init__(self, text: str, line: int, symbol: str):
        self.text = text
        self.line = line
        self.symbol = symbol


class RegularLexer:
    def __init__(self):
        self.__token_list: list = []
        self.__line: int = 1
        self.__error_line: int = -1
        self.__no_error_line: int = -1
        self.__skip: bool = False
        self.__compact_move_table: dict = {
            0: [
                [0, set(), [('\x30', '\x39')], 1],
                [2, {'\x3f'}, [('\x28', '\x2e'), ('\x30', '\x39'), ('\x5b', '\x5e'), ('\x7b', '\x7d')], 2],
                [0, {'\x7c'}, [], 3],
                [0, {'\x2e'}, [], 4],
                [0, {'\x5b'}, [], 5],
                [0, {'\x5e'}, [], 6],
                [0, {'\x5c'}, [], 7],
                [0, {'\x5d'}, [], 8],
                [0, {'\x28'}, [], 9],
                [0, {'\x29'}, [], 10],
                [0, {'\x7b'}, [], 11],
                [0, {'\x2d'}, [], 12],
                [0, {'\x2b'}, [], 13],
                [0, {'\x2a'}, [], 14],
                [0, {'\x3f'}, [], 15],
                [0, {'\x2c'}, [], 16],
                [0, {'\x7d'}, [], 17]
            ],
            11: [
                [0, {'\x5f'}, [('\x41', '\x5a'), ('\x61', '\x7a')], 18]
            ],
            18: [
                [0, {'\x5f'}, [('\x30', '\x39'), ('\x41', '\x5a'), ('\x61', '\x7a')], 18],
                [0, {'\x7d'}, [], 19]
            ],
            7: [
                [2, set(), [], 20]
            ]
        }
        self.__character_set: set = {'\x47', '\x70', '\x61', '\x36', '\x32', '\x35', '\x68', '\x6e', '\x59', '\x5f', '\x54', '\x34', '\x66', '\x37', '\x38', '\x67', '\x5e', '\x6c', '\x7b', '\x55', '\x42', '\x31', '\x50', '\x72', '\x2e', '\x4d', '\x71', '\x46', '\x4b', '\x69', '\x2d', '\x33', '\x74', '\x78', '\x6a', '\x39', '\x28', '\x41', '\x30', '\x4a', '\x45', '\x76', '\x64', '\x65', '\x6b', '\x2b', '\x29', '\x57', '\x5c', '\x3f', '\x77', '\x5b', '\x53', '\x58', '\x75', '\x4c', '\x2a', '\x7a', '\x63', '\x51', '\x7d', '\x5d', '\x4e', '\x48', '\x7c', '\x5a', '\x73', '\x2c', '\x6f', '\x62', '\x44', '\x4f', '\x6d', '\x79', '\x56', '\x43', '\x49', '\x52'}
        self.__start_state: int = 0
        self.__end_state_set: set = {1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20}
        self.__lexical_symbol_mapping: dict = {
            1: 'single_number',
            2: 'normal_character',
            3: '!symbol_1',
            4: '!symbol_2',
            5: '!symbol_3',
            6: '!symbol_4',
            8: '!symbol_5',
            9: '!symbol_6',
            10: '!symbol_7',
            11: '!symbol_12',
            12: '!symbol_8',
            13: '!symbol_9',
            14: '!symbol_10',
            15: '!symbol_11',
            16: '!symbol_13',
            17: '!symbol_14',
            19: 'reference',
            20: 'escape_character'
        }
        self.__non_greedy_state_set: set = set()
        self.__symbol_function_mapping: dict = {
            'single_number': [],
            'escape_character': [],
            'reference': ['reference'],
            'normal_character': []
        }
        self.__lexical_function: dict = {}

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
            if not get_token and state in self.__compact_move_table:
                for attribute, character_set, range_list, next_state in self.__compact_move_table[state]:
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

    def register_function(self, function_name: str) -> callable:
        def decorator(f: callable):
            self.__lexical_function[function_name] = f
            return f
        return decorator


class BosonGrammarNode:
    def __init__(self):
        self.reduce_number = -1
        self.__data: list = []

    def __getitem__(self, item):
        return self.__data[item]

    def __iadd__(self, other):
        self.__data += other
        return self

    def append(self, item) -> None:
        self.__data.append(item)

    def insert(self, index, item) -> None:
        self.__data.insert(index, item)

    def data(self) -> list:
        return self.__data


class BosonGrammar:
    def __init__(self):
        self.__grammar_tree: (BosonGrammarNode, None) = None
        self.__error_index: int = -1
        self.__no_error_index: int = -1

    def get_grammar_tree(self) -> (BosonGrammarNode, None):
        return self.__grammar_tree

    def set_grammar_tree(self, grammar_tree: BosonGrammarNode) -> None:
        self.__grammar_tree = grammar_tree

    grammar_tree = property(get_grammar_tree, set_grammar_tree)

    def get_error_index(self) -> int:
        return self.__error_index

    def set_error_index(self, error_index: int) -> None:
        self.__error_index = error_index

    error_index = property(get_error_index, set_error_index)

    def no_error_index(self) -> int:
        return self.__no_error_index


class RegularParser:
    def __init__(self):
        self.__terminal_index_mapping: dict = {
            '!symbol_14': 0,
            'single_number': 1,
            '!symbol_13': 2,
            '!symbol_7': 3,
            'normal_character': 4,
            '$': 5,
            '!symbol_11': 6,
            '!symbol_3': 7,
            'escape_character': 8,
            '!symbol_12': 9,
            '!symbol_1': 10,
            '!symbol_10': 11,
            '!symbol_2': 12,
            '!symbol_5': 13,
            'reference': 14,
            '!symbol_6': 15,
            '!symbol_4': 16,
            '!symbol_8': 17,
            '!symbol_9': 18
        }
        self.__sparse_action_table: dict = {
            0: {1: 's16', 4: 's15', 7: 's10', 8: 's13', 12: 's1', 14: 's14', 15: 's8'},
            1: {1: 'r10', 3: 'r10', 4: 'r10', 5: 'r10', 6: 'r10', 7: 'r10', 8: 'r10', 9: 'r10', 10: 'r10', 11: 'r10', 12: 'r10', 14: 'r10', 15: 'r10', 18: 'r10'},
            2: {5: 'a'},
            3: {1: 'r19', 3: 'r19', 4: 'r19', 5: 'r19', 6: 'r19', 7: 'r19', 8: 'r19', 9: 'r19', 10: 'r19', 11: 'r19', 12: 'r19', 14: 'r19', 15: 'r19', 18: 'r19'},
            4: {5: 'r7'},
            5: {1: 'r36', 3: 'r36', 4: 'r36', 5: 'r36', 6: 'r36', 7: 'r36', 8: 'r36', 9: 'r36', 10: 'r36', 11: 'r36', 12: 'r36', 14: 'r36', 15: 'r36', 18: 'r36'},
            6: {3: 'r8', 5: 'r8', 10: 'r8'},
            7: {1: 's16', 3: 'r1', 4: 's15', 5: 'r1', 7: 's10', 8: 's13', 10: 'r1', 12: 's1', 14: 's14', 15: 's8'},
            8: {1: 's16', 4: 's15', 7: 's10', 8: 's13', 12: 's1', 14: 's14', 15: 's8'},
            9: {1: 'r29', 3: 'r29', 4: 'r29', 5: 'r29', 7: 'r29', 8: 'r29', 10: 'r29', 12: 'r29', 14: 'r29', 15: 'r29'},
            10: {1: 'r26', 4: 'r26', 8: 'r26', 16: 's37'},
            11: {1: 'r22', 3: 'r22', 4: 'r22', 5: 'r22', 6: 'r22', 7: 'r22', 8: 'r22', 9: 'r22', 10: 'r22', 11: 'r22', 12: 'r22', 14: 'r22', 15: 'r22', 18: 'r22'},
            12: {1: 'r27', 3: 'r27', 4: 'r27', 5: 'r27', 6: 's22', 7: 'r27', 8: 'r27', 9: 's20', 10: 'r27', 11: 's23', 12: 'r27', 14: 'r27', 15: 'r27', 18: 's21'},
            13: {1: 'r39', 3: 'r39', 4: 'r39', 5: 'r39', 6: 'r39', 7: 'r39', 8: 'r39', 9: 'r39', 10: 'r39', 11: 'r39', 12: 'r39', 13: 'r39', 14: 'r39', 15: 'r39', 18: 'r39'},
            14: {1: 'r40', 3: 'r40', 4: 'r40', 5: 'r40', 6: 'r40', 7: 'r40', 8: 'r40', 9: 'r40', 10: 'r40', 11: 'r40', 12: 'r40', 14: 'r40', 15: 'r40', 18: 'r40'},
            15: {1: 'r24', 3: 'r24', 4: 'r24', 5: 'r24', 6: 'r24', 7: 'r24', 8: 'r24', 9: 'r24', 10: 'r24', 11: 'r24', 12: 'r24', 13: 'r24', 14: 'r24', 15: 'r24', 17: 'r24', 18: 'r24'},
            16: {1: 'r41', 3: 'r41', 4: 'r41', 5: 'r41', 6: 'r41', 7: 'r41', 8: 'r41', 9: 'r41', 10: 'r41', 11: 'r41', 12: 'r41', 13: 'r41', 14: 'r41', 15: 'r41', 17: 'r41', 18: 'r41'},
            17: {1: 'r5', 3: 'r5', 4: 'r5', 5: 'r5', 7: 'r5', 8: 'r5', 10: 'r5', 12: 'r5', 14: 'r5', 15: 'r5'},
            18: {1: 'r37', 3: 'r37', 4: 'r37', 5: 'r37', 7: 'r37', 8: 'r37', 10: 'r37', 12: 'r37', 14: 'r37', 15: 'r37'},
            19: {1: 'r20', 3: 'r20', 4: 'r20', 5: 'r20', 7: 'r20', 8: 'r20', 10: 'r20', 12: 'r20', 14: 'r20', 15: 'r20'},
            20: {1: 's27', 2: 'r25'},
            21: {1: 'r21', 3: 'r21', 4: 'r21', 5: 'r21', 7: 'r21', 8: 'r21', 10: 'r21', 12: 'r21', 14: 'r21', 15: 'r21'},
            22: {1: 'r28', 3: 'r28', 4: 'r28', 5: 'r28', 7: 'r28', 8: 'r28', 10: 'r28', 12: 'r28', 14: 'r28', 15: 'r28'},
            23: {1: 'r33', 3: 'r33', 4: 'r33', 5: 'r33', 7: 'r33', 8: 'r33', 10: 'r33', 12: 'r33', 14: 'r33', 15: 'r33'},
            24: {2: 'r17'},
            25: {2: 'r15'},
            26: {0: 'r35', 1: 's34', 2: 'r35'},
            27: {0: 'r16', 1: 'r16', 2: 'r16'},
            28: {2: 's29'},
            29: {0: 'r14', 1: 's27'},
            30: {0: 'r38'},
            31: {0: 's33'},
            32: {0: 'r2'},
            33: {1: 'r18', 3: 'r18', 4: 'r18', 5: 'r18', 7: 'r18', 8: 'r18', 10: 'r18', 12: 'r18', 14: 'r18', 15: 'r18'},
            34: {0: 'r11', 1: 'r11', 2: 'r11'},
            35: {1: 's16', 4: 's15', 8: 's13'},
            36: {1: 'r42', 4: 'r42', 8: 'r42'},
            37: {1: 'r23', 4: 'r23', 8: 'r23'},
            38: {1: 'r22', 4: 'r22', 8: 'r22', 13: 'r22', 17: 's44'},
            39: {1: 's16', 4: 's15', 8: 's13', 13: 's42'},
            40: {1: 'r3', 4: 'r3', 8: 'r3', 13: 'r3'},
            41: {1: 'r9', 4: 'r9', 8: 'r9', 13: 'r9'},
            42: {1: 'r31', 3: 'r31', 4: 'r31', 5: 'r31', 6: 'r31', 7: 'r31', 8: 'r31', 9: 'r31', 10: 'r31', 11: 'r31', 12: 'r31', 14: 'r31', 15: 'r31', 18: 'r31'},
            43: {1: 'r12', 4: 'r12', 8: 'r12', 13: 'r12'},
            44: {1: 's16', 4: 's15'},
            45: {1: 'r34', 4: 'r34', 8: 'r34', 13: 'r34'},
            46: {3: 's51'},
            47: {3: 'r13', 5: 'r13', 10: 's49'},
            48: {3: 'r4', 5: 'r4', 10: 'r4'},
            49: {1: 's16', 4: 's15', 7: 's10', 8: 's13', 12: 's1', 14: 's14', 15: 's8'},
            50: {3: 'r6', 5: 'r6', 10: 'r6'},
            51: {1: 'r30', 3: 'r30', 4: 'r30', 5: 'r30', 6: 'r30', 7: 'r30', 8: 'r30', 9: 'r30', 10: 'r30', 11: 'r30', 12: 'r30', 14: 'r30', 15: 'r30', 18: 'r30'},
            52: {1: 'r32', 3: 'r32', 4: 'r32', 5: 'r32', 7: 'r32', 8: 'r32', 10: 'r32', 12: 'r32', 14: 'r32', 15: 'r32'}
        }
        self.__sparse_goto_table: dict = {
            0: {1: 5, 2: 6, 5: 3, 14: 4, 17: 7, 18: 9, 19: 11, 20: 12, 23: 2},
            6: {7: 47},
            7: {1: 5, 5: 3, 18: 52, 19: 11, 20: 12},
            8: {1: 5, 2: 6, 5: 3, 14: 46, 17: 7, 18: 9, 19: 11, 20: 12},
            10: {4: 36, 10: 35},
            12: {8: 19, 21: 17, 22: 18},
            20: {0: 24, 12: 26, 13: 28, 15: 25},
            29: {11: 31, 12: 26, 15: 32, 16: 30},
            35: {3: 39, 5: 40, 9: 41, 19: 38},
            39: {5: 40, 9: 43, 19: 38},
            44: {19: 45},
            47: {24: 48},
            49: {1: 5, 2: 50, 5: 3, 17: 7, 18: 9, 19: 11, 20: 12}
        }
        self.__sentence_index_grammar_tuple_mapping: dict = {
            35: ('*0',),
            11: ('*0', '1'),
            18: ('*1', '*3'),
            2: ('0',),
            15: ('0',),
            14: (),
            38: ('*0',),
            25: (),
            17: ('*0',),
            34: ('0', '2'),
            40: ('0',),
            30: ('1',),
            31: ('*1', '2'),
            23: ('0',),
            12: ('*0', '1'),
            26: (),
            42: ('*0',),
            10: ('0',),
            36: ('0',),
            19: ('0',),
            5: ('0', '*1'),
            20: ('0',),
            27: (),
            37: ('*0',),
            1: ('*0',),
            32: ('*0', '1'),
            13: ('0', '*1'),
            6: ('1',),
            8: (),
            4: ('*0', '*1'),
            7: ('0',)
        }
        self.__reduce_symbol_count: list = [1, 1, 1, 1, 2, 2, 2, 1, 0, 1, 1, 2, 2, 2, 0, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 3, 4, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1]
        self.__reduce_non_terminal_index: list = [6, 2, 16, 9, 7, 18, 24, 23, 7, 3, 20, 12, 3, 14, 11, 0, 12, 13, 8, 20, 22, 8, 5, 4, 19, 13, 10, 21, 8, 17, 1, 1, 17, 8, 9, 15, 20, 21, 11, 5, 1, 19, 10]

    def parse(self, token_list: list) -> BosonGrammar:
        grammar = BosonGrammar()
        analysis_stack = [0]
        symbol_stack = []
        token_index = 0
        while token_index < len(token_list):
            token = token_list[token_index]
            current_state = analysis_stack[-1]
            operation = self.__sparse_action_table.get(current_state, {}).get(self.__terminal_index_mapping[token.symbol], 'e')
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
                statement_index = int(operation[1:])
                reduce_count = self.__reduce_symbol_count[statement_index]
                for _ in range(reduce_count):
                    analysis_stack.pop()
                current_state = analysis_stack[-1]
                current_non_terminal_index = self.__reduce_non_terminal_index[statement_index]
                goto_next_state = self.__sparse_goto_table.get(current_state, {}).get(current_non_terminal_index, -1)
                if goto_next_state == -1:
                    raise ValueError('Invalid goto action: state={}, non-terminal={}'.format(current_state, current_non_terminal_index))
                analysis_stack.append(goto_next_state)
                if statement_index in self.__sentence_index_grammar_tuple_mapping:
                    symbol_package = []
                    for _ in range(reduce_count):
                        symbol_package.insert(0, symbol_stack.pop())
                    grammar_node = BosonGrammarNode()
                    for node in self.__sentence_index_grammar_tuple_mapping[statement_index]:
                        if node[0] == '*':
                            grammar_node += symbol_package[int(node[1:])]
                        else:
                            grammar_node.append(symbol_package[int(node)])
                    grammar_node.reduce_number = statement_index
                    symbol_stack.append(grammar_node)
                elif statement_index in {0, 33, 3, 39, 9, 41, 16, 21, 22, 24, 28, 29}:
                    grammar_node = BosonGrammarNode()
                    for _ in range(reduce_count):
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


class RegularInterpreter:
    def __init__(self):
        self.__reduce_number_grammar_name_mapping: dict = {
            7: 'regular_expression',
            13: 'expression',
            1: 'branch',
            5: 'group',
            19: 'simple_construct',
            36: 'complex_construct',
            10: 'wildcard_character',
            31: 'select',
            30: 'sub_expression',
            40: 'reference',
            18: 'count_range',
            35: 'construct_number'
        }
        self.__naive_reduce_number_set: set = {33, 3, 36, 39, 40, 7, 10, 41, 19, 21, 22, 24, 28}
        self.__semantic_action_mapping: dict = {}

    def __semantic_analysis(self, grammar_tree: BosonGrammarNode):
        if grammar_tree.reduce_number in self.__reduce_number_grammar_name_mapping:
            grammar_name = self.__reduce_number_grammar_name_mapping[grammar_tree.reduce_number]
        else:
            grammar_name = '!grammar_hidden'
        semantic_node_list = []
        for grammar_node in grammar_tree.data():
            if isinstance(grammar_node, BosonGrammarNode):
                semantic_node = self.__semantic_analysis(grammar_node)
            else:
                semantic_node = grammar_node
            semantic_node_list.append(semantic_node)
        if grammar_name in self.__semantic_action_mapping:
            return self.__semantic_action_mapping[grammar_name](semantic_node_list)
        elif grammar_tree.reduce_number in self.__naive_reduce_number_set:
            if len(semantic_node_list) == 0:
                return None
            elif len(semantic_node_list) == 1:
                return semantic_node_list[0]
            else:
                return semantic_node_list
        else:
            return semantic_node_list

    def execute(self, grammar_tree: BosonGrammarNode):
        return self.__semantic_analysis(grammar_tree)

    def register_action(self, name: str) -> callable:
        def decorator(f: callable):
            self.__semantic_action_mapping[name] = f
            return f
        return decorator
