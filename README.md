# Boson - Grammar Analyzer Generator

![Version](https://img.shields.io/badge/Version-1.2-blue.svg)
![Python](https://img.shields.io/badge/Python-3.7.0-green.svg)
![C++](https://img.shields.io/badge/C++-17-green.svg)

Boson can use production sentences like EBNF which given by user to generate grammar analyzer code.

> Only support Python3.

* * *

## Install

> Use `pip`: `pip install boson`

This way may get the lastest release version.

> Install from source code

You just need download the ZIP file, and unZIP it, type the command:
 `python3 setup.py install` or `sudo python3 setup.py install`

Or Clone it from Github:

`git clone https://github.com/ictxiangxin/boson`

 Type the command: `python3 setup.py install` or `sudo python3 setup.py install`

* * *

### Usage

> Use console command boson to generate code.

You can execute `boson` by type "boson" at console interface.
You can see the usage of console command `boson -h`.

The usage of `boson` is:

```
usage: boson [-h] [-o OUTPUT] [-a {slr,lr,lalr}] [-l {python3,c++}] [-f] [-q]
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
  -l {python3,c++}, --language {python3,c++}
                        Generate code language (default is Python3).
                          python3 - Python3 code.
                          c++ - C++ code.
  -f, --force           Force generate code when exist conflict.
  -q, --quiet           Do not output code when executing boson script.
```

## Boson Script

Boson read file named boson script which contains a set of productions like EBNF.

There are 2 types of boson script statements:
* Command statements.
* Sentence statements. 

### Command Statements

Command statements syntax like this:

```
%command argument1 argument2 ...;
```

`command` must start with `%` symbol and value is any word or string.

In current version, boson has these commands:

|Command|Value Type|Value Range|Comment|
|:-|:-:|:-|:-|
|%start_symbol|Words|Any|Determine the start symbol name of script|
|%lexical_token_class_name|Words|Any|Set lexical token class name of result code|
|%grammar_analyzer_class_name|Words|Any|Set grammar analyzer class name of result code|
|%grammar_class_name|Words|Any|Set grammar class name of result code|
|%grammar_node_class_name|Words|Any|Set grammar node class name of result code|
|%semantics_analyzer_class_name|Words|Any|Set semantics analyzer class name of result code|
|%generate_semantics_analyzer|Bool|yes/no|Determine weather generate semantics analyzer code|
|%code_comment|Bool|yes/no|Determine weather generate comment header in result code|
|%sparse_table|Bool|yes/no|Determine weather use sparse grammar table in result code|

You can also write command like this:

`%StartSymbol`, instead of use `_` join each word, this style is equal to `%start_symbol`.

### Sentence Statements

Sentence statements syntax like this:

```
symbol : <derivation> = [grammar name]<grammar tuple> | <derivation> = [grammar name]<grammar tuple> | ... ;
```

There is a convention which must exist a non-terminal named "start"

#### Derivation

`derivation` looks like EBNF, but that is a little different.

Derivation is made up by a list of symbols which split by blank space:

```
symbol1 symbol2 ...
```

You can use `(` and `)` to group a set of symbols to form a sub-derivation:

```
symbols1 (symbol2 symbols3) symbols4 ...
```

Each symbol or sub-derivation can use `*` or `+` to present it is a closure:

```
symbols1+ (symbols2 symbols3)* symbols4 ...
```

Closure types:
* `*` present kleene closure which means it's count between 0 and infinite.
* `+` present positive closure which means it's count between 1 and infinite.

For example, We need a number list derivation which at least 1 element:

```
list: number+;
```

Or it can present empty list:

```
list: number*;
```

#### Grammar Tuple

`(grammar tuple)` is the AST node structure of this production and it's not necessary.

**Notice**

1.`[grammar name]` satisfied `[_a-zA-Z][_a-zA-Z0-0]*`, it used to name this derivation to help semantics analyzer and it is not necessary.

2.`(grammar tuple)` satisfied `($$, $0, $1, ...)`, it surround with `(` and `)`, contains a set of node symbols.

> node symbols `$$, $0, $1, ...` has special meaning:

* `$$`, the number of this derivation.
* `$?`, all elements of sub-derivation.
* `$0 $1 $2 ...`, the index of element of this derivation(base-0).

> You can write more complex grammar tuple.

Example:
```
function: func_name '(' arg (',' arg)* ')' = func_sign($0, $2, *$3($1));
```

Then you can get `arg (',' arg)*` as a list like `[arg, arg, arg, ...]`.

The `func_sign` is grammar name, which use for semantic analyzing.

### Simple Example

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

#### Console command

Use "example/arithmetic_grammar.txt" to generate "example/arithmetic_grammar_code.py":

```
> boson example/arithmetic_grammar.txt -a slr -l python3 -o example/arithmetic_grammar_code.py
```

## Algorithm

Boson can generate SLR, LR, LALR analyzer.

1.SLR(Simple LR) in boson means SLR(1), it is fast and simple, but it only can recognize a few grammars.

2.LR(Canonical LR) in boson means LR(1), it is slower than SLR, but can recognize more grammar. And its table will bigger than SLR.

3.LALR(Look-Ahead LR) in boson means LALR(1), it is slow like LR, and can recognize more grammar than SLR, but less than LR.
The feature is that its table size is the same as SLR.

* * *

## Author

Author: ict

Email: ictxiangxin@gmail.com

Email: ictxiangxin@hotmail.com
