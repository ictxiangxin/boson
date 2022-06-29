option = {
    'mode': 'integration',
    'parser': {
        'start_symbol': 'start',
        'analyzer': 'lalr',
        'conflict_resolver': {
            'enable': 'False',
            'shift_reduce': 'order',
            'reduce_reduce': 'order',
        },
    },
    'code': {
        'checker': 'False',
        'language': 'python',
        'generator': {
            'lexer': 'True',
            'interpreter': 'True',
            'comment': 'True',
        },
        'lexer': {
            'unicode': 'False',
            'compact_table': 'True',
        },
        'parser': {
            'sparse_table': 'True',
        },
        'class_name': {
            'token': 'BosonToken',
            'lexer': 'BosonLexer',
            'parser': 'BosonParser',
            'grammar': 'BosonGrammar',
            'grammar_node': 'BosonGrammarNode',
            'interpreter': 'BosonInterpreter',
            'semantic_node': 'BosonSemanticsNode',
        }
    }
}
