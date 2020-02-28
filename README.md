# Boson - 语法分析器生成器

![Version](https://img.shields.io/badge/Version-1.2-blue.svg)
![Python](https://img.shields.io/badge/Python-3.7.0-green.svg)
![C++](https://img.shields.io/badge/C++-11-green.svg)

Boson是一个语法分析器生成器（也能生成词法分析器）。采用自有的Boson脚本（Boson Script）来定义语法和词法，
Boson根据输入的脚本内容和命令参数生成相应的语法分析器及词法分析器的代码。

> Boson需要Python3的运行环境。

* * *

## 安装

Boson可通过pip命令安装或从源码进行安装：

### pip命令安装
 
> `pip install boson`

### 从源码安装

从GitHub的代码仓库下载或克隆Boson的源代码，在源码根目录下执行：
`python setup.py install`或`python3 setup.py install`
命令进行安装。

* * *

### 使用手册

安装Boson之后，在控制台输入`boson`即可运行Boson。
输入`boson -h`以查看Boson的简要的使用说明：

```
usage: boson [-h] [-o OUTPUT] [-a {slr,lr,lalr}] [-l {python3,c++}] [-f] [-q]
             boson_script_file

Boson v1.3 - Grammar analyzer generator

positional arguments:
  boson_script_file     Input Boson Script File.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output Lexer&Parser Code File.
  -a {slr,lr,lalr}, --analyzer {slr,lr,lalr}
                        Grammar Analyzer Type (Default Is LALR).
                          slr  - SLR(1) (Simple LR)
                          lr   - LR(1) (Canonical LR)
                          lalr - LALR(1) (Look-Ahead LR)
  -l {python3,c++}, --language {python3,c++}
                        Generate Code Program Language (Default Is Python3).
                          python3 - Python3 Code.
                          c++ - C++ Code.
  -f, --force           Force Generate Parse Table When Exist Conflicts.
  -q, --quiet           Display Nothing.
```

Boson运行命令形式简单，可归纳为`boson <Boson脚本文件> <其他各项参数>`。

上述所列参数详细说明如下：

1. `-h`或`--help`，Boson将显示简要的使用说明。
2. `-o`或`--output`，该参数后跟输出代码文件的文件名（包括文件路径）。
3. `-a`或`--analyzer`，指定Boson使用的语法分析器，目前支持`slr`、`lr`、`lalr`，默认为`lalr`。
4. `-l`或`--language`，指定生成代码的编程语言，目前支持`python3`、`c++`，默认为`c++`。
5. `-f`或`--force`，在有语法冲突时，强制生成代码，后续手动解决冲突问题。
6. `-q`或`--quiet`，安静模式，Boson运行时不输出任何信息。

### Boson的自举

Boson自身的部分代码也由Boson生成（该过程称为“自举”）。

> `boson/boson_script/boson_script_parser.py`文件是由`boson boson_script.boson -a lalr -l python3 -o boson_script_parser.py`生成。

> `boson/lexer_generator/regular_parser.py`文件是由`boson regular.boson -a lalr -l python3 -o regular_parser.py`生成。

上述命令中用到的`boson_script.boson`文件和`regular.boson`是两个Boson脚本文件，可在Boson源码的根目录找到。


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
