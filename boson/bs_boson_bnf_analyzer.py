"""
    Boson v0.6

        Author: ict
        Email:  ictxiangxin@gmail.com

    This code was generated by boson python code generator.
        
         0: start -> grammar
         1: derivation -> derivation_body
         2: derivation -> derivation_body grammar_tuple
         3: derivation_body -> element_list
         4: derivation_body -> null
         5: derivation_body -> ~
         6: derivation_list -> derivation
         7: derivation_list -> derivation_list or derivation
         8: element -> literal
         9: element -> name
        10: element_list -> element
        11: element_list -> element_list element
        12: grammar -> grammar statement
        13: grammar -> statement
        14: grammar_tuple -> bracket_l node_list bracket_r
        15: node_list -> node
        16: node_list -> node_list comma node
        17: reduction_statement -> name reduce derivation_list end
        18: command_statement -> command element_list end
        19: statement -> command_statement
        20: statement -> lexical_statement
        21: statement -> reduction_statement
"""


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


class BosonBNFAnalyzer:
    def __init__(self):
        self.__terminal_index = {
            "command": 3,
            "bracket_r": 1,
            "reduce": 11,
            "lexical_statement": 5,
            "null": 9,
            "node": 8,
            "literal": 6,
            "comma": 2,
            "or": 10,
            "$": 12,
            "name": 7,
            "bracket_l": 0,
            "end": 4
        }
        self.__action_table = [
            ["e", "e", "e", "s1", "e", "s6", "e", "s5", "e", "e", "e", "e", "e"],
            ["e", "e", "e", "e", "e", "e", "s8", "s10", "e", "e", "e", "e", "e"],
            ["e", "e", "e", "r19", "e", "r19", "e", "r19", "e", "e", "e", "e", "r19"],
            ["e", "e", "e", "r21", "e", "r21", "e", "r21", "e", "e", "e", "e", "r21"],
            ["e", "e", "e", "r13", "e", "r13", "e", "r13", "e", "e", "e", "e", "r13"],
            ["e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "s12", "e"],
            ["e", "e", "e", "r20", "e", "r20", "e", "r20", "e", "e", "e", "e", "r20"],
            ["e", "e", "e", "s1", "e", "s6", "e", "s5", "e", "e", "e", "e", "a"],
            ["r8", "e", "e", "e", "r8", "e", "r8", "r8", "e", "e", "r8", "e", "e"],
            ["e", "e", "e", "e", "s14", "e", "s8", "s10", "e", "e", "e", "e", "e"],
            ["r9", "e", "e", "e", "r9", "e", "r9", "r9", "e", "e", "r9", "e", "e"],
            ["r10", "e", "e", "e", "r10", "e", "r10", "r10", "e", "e", "r10", "e", "e"],
            ["r5", "e", "e", "e", "r5", "e", "s8", "s10", "e", "s20", "r5", "e", "e"],
            ["e", "e", "e", "r12", "e", "r12", "e", "r12", "e", "e", "e", "e", "r12"],
            ["e", "e", "e", "r18", "e", "r18", "e", "r18", "e", "e", "e", "e", "r18"],
            ["r11", "e", "e", "e", "r11", "e", "r11", "r11", "e", "e", "r11", "e", "e"],
            ["e", "e", "e", "e", "s21", "e", "e", "e", "e", "e", "s22", "e", "e"],
            ["e", "e", "e", "e", "r6", "e", "e", "e", "e", "e", "r6", "e", "e"],
            ["r3", "e", "e", "e", "r3", "e", "s8", "s10", "e", "e", "r3", "e", "e"],
            ["s23", "e", "e", "e", "r1", "e", "e", "e", "e", "e", "r1", "e", "e"],
            ["r4", "e", "e", "e", "r4", "e", "e", "e", "e", "e", "r4", "e", "e"],
            ["e", "e", "e", "r17", "e", "r17", "e", "r17", "e", "e", "e", "e", "r17"],
            ["r5", "e", "e", "e", "r5", "e", "s8", "s10", "e", "s20", "r5", "e", "e"],
            ["e", "e", "e", "e", "e", "e", "e", "e", "s27", "e", "e", "e", "e"],
            ["e", "e", "e", "e", "r2", "e", "e", "e", "e", "e", "r2", "e", "e"],
            ["e", "e", "e", "e", "r7", "e", "e", "e", "e", "e", "r7", "e", "e"],
            ["e", "s29", "s28", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e"],
            ["e", "r15", "r15", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e"],
            ["e", "e", "e", "e", "e", "e", "e", "e", "s30", "e", "e", "e", "e"],
            ["e", "e", "e", "e", "r14", "e", "e", "e", "e", "e", "r14", "e", "e"],
            ["e", "r16", "r16", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e"]
        ]
        self.__goto_table = [
            [2, -1, -1, -1, -1, -1, 7, -1, -1, 3, 4],
            [-1, -1, -1, -1, 11, 9, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [2, -1, -1, -1, -1, -1, -1, -1, -1, 3, 13],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 17, 19, 16, 11, 18, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, 24, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 25, 19, -1, 11, 18, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 26, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]
        self.__reduce_symbol_sum = [0, 1, 2, 1, 1, 0, 1, 3, 1, 1, 1, 2, 2, 1, 3, 1, 3, 4, 3, 1, 1, 1]
        self.__reduce_to_non_terminal_index = [0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 8, 8, 9, 0, 10, 10, 10]

    def grammar_analysis(self, token_list):
        grammar = BosonGrammar()
        analysis_stack = [0]
        symbol_stack = []
        token_index = 0
        while token_index < len(token_list):
            token = token_list[token_index]
            current_state = analysis_stack[-1]
            operation = self.__action_table[current_state][self.__terminal_index[token.symbol]]
            operation_flag = operation[0]
            if operation_flag == "e":
                grammar.error_index = token_index
                return grammar
            elif operation_flag == "s":
                operation_number = int(operation[1:])
                analysis_stack.append(operation_number)
                token_index += 1
                symbol_stack.append(token.text)
            elif operation_flag == "r":
                operation_number = int(operation[1:])
                reduce_sum = self.__reduce_symbol_sum[operation_number]
                for _ in range(reduce_sum):
                    analysis_stack.pop()
                current_state = analysis_stack[-1]
                current_non_terminal_index = self.__reduce_to_non_terminal_index[operation_number]
                goto_next_state = self.__goto_table[current_state][current_non_terminal_index]
                if goto_next_state == -1:
                    raise Exception("Invalid goto action: state=%d, non-terminal=%d" % (current_state, current_non_terminal_index))
                analysis_stack.append(goto_next_state)
                if operation_number == 7:
                    temp_grammar_tuple_list = []
                    real_temp_grammar_tuple_list = []
                    for _ in range(reduce_sum):
                        temp_grammar_tuple_list.insert(0, symbol_stack.pop())
                    for i in ["@", 0, 2]:
                        if i == "@":
                            real_temp_grammar_tuple_list.append(7)
                        else:
                            real_temp_grammar_tuple_list.append(temp_grammar_tuple_list[i])
                    symbol_stack.append(tuple(real_temp_grammar_tuple_list))
                elif operation_number == 17:
                    temp_grammar_tuple_list = []
                    real_temp_grammar_tuple_list = []
                    for _ in range(reduce_sum):
                        temp_grammar_tuple_list.insert(0, symbol_stack.pop())
                    for i in ["@", 0, 2]:
                        if i == "@":
                            real_temp_grammar_tuple_list.append(17)
                        else:
                            real_temp_grammar_tuple_list.append(temp_grammar_tuple_list[i])
                    symbol_stack.append(tuple(real_temp_grammar_tuple_list))
                elif operation_number == 14:
                    temp_grammar_tuple_list = []
                    real_temp_grammar_tuple_list = []
                    for _ in range(reduce_sum):
                        temp_grammar_tuple_list.insert(0, symbol_stack.pop())
                    for i in ["@", 1]:
                        if i == "@":
                            real_temp_grammar_tuple_list.append(14)
                        else:
                            real_temp_grammar_tuple_list.append(temp_grammar_tuple_list[i])
                    symbol_stack.append(tuple(real_temp_grammar_tuple_list))
                elif operation_number == 18:
                    temp_grammar_tuple_list = []
                    real_temp_grammar_tuple_list = []
                    for _ in range(reduce_sum):
                        temp_grammar_tuple_list.insert(0, symbol_stack.pop())
                    for i in ["@", 0, 1]:
                        if i == "@":
                            real_temp_grammar_tuple_list.append(18)
                        else:
                            real_temp_grammar_tuple_list.append(temp_grammar_tuple_list[i])
                    symbol_stack.append(tuple(real_temp_grammar_tuple_list))
                elif operation_number == 16:
                    temp_grammar_tuple_list = []
                    real_temp_grammar_tuple_list = []
                    for _ in range(reduce_sum):
                        temp_grammar_tuple_list.insert(0, symbol_stack.pop())
                    for i in ["@", 0, 2]:
                        if i == "@":
                            real_temp_grammar_tuple_list.append(16)
                        else:
                            real_temp_grammar_tuple_list.append(temp_grammar_tuple_list[i])
                    symbol_stack.append(tuple(real_temp_grammar_tuple_list))
                elif operation_number in [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 19, 20, 21]:
                    temp_grammar_tuple_list = []
                    for _ in range(reduce_sum):
                        temp_grammar_tuple_list.insert(0, symbol_stack.pop())
                    temp_grammar_tuple_list.insert(0, operation_number)
                    symbol_stack.append(tuple(temp_grammar_tuple_list))
                else:
                    raise Exception("Invalid reduce number: reduce=%d" % operation_number)
            elif operation_flag == "a":
                grammar.grammar_tree = symbol_stack[0]
                return grammar
            else:
                raise Exception("Invalid action: action=%s." % operation)
        raise Exception("Analyzer unusual exit.")
