# Boson  - grammar analyzer generator

[![Build Status](https://travis-ci.org/ictxiangxin/boson.svg?branch=master)](https://travis-ci.org/ictxiangxin/boson)

[![Join the chat at https://gitter.im/ictxiangxin/ict-boson](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ictxiangxin/ict-boson?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

v0.9

Boson can use production sentences given by the user to generate grammar analyzer code.

> Only support Python3.

* * *

## How to install boson?

You just need download the ZIP file, and unZIP it, type the command:
 `python3 setup.py install` or `sudo python3 setup.py install`

Or Clone it from Github:

`git clone https://github.com/ictxiangxin/boson`

* * *

## Usage

Boson read file contains a set of productions, and each production form is:

```
name : [derivation] = [grammar name](grammar tuple) | [derivation] = [grammar name](grammar tuple) | ... ;
```

There is a convention which must exist a non-terminal named "start"

`derivation` looks like EBNF, but that is a little different.

`(grammar tuple)` is the AST node structure of this production and it's not necessary.

**Notice**

`name` satisfied `[_a-zA-Z][_a-zA-Z0-0]*`

`(grammar tuple)` satisfied `($$, $0, $1, ...)`

`$$, $0, $1, ...` has special meaning:

* `$$`, the number of this production.
* `$0 $1 $2 ...`, the index of element of this production(base-0).

> You can unpack one non-terminal by `*`.
Example:
```
list : packed text = ($0, $1);
packed : text text = ($0, $1);
```
This well parse `'1' '2' '3'` as AST like (('1', '2'), '3')

```
list : packed text = (*$0, $1);
packed : text text = ($0, $1);
```
This well parse `'1' '2' '3'` as AST like ('1', '2', '3')

> You can write more complex grammar tuple.

Example:
```
function: func_name '(' arg (',' arg)* ')' = func_sign($0, $2, *$3($1));
```

Then you can get `arg (',' arg)*` as a list like `[arg, arg, arg, ...]`.

The `func_sign` at before grammar tuple is grammar name, which use for semantic analyzing.

### Simple example

A example of arithmetic grammar like this:

```
start : E ;
E : E plus T | E minus T | T ;
T : T times F | T div F | F ;
F : F power D | D ;
D : bl E br | N ;
N : int | float ;
```

You also can write literal terminal like this:

```
start : E ;
E : E '+' T | E '-' T | T ;
T : T '*' F | T '/' F | F ;
F : F '^' D | D ;
D : '(' E ')' | N ;
N : int | float ;
```

> NOTICE: The null reduce production present as "~" (without quotation marks) or write nothing.

There are some commands can add to grammar file, these commands start with "%", the form is:

```
%command argument1 argument2 ...
```

The command can be: `start_symbol`, `grammar_analyzer_class_name`, `grammar_class_name` etc.

* `start_symbol`, set the start non-terminal literal.
* `grammar_analyzer_class_name`, set the grammar analyzer name.
* `grammar_class_name`, set the lexical analyzer name.

> You can consult the example at "example/arithmetic_grammar.txt" and "boson_grammar.boson" is boson itself grammar file.

### Easy to use

> Use console command boson to generate code.

You can execute `boson` by type "boson" at console interface.
So that you can see the usage of console command `boson`.

The usage of `boson` is:

```
usage: boson [-h] [-o OUTPUT] [-a {slr,lr,lalr}] [-l {python3}] [-r] [-f]
             grammar_file

Boson v0.9 - Grammar analyzer generator

positional arguments:
  grammar_file          Inpute grammar description file.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output grammar analyzer code.
  -a {slr,lr,lalr}, --analyzer {slr,lr,lalr}
                        Analyzer type (default is LALR).
                          slr  - SLR (Simple LR)
                          lr   - LR (Canonical LR)
                          lalr - LALR (Look-Ahead LR)
  -l {python3}, --language {python3}
                        Generate code language (default is Python3).
                          python3 - Python3 code.
  -r, --report          Report conflict when create grammar analyzer.
  -f, --force           Force generate code when exist conflict.
```

> You can input `boson -h` to get this information.

#### Example

use "example/arithmetic_grammar.txt" to generate "example/arithmetic_grammar_code.py":

```
> boson example/arithmetic_grammar.txt -a SLR -l Python -o example/arithmetic_grammar_code.py
```

### Use boson as library

You can use boson as library, just "import boson".

Of course, you can install the python package, and just import boson module.

Example:

```python
    >>> from boson.bs_grammar_analysis import bs_token_list
    >>> from boson.bs_lalr_generate.py import bs_lalr_generate_table
    >>> from boson.bs_code_generator import bs_generate_python3_code
    >>> grammar_package = bs_grammar_analysis("example/arithmetic_grammar.txt")
    >>> lalr_analyzer_table = bs_lalr_generate_table(grammar_package.sentence_set)
    >>> code = bs_generate_python3_code(lalr_analyzer_table, grammar_package)
    >>> print(code)
```

#### Parse grammar file

"bs_grammar_analysis.py" file contains functions are used to parse grammar file.

**bs_token_list()** function read grammar file and return a token list.

```python
token_list = bs_token_list(grammar_file)
```

**bs_grammar_analysis()** function use token list to generate production sentence set, reduce code
 and some other content as class GrammarPackage.

```python
grammar_package = bs_grammar_analysis(token_list)
```

The class `GrammarPackage` like this:

```python
class GrammarPackage:
    def __init__(self):
        self.command_list = None
        self.sentence_set = None
        self.grammar_tuple_map = None
        self.none_grammar_tuple_set = None
        self.literal_map = None
        self.literal_reverse_map = None
        self.sentence_grammar_map = None
        self.naive_sentence = None
```

Now, the final result of "bs_grammar_analysis.py" is data_package, which contains many things used by generator
 and analyzer.

#### Generate analyzer table

Use sentence list to generate analyzer table, just import corresponding generator file of one analyzer type.

For example, if we want to generate SLR analyzer, import "bs_slr_generate.py".

**bs_slr_generate_table()** function use sentence list to create all tables used by analyzer(DFA).
It returns a tuple, which contains these tables.

```python
tables_tuple = bs_slr_generate_table(sentence_list)
```

#### Generate analyzer code

All code generator use analyzer table to generate code of grammar analyzer.

> Import "bs_code_generate.py" file, which include code generators of all languages.

Each generator is a function, now, I am already finished Python3 code generator, and it definition is:

##### Python3 code generator definition

`bs_generate_python3_code(analyzer_table: AnalyzerTable, grammar_package: GrammarPackage)`

**analyzer_table** is grammar analyzer tables, which output by SLR, LR, or LALR generator.

**grammar_package** is a class contains reduce code, literal and many other things.

## Reference

Boson can generate SLR, LR, LALR analyzer.

All analyzer input is `sentence_set`, which created by `bs_grammar_analysis.py`.

They all have a `dfa generate function` and `table generate function`.

`dfa generate function` returns `state_list` and `state_transfer`.

`table generate function` returns `AnalyzerTable`

```python
class AnalyzerTable:
    def __init__(self):
        self.terminal_index = None
        self.action_table = None
        self.goto_table = None
        self.reduce_symbol_sum = None
        self.reduce_to_non_terminal_index = None
        self.sentence_list = None
        self.conflict_list = None
```

### SLR - Simple LR

SLR in boson means SLR(1), it is fast and simple, but it only can recognize a few grammars.

> boson.bs_slr_generate

`bs_slr_generate_dfa(sentence_set)` function can generate SLR DFA.

`bs_slr_generate_table(sentence_set)` function can generate SLR table.

### LR - canonical LR

LR in boson means LR(1), it is slower than SLR, but can recognize more grammar. And its table will bigger than SLR.

> boson.bs_lr_generate

`bs_lr_generate_dfa(sentence_set)` function can generate LR DFA.

`bs_lr_generate_table(sentence_set)` function can generate LR table.

### LALR - Look-Ahead LR

LALR in boson means LALR(1), it is slow like LR, and can recognize more grammar than SLR, but less than LR.
The feature is that its table size is the same as SLR.

> boson.bs_lalr_generate

`bs_lalr_generate_dfa(sentence_set)` function can generate LALR DFA.

`bs_lalr_generate_table(sentence_set)` function can generate LALR table.

* * *

## Author

Author: ict

Email: ictxiangxin@gmail.com

Email: ictxiangxin@hotmail.com
