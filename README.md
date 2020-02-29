# Boson - 语法分析器生成器

![Version](https://img.shields.io/badge/Version-1.3-blue.svg)
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

> `boson/boson_script/boson_script_parser.py`文件是由`boson boson_script.boson -o boson_script_parser.py`生成。

> `boson/lexer_generator/regular_parser.py`文件是由`boson regular.boson -o regular_parser.py`生成。

上述命令中用到的`boson_script.boson`文件和`regular.boson`是两个Boson脚本文件，可在Boson源码的根目录找到。

## Boson脚本

Boson脚本可分为三部分：

* 命令。
* 词法定义。
* 语法定义。

这三部分在脚本编写时无顺序关系。

Boson脚本中有一个很重要的概念叫做“符号”，符号是字母、数字加下划线的组合（数字不能出现在首位）。
“符号”是命令、词法定义和语法定义的重要组成部分。

### 命令

命令的结构较为简单，都为如下形式：

```
%命令 参数1 参数2 ...;
```

命令都以`%`符号开头，后面为合法的符号。
在命令名中，下划线命名和驼峰命名本质上是相同意义。例如`%start_symbol`与`%StartSymbol`等价。

在当前的Boson版本中，实现的所有命令都只有一个参数，以下为所有命令的清单:

|命令名|参数范围|默认值|备注|
|:-|:-:|:-|:-|
|%start_symbol|任意符号量名|start|指明脚本中语法定义的起始语法符号。|
|%lexical_token_class_name|任意变量名|BosonToken|生成代码中词法符号的类名。|
|%lexical_analyzer_class_name|任意变量名|BosonLexicalAnalyzer|生成代码中词法分析器类名。|
|%grammar_analyzer_class_name|任意变量名|BosonGrammarAnalyzer|生成代码中语法分析器类名。|
|%grammar_class_name|任意变量名|BosonGrammar|生成代码中语法结构类名。|
|%grammar_node_class_name|任意变量名|BosonGrammarNode|生成代码中语法节点类名。|
|%semantics_analyzer_class_name|BosonSemanticsAnalyzer|任意变量名|生成代码中语义分析器类名。|
|%semantics_node_class_name|BosonSemanticsNode|任意变量名|生成代码中语义节点类名。|
|%generate_semantics_analyzer|yes/no|yes|是否生成语义分析器代码。|
|%generate_lexical_analyzer|yes/no|yes|是否生成词法分析器代码。|
|%code_comment|yes/no|yes|是否在生成代码中显示版本版权等信息。|
|%sparse_table|yes/no|yes|是否生成稀疏分析表。|
|%conflict_resolver|yes/no|no|是否开启内置冲突解决器。|
|%shift_reduce_conflict_resolver|shift/reduce|shift|“移入-规约”冲突的解决方式，“shift”为移入优先，“reduce”为规约优先。|
|%reduce_reduce_conflict_resolver|long/short|long|“规约-规约”冲突的解决方式，“long”为最长优先，“short”为最短优先。|

#### 示例

1. 设置脚本的语法定义起始符号为`S`：`%StartSymbol S;`

2. 打开内置冲突解决器：`%ConflictResolver yes;`

3. 设置“移入-规约”冲突的解决方式为规约优先：`%ShiftReduceConflictResolver reduce;`

### 词法定义

词法定义的结构为如下形式：

```
词法符号 : 正则表达式 [!] [@{ 词法函数列表 }];
```

#### 词法符号

`词法符号`为任意合法的符号。当词法符号以`_`（下划线）开头时，该词法定义将被视为隐藏定义，
不会纳入至最终的词法定义中，词法的隐藏定义通常用于正则表达式中的“引用”。

#### 正则表达式

Boson的正则表达式由一对尖括号包围（`<`、`>`），起表达式结构对于词法定义进行设计和化简，基本语法与主流正则表达式相近。

Boson正则表达式支持语法如下：

1. 字符串定义，任意普通字符组合的字符串，
例如`<boson>`为匹配“boson”字符串。

2. 区间定义，用短横线（`-`）连接两个字符形成区间定义，
例如`<0-9>`为匹配“0123456789”中任意1个字符。

3. 选择定义，用竖线（`|`）分割的任意正则定义为选择定义，
例如`<boson|Boson>`为匹配“boson”或“Boson”字符串。

4. 正闭包，在任意正则定义后面加入`+`形成正闭包，
例如`<a+>`为匹配至少一个字符“a”。

5. 克林闭包，在任意正则定义后面加入`*`形成克林包，
例如`<a*>`为匹配若干个字符（可以为0个）字符“a”。

6. 数量区间，在任意正则定义后面加入`{n,m}`代表至少`n`个至多`m`个，
例如`<a{2,3}>`为匹配至少2个至多3个字符“a”。

7. 可有可无，在任意正则定义后面加入`？`代表要么只有1个要么是0个，
其效果与`{0,1}`等价，例如`<a？>`代表配1个字符“a”或没有字符“a”。

8. 选择集，使用方括号包围（`[`、`]`）的若干字符集（可含有区间定义），
例如`<[a-zA-Z]>`为匹配1个任意大小写的英文字母。

9. 选择集补集，在选择集的`[`后紧跟`^`代表该选择集为补集，
例如`<[^0-9]>`为匹配1个除“0123456789”以外的任意字符。

10. 子定义，使用圆括号包围（`[`、`]`）的任意正则定义为子定义，
例如`<(boson|Boson)+>`为匹配“boson”与“Boson”的任意组合。

11. 通配符，`.`为正则通配符，例如`<boson.*>`为匹配以“boson”开头的任意文本。
注意通配符不能出现在选择集、选择集补集中。

12. 字符转义，以`\`接字符进行转义，转义分为两种情况：
一是将具有语法含义的正则符号转为普通符号，例如`<\.>`匹配字符“.”而非通配；
二是将普通字符转为特殊字符或特殊正则定义，例如`<\n>`匹配换行符而非字符“n”。
目前Boson支持6种普通字符转义：
`\n`代表换行符，`\r`代表回车符，`\t`代表制表符，`\d`代表`0-9`，`\w`代表`a-z`，`\W`代表`A-Z`。

13. 引用，使用花括号包围（`{`、`}`）的其他词法符号为引用该词法符号。
例如有词法定义`_number = <[0-9]+>`，则`<boson{_number}>`匹配以“boson”开头后接任意数字组合的文本。

##### 示例

* `<[_a-zA-Z][_a-zA-Z0-9]*>`为下划线、字母和数字的任意组合，其中数字不能出现在首位。

* `<".*[^\\]"|'.*[^\\]'>`为双引号`"`或单引号`'`包围的字符串。

#### 词法定义后缀

词法定义后缀分为两部分组成，前者为非贪婪标志，用`!`表示；
后者为词法函数列表，由`@`符号引出，花括号（`{`、`}`）包围的词法函数名。
这两部分均为可选项。

##### 非贪婪标志

在词法定义的正则表达式之后加入`!`代表该表达式为非贪婪匹配，当检索到相匹配的文本时立即生成对应的词法单元。

例如`string = <".*[^\\]"|'.*[^\\]'>!;`表明字符串的词法定义是非贪婪匹配。

##### 词法函数列表

词法函数列表中可包含任意合法的符号名，有多个以空格隔开。
目前Boson有两个内置词法函数，分别为`skip`和`newline`。
`skip`表明该词法定义只匹配，但不生成词法单元。
`newline`表示词法分析器的行计数器加1。

如果词法函数中加入自定义的词法函数，则需要在后续调用注册函数进行自定义函数注册。

例如`newline = <\n\r|\n>@{skip, newline};`代表在匹配到换行时，忽略这些换行符，并且使行计数器加1。

### 语法定义

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

Email: ictxiangxin@hotmail.com
