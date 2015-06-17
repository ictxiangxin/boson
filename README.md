#Boson  - grammar analyzer generator

[![Build Status](https://travis-ci.org/ictxiangxin/boson.svg?branch=master)](https://travis-ci.org/ictxiangxin/boson)

[![Join the chat at https://gitter.im/ictxiangxin/ict-boson](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ictxiangxin/ict-boson?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

v0.5

Boson can use production sentences given by the user to generate grammar analyzer code.

> Only support Python3.

* * *

##How to install boson?

You just need download the ZIP file, and unZIP it, type the command:
 `python3 setup.py install` or `sudo python3 setup.py install`

Or Clone it from Github:

`git clone https://github.com/ictxiangxin/boson`

* * *

##Usage

Boson read file contains a set of productions, and each production form is:

```
name : <name combination> [code] | <name combination> [code] | ... ;
```

There is a convention which must exist a non-terminal named "start"

`[code]` is not necessary.

**Notice**

`name` satisfied `[_a-zA-Z][_a-zA-Z0-0]*`

`code` satisfied `\{.*\}`

A example of arithmetic grammar like this:

```
start : E ;
E : E plus T | E minus T | T ;
T : T times F | T div F | F ;
F : F power D | D ;
D : bl E br | N ;
N : int | float ;
```

Add you can write literal terminal like this:

```
start : E ;
E : E '+' T | E '-' T | T ;
T : T '*' F | T '/' F | F ;
F : F '^' D | D ;
D : '(' E ')' | N ;
N : int | float ;
```

> NOTICE: The null reduce production present as "~" (without quotation marks) or write nothing.

There are some command can add to grammar file, these commands start with "%", the form is:

```
%command argument1 argument2 ...
```

The command can be: `grammar_analyzer_name`, `lexical_analyzer_name`, `symbol_stack`, `generate_comment`, `start_symbol`,
 `have_line_number`, `symbol_type`.

`grammar_analyzer_name`, set the grammar analyzer name.

`lexical_analyzer_name`, set the lexical analyzer name.

`symbol_stack`, set the symbol stack variable name.

`generate_comment`, set whether generate reduce comment in code.

`start_symbol`, set the start non-terminal literal.

`have_line_number`, tell boson lexer can give line number.

`symbol_type`, set symbol type which will shift to symbol stack.

And you can add some static code, named "section" in boson, each section have a name, and have prefix "@",
 the code lines start with "@@" and end with "@@", the form is:

```
@section_name
@@
your code here
@@
```

The section name can be the following types:
`initial`, `ending`, `extends`.

`initial`, these code will be inserted to the initial block of grammar analyzer.

`ending`, these code will be inserted to the end of grammar analyzer, it is used to return some things or
 postprocess at the end.

`extends`, these code are extends code, these code will bed inserted at the end of file.

Write these productions to one file.

> You can consult the example at "example/arithmetic_grammar.txt"

###Easy to use

> Use boson.py to generate code.

You can execute boson.py by "python3 boson.py" in linux or "python boson.py" in windows.
So that you can see the usage of boson.py.

The usage of boson.py is:

```
boson.py [grammar file]
         -t/type <type>
         -m/mode <ebnf mode>
         -o/output <code file>
         -a/analyzer <analyzer>
         -c/code <code>
         -l/lexical <lexical file>
         -r/report
         -f/force
```

`\[grammar file\]` is the file contains grammar description.

`-t/type <type>` point grammar file is bnf or ebnf.

`-m/mode` the mode when handle ebnf file.

`-o/output <code file>` is analyzer code file which generated by boson.

`-a/analyzer <analyzer>` is the type of analyzer.

`-c/code <code>` is the language of generated code.

`-l/lexical <lexical file>` is the lexical description for lexical analysis.

`-r/report` tell boson report conflict when generate grammar analyzer.

`-f/force` tell boson generate grammar analyzer even exist conflict.

You can input `boson.py -h` to get the full help.

####Example

use "example/arithmetic_grammar.txt" to generate "example/arithmetic_grammar_code.py":

```
boson.py example/arithmetic_grammar.txt -a SLR -l Python -o example/arithmetic_grammar_code.py
```

###Use boson as library

You can use boson as library, just import boson code file.

Of course, you can install the python package, and just import boson module.

Example:

```python
    >>> from boson.bs_grammar_analysis import bs_token_list
    >>> from boson.bs_lalr_generate.py import bs_lalr_generate_table
    >>> from boson.bs_code_generate import bs_generate_python_code
    >>> data_package = bs_grammar_analysis("example/arithmetic_grammar.txt")
    >>> lalr_table = bs_lalr_generate_table(data_package["sentence set"])
    >>> bs_generate_python_code(lalr_table, data_package)
    *** Here you will get the code of LALR grammar analyzer of grammar, which described ***
    *** in "example/arithmetic_grammar.txt" file.                                       ***
```

####Parse grammar file

"bs_grammar_analysis.py" file contains functions are used to parse grammar file.

**bs_token_list()** function read grammar file and return a token list.

```python
token_list = bs_token_list(grammar_file)
```

**bs_grammar_analyzer()** function use token list to generate production sentence set, reduce code
 and some other content as a dict named data_package for each sentence.

```python
data_package = bs_grammar_analyzer(token_list)
```

Now, the final result of "bs_grammar_analysis.py" is data_package, which contains many things used by generator
 and analyzer.

####Generate analyzer table

Use sentence list to generate analyzer table, just import corresponding generator file of one analyzer type.

For example, if we want to generate SLR analyzer, import "bs_slr_generate.py".

**bs_slr_generate_table()** function use sentence list to create all tables used by analyzer(DFA).
It returns a tuple, which contains these tables.

```python
tables_tuple = bs_slr_generate_table(sentence_list)
```

####Generate analyzer code

All code generator use analyzer table to generate code of grammar analyzer.

> Import "bs_code_generate.py" file, which include code generators of all languages.

Each generator is a function, now, I am already finished Python3 code generator, and it definition is:

#####Python3 code generator definition

`bs_generate_python_code(analyzer_table, data_package, lex=None, output=sys.stdout)`

**analyzer_table** is grammar analyzer tables, which output by SLR, LR, or LALR generator.

**data_package** is a dict contains reduce code, literal and many other things.

**lex** is the simple lexical analyzer (is a Class) provided by boson, default is None.

**output** is the output file handle, default is stdout, which will output code on screen.

#####With lexical analyzer

Boson provide a simple lexical analyzer, you can use it by `import boson.bs_lexical_analyzer`.
And just instantiate Class BosonLexicalAnalyzer.
It will read a lexical description file, which each line described one token and its regular expression.

The format is:

```
"regular expression here"  token_name ;
```

Or

```
token_name "regular expression here" ;
```

And you can use some command, the command form is:

```
%command argument1 argument2 ... ;
```

There are 2 commands can use: `ignore`, `error`.

`ignore` can set the ignore set for lexical analyzer.

`error` can set the error set for lexical analyzer.

**For example**

"lex.txt":

```
%ignore skip ;
"[_a-zA-Z][_a-zA-Z0-9]*" name ;
"\r\n|\n"                newline ;
" \t"                    skip ;
"."                      invalid ;
```

When you create this file, now, you can instantiate Class BosonLexicalAnalyzer by:

```python
mylex = BosonLexicalAnalyzer("lex.txt", ignore=("skip"), error=("invalid"))
```

`ignore` and `error` are not necessary, so you can create lexical analyzer just like this:

``` python
mylex = BosonLexicalAnalyzer("lex.txt")
```

Now, you can use `mylex` by invoke its `tokenize()` function.
And you also can use it to generate simple lexical analyzer code by give it to code generator.

#####Without lexical analyzer

```python
fp = open("my_analyzer.py", "w")
bs_generate_python_code(tables_tuple, reduce_code, literal, output=fp)
fp.close()
```

#####With lexical analyzer

```python
fp = open("my_analyzer.py", "w")
mylex = BosonLexicalAnalyzer("lex.txt")
bs_generate_python_code(tables_tuple, reduce_code, literal, lex=mylex, output=fp)
fp.close()
```

If you do not provide any file handle, the default value is **sys.stdout**, it may print all codes on screen.

```python
bs_generate_python_code(tables_tuple, reduce_code, literal)
```

####EBNF translate to BNF

You needn't write BNF line by line, just write more simpler form: EBNF.

So, boson provide a function, which can translate EBNF to BNF.

`import boson.bs_ebnf_to_bnf`

If you want to get the BNF output, just invoke function `bs_ebnf_to_bnf`, like this:

```python
from boson.bs_ebnf_to_bnf import bs_ebnf_to_bnf
fp = open("bnf.txt", "r")
bs_ebnf_to_bnf("ebnf.txt", fp)
fp.close()
```

If you just want get the BNF sentence set, invoke function `bs_ebnf_to_sentence_set`, like this:

```python
from boson.bs_ebnf_to_bnf import bs_ebnf_to_bnf
sentence_set = bs_ebnf_to_sentence_set("ebnf.txt")
```

* * *

##Reference

Boson can generate SLR, LR, LALR analyzer.

All analyzer input is `sentence_set`, which created by `bs_grammar_analysis.py`.

They all have a `dfa generate function` and `table generate function`.

`dfa generate function` returns `state_list` and `state_transfer`.

`table generate function` returns `terminal_index`, `non_terminal_index`,
 `action_table`, `goto_table`, `reduce_symbol_sum`, `reduce_to_non_terminal`, `sentence_list`.

###SLR - Simple LR

SLR in boson means SLR(1), it is fast and simple, but it only can recognize a few grammars.

> boson.bs_slr_generate

`bs_slr_generate_dfa(sentence_set)` function can generate SLR DFA.

`bs_slr_generate_table(sentence_set)` function can generate SLR table.

###LR - canonical LR

LR in boson means LR(1), it is slower than SLR, but can recognize more grammar. And its table will bigger than SLR.

> boson.bs_lr_generate

`bs_lr_generate_dfa(sentence_set)` function can generate LR DFA.

`bs_lr_generate_table(sentence_set)` function can generate LR table.

###LALR - Look-Ahead LR

LALR in boson means LALR(1), it is slow like LR, and can recognize more grammar than SLR, but less than LR.
The feature is that its table size is the same as SLR.

> boson.bs_lalr_generate

`bs_lalr_generate_dfa(sentence_set)` function can generate LALR DFA.

`bs_lalr_generate_table(sentence_set)` function can generate LALR table.

* * *

##Author

Author: ict

Email: ictxiangxin@gmail.com

Email: ictxiangxin@hotmail.com
