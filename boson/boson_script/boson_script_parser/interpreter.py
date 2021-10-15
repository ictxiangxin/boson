from typing import Dict, Set

from .semantic_node import BosonSemanticsNode
from .grammar_node import BosonGrammarNode


class BosonInterpreter:
    def __init__(self):
        self.__reduce_number_grammar_name_mapping: Dict[int, str] = {
            36: 'command',
            20: 'lexical_define',
            88: 'reduce',
            29: 'getter_tuple',
            6: 'grammar_node',
            53: 'name_closure',
            95: 'literal',
            13: 'complex_closure',
            89: 'complex_optional',
            87: 'select',
            16: 'attribute',
            77: 'string',
            54: 'number',
            64: 'attribute_value_list'
        }
        self.__naive_reduce_number_set: Set[int] = {4, 12, 14, 24, 28, 30, 42, 44, 45, 52, 54, 57, 59, 67, 77, 81, 83, 90, 93, 95}
        self.__semantic_action_mapping: Dict[str, callable] = {}

    def __semantics_analysis(self, grammar_tree: BosonGrammarNode) -> BosonSemanticsNode:
        if grammar_tree.get_reduce_number() in self.__reduce_number_grammar_name_mapping:
            grammar_name: str = self.__reduce_number_grammar_name_mapping[grammar_tree.get_reduce_number()]
        else:
            grammar_name: str = '!grammar_hidden'
        semantic_node = BosonSemanticsNode()
        if len(grammar_tree.children()) == 0:
            semantic_node.set_reduce_number(grammar_tree.get_reduce_number())
            semantic_node.set_text(grammar_tree.get_text())
        else:
            for grammar_node in grammar_tree.children():
                semantic_node.append(self.__semantics_analysis(grammar_node))
        if grammar_name in self.__semantic_action_mapping:
            return self.__semantic_action_mapping[grammar_name](semantic_node)
        elif grammar_tree.get_reduce_number() in self.__naive_reduce_number_set:
            if len(semantic_node.children()) == 0:
                return BosonSemanticsNode.null_node()
            elif len(semantic_node.children()) == 1:
                return semantic_node[0]
            else:
                return semantic_node
        else:
            return semantic_node

    def execute(self, grammar_tree: BosonGrammarNode) -> BosonSemanticsNode:
        return self.__semantics_analysis(grammar_tree)

    def register_action(self, name: str) -> callable:
        def decorator(f: callable):
            self.__semantic_action_mapping[name] = f
            return f
        return decorator
