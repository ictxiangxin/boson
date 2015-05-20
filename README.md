#Boson  - grammar analyzer generator

[![Build Status](https://travis-ci.org/ictxiangxin/boson.svg?branch=master)](https://travis-ci.org/ictxiangxin/boson)

v0.3

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
start : E
E : E plus T | E minus T | T ;
T : T times F | T div F | F ;
F : F power D | D ;
D : bl E br | N ;
N : int | float ;
```

Add you can write literal terminal like this:

```
start : E
E : E '+' T | E '-' T | T ;
T : T '*' F | T '/' F | F ;
F : F '^' D | D ;
D : '(' E ')' | N ;
N : int | float ;
```

Write these productions to one file.

###Easy to use

> Use boson.py to generate code.

You can execute boson.py by "python3 boson.py" in linux or "python boson.py" in windows.
So that you can see the usage of boson.py.

The usage of boson.py is:

```
boson.py [grammar file] -o/output <code file> -a/analyzer <analyzer> -l/language <language>
```

`\[grammar file\]` is the file contains grammar description.

`-o/output <code file>` is analyzer code file which gernerated by boson.

`-a/analyzer <analyzer>` is the type of analyzer.

`-l/language <language>` is the language of generated code.

####Example

use "example/arithmetic_grammar.txt" to generate "example/arithmetic_grammar_code.py":

```
boson.py example/arithmetic_grammar.txt -a SLR -l Python -o example/arithmetic_grammar_code.py
```

###Use boson as library

You can use boson as library, just import boson code file.

Of course, you can install the python package, and just import boson module.

Example:

    >>> from boson.bs_grammar_analysis import bs_token_list
    >>> from boson.bs_lalr_generate.py import bs_lalr_generate_table
    >>> from boson.bs_code_generate import bs_generate_python_code
    >>> sentence_set, reduce_code = bs_grammar_analysis("example/arithmetic_grammar.txt")
    >>> lalr_table = bs_lalr_generate_table(sentence_set)
    >>> bs_generate_python_code(lalr_table, reduce_code)
    *** Here you will get the code of LALR grammar analyzer of grammar, which described ***
    *** in "example/arithmetic_grammar.txt" file.                                       ***

####Parse grammar file

"bs_grammar_analysis.py" file contains functions are used to parse grammar file.

**bs_token_list()** function read grammar file and return a token list.

```python
token_list = bs_token_list(grammar_file)
```

**bs_grammar_analyzer()** function use token list to generate production sentence set and reduce code for each sentence.

```python
sentence_set, reduce_code = bs_grammar_analyzer(token_list)
```

Now, the final result of "bs_grammar_analysis.py" is sentence list.

####Generate analyzer table

Use sentence list to generate analyer table, just import corresponding generator file of one analyzer type.

For example, if we want to generate SLR analyzer, import "bs_slr_generate.py".

**bs_slr_generate_table()** function use sentence list to create all tables used by analyzer(DFA).
It returns a tuple, which contains these tables.

```python
tables_tuple = bs_slr_generate_table(sentence_list)
```

####Generate analyzer code

All code generator use analyzer table to generate code of grammar analyzer.

Import "bs_code_generate.py" file, which include code generators of all languages.

Each generator is a function, the first argument is analyzer tables and the second argument is file handle.
So, you need open a file first, and analyzer code may saved in this file.

```python
fp = open("my_analyzer.py", "w")
bs_generate_python_code(tables_tuple, reduce_code, output=fp)
fp.close()
```

If you do not provide any file handle, the default value is **sys.stdout**, it may print all codes on screen.

```python
bs_generate_python_code(tables_tuple, reduce_code)
```

* * *

##Reference

Boson can generate SLR, LR, LALR analyzer.

###SLR - Simple LR

> boson.bs_slr_generate

`bs_slr_generate_dfa(sentence_set)` function can generate SLR DFA, it return `state_list` and `state_transfer`.

`bs_slr_generate_table(sentence_set)` function can generate SLR table, it return `terminal_index`, `non_terminal_index`,
 `action_table`, `goto_table`, `reduce_symbol_sum`, `reduce_to_non_terminal`, `sentence_list`.

* * *

##Author

Author: ict

Email: ictxiangxin@gmail.com

Email: ictxiangxin@hotmail.com
