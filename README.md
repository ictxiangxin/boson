# Boson - 语法分析器生成器

![Version](https://img.shields.io/badge/Version-1.5-blue.svg)
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

# Boson脚本

Boson脚本可分为三部分：

* 命令。
* 词法定义。
* 语法定义。

这三部分在脚本编写时无顺序关系。

Boson脚本中有一个很重要的概念叫做“符号”，符号是字母、数字加下划线的组合（数字不能出现在首位）。
“符号”是命令、词法定义和语法定义的重要组成部分。

## 命令

命令的结构较为简单，都为如下形式：

```
%命令 参数1 参数2 ...;
```

命令都以`%`符号开头，后面为合法的符号。
在命令名中，下划线命名和驼峰命名本质上是相同意义。例如`%start_symbol`与`%StartSymbol`等价。

在当前的Boson版本中，实现的所有命令都只有一个参数，以下为所有命令的清单:

|命令名|参数范围|默认值|备注|
|:-|:-:|:-:|:-|
|%start_symbol|任意符号名|start|指明脚本中语法定义的起始语法符号。|
|%token_class_name|任意变量名|BosonToken|生成代码中词法符号的类名。|
|%lexer_class_name|任意变量名|BosonLexer|生成代码中词法分析器类名。|
|%parser_class_name|任意变量名|BosonParser|生成代码中语法分析器类名。|
|%grammar_class_name|任意变量名|BosonGrammar|生成代码中语法结构类名。|
|%grammar_node_class_name|任意变量名|BosonGrammarNode|生成代码中语法节点类名。|
|%interpreter_class_name|任意变量名|BosonInterpreter|生成代码中语义分析器类名。|
|%semantic_node_class_name|任意变量名|BosonSemanticsNode|生成代码中语义节点类名。|
|%generate_interpreter|yes/no|yes|是否生成语义分析器代码。|
|%generate_lexer|yes/no|yes|是否生成词法分析器代码。|
|%code_comment|yes/no|yes|是否在生成代码中显示版本版权等信息。|
|%parser_sparse_table|yes/no|yes|语法分析器是否生成稀疏分析表。|
|%lexer_compact_table|yes/no|yes|词法分析器是否生成压缩分析表。|
|%conflict_resolver|yes/no|no|是否开启内置冲突解决器。|
|%shift_reduce_conflict_resolver|shift/reduce|shift|“移入-规约”冲突的解决方式，“shift”为移入优先，“reduce”为规约优先。|
|%reduce_reduce_conflict_resolver|long/short|long|“规约-规约”冲突的解决方式，“long”为最长优先，“short”为最短优先。|

### 示例

1. 设置脚本的语法定义起始符号为`S`：`%StartSymbol S;`

2. 打开内置冲突解决器：`%ConflictResolver yes;`

3. 设置“移入-规约”冲突的解决方式为规约优先：`%ShiftReduceConflictResolver reduce;`

## 词法定义

词法定义的结构为如下形式：

```
词法符号 : 正则表达式 [!] [@{ 词法函数列表 }];
```

### 词法符号

`词法符号`为任意合法的符号。当词法符号以`_`（下划线）开头时，该词法定义将被视为隐藏定义，
不会纳入至最终的词法定义中，词法的隐藏定义通常用于正则表达式中的“引用”。

### 正则表达式

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

#### 示例

* `<[_a-zA-Z][_a-zA-Z0-9]*>`为下划线、字母和数字的任意组合，其中数字不能出现在首位。
* `<".*[^\\]"|'.*[^\\]'>`为双引号`"`或单引号`'`包围的字符串。

### 词法定义后缀

词法定义后缀分为两部分组成，前者为非贪婪标志，用`!`表示；
后者为词法函数列表，由`@`符号引出，花括号（`{`、`}`）包围的词法函数名。
这两部分均为可选项。

#### 非贪婪标志

在词法定义的正则表达式之后加入`!`代表该表达式为非贪婪匹配，当检索到相匹配的文本时立即生成对应的词法单元。

例如`string = <".*[^\\]"|'.*[^\\]'>!;`表明字符串的词法定义是非贪婪匹配。

#### 词法函数列表

词法函数列表中可包含任意合法的符号名，有多个以空格隔开。
目前Boson有两个内置词法函数，分别为`skip`和`newline`。
`skip`表明该词法定义只匹配，但不生成词法单元。
`newline`表示词法分析器的行计数器加1。

如果词法函数中加入自定义的词法函数，则需要在后续调用注册函数进行自定义函数注册。

例如`newline = <\n\r|\n>@{skip, newline};`代表在匹配到换行时，忽略这些换行符，并且使行计数器加1。

## 语法定义

Boson的语法定义类似EBNF的写法，但所用符号上更接近正则表达式的写法。

语法定义的结构通常如下：
```
语法符号 : 规约式 [= [语法元组名称]语法元组定义] | 规约式 [= [语法元组名称]语法元组] | ...;
```

### 语法符号

`语法符号`为为任意合法的符号。所有语法定义中必须包含一个语法符号为`起始语法符号`。

`起始语法符号`是整个脚本语法定义的起始，可通过`%start_symbol`命令进行设定，也可直接使用默认的`start`符号。

### 规约式

`规约式`是由若干个`语法符号`、`词法符号`和`文本词法`以类似EBNF的方式组成。

> 其中`文本词法`为语法定义的特殊元素，其表现形式为普通的字符串，代表该位置为一个以该字符串表示的词法单元。

下文中`symbolN`表示为`语法符号`、`词法符号`和`文本词法`中的一种。

#### 常规规约式

`规约式`可由上述元素以空格隔开的方式进行排列：
```
symbol0 : symbol1 symbol2 symbol3;
```

#### 子规约式

使用圆括号（`(`、`)`）包围的规约式称为`子规约式`:
```
symbol0 : symbol1 (symbol2 symbol3) symbol4;
```
> `子规约式`将构造一个隐藏的语法符号和对应的`规约式`

上述示例将实际扩展为：
```
symbol0 : symbol1 hidden_symbol0 symbol4;
hidden_symbol0 : symbol2 symbol3;
```
其中`hidden_symbol0`为Boson生成的隐藏语法符号。

#### 闭包

所有`规约式`元素（包括`symbolN`、`子规约式`等）均可使用`闭包后缀`构造闭包：
```
symbol0 : symbol1+ (symbol2 symbol3)* symbol4;
```
闭包后缀的分为2种，其含义与正则表达式中的闭包类似:
* `*`为克林闭包，代表该元素可以为0个或重复任意多个。
* `+`为正闭包，代表该元素至少为1个或重复任意多个。
> `闭包`同样会生成相应的`隐藏语法符号`和`规约式`。

##### 示例

列表的词法符号`list`的规约式为至少1个或任意多个`number`构成：
```
list: number+;
```
或者该列表可以为空:
```
list: number*;
```

#### 可选项

使用方括号（`[`、`]`）包围的规约式称为`可选项`：
```
symbol0 : [symbol1 symbol2] symbol3;
```
`可选项`的含义要么存在要么不存在。

上述语法定义等价于：
```
symbol0 : symbol3;
symbol0 : symbol1 symbol2 symbol3;
```

#### 选择项

使用竖线（`|`）隔开的元素为`选择项`：
```
symbol0 : symbol1 | symbol2 | symbol3;
```
等价于：
```
symbol0 : symbol1;
symbol0 : symbol2;
symbol0 : symbol3;
```

### 语法元组

`语法元组`是`语法定义`中的一个可选特性，用于修改、化简、构造由`语法定义`描述的`抽象语法树`。

语法元组包含2部分：
* `语法元组名称`，用于`语义分析`时语义动作的注册和定位。
* `语法元组定义`，描述该语法定义的`语法元组`结构。

#### 语法元组名称

`语法元组名称`为任意合法的符号，同名的语法元组名称将获得相同的语义分析动作。

#### 语法元组定义

`语法元组定义`大致结构如下：
```
(元组元素, 元组元素, ...)
```
`元组元素`可为下列6种形式：
1. `语法节点`
2. `*语法节点`
3. `语法节点 子语法元组定义`
4. `*语法节点 子语法元组定义`
5. `语法节点 *子语法元组定义`
6. `*语法节点 *子语法元组定义`

其中：
* `语法节点`可表示为`$N`，`N`代表语法元素在`规约式`中的下标。
* `子语法元组定义`以圆括号（`(`、`)`）包围，代表规约式中`子规约式`（含`闭包`）或`可选项`内部的`语法元组定义`。
* `*`通常在`语法节点`之前或`子语法元组定义`之前，代表其后的`语法节点`或`子语法元组定义`构造`抽象语法树节点`需解包。

#### 基本用法
对于`常规规约式`，可通过`语法元组定义`改变其`抽象语法树`中的元素顺序或舍弃部分无语义的元素。

例如中置运算符的计算式的语法定义使用逆波兰式的语法元组：
```
expression : a '+' b = ($1, $0, $2);
```
在解析过程中产生的`抽象语法树`节点将被构造成`('+', a, b)`。

或子计算中舍弃无语义的标点符号：
```
expression : '(' expression ')' = ($1);
```

#### 包含“子规约式”和“可选项”的用法
对于这类规约式，需定义`子规约式`和`可选项`的`语法元组`就需要用到`子语法元组定义`。

##### 基本用法

中置运算符`语法定义`的扩展：
```
expression : a ('+' | '-' | '*' | '/') b = ($1, *$0, $2);
```
其`语法元组定义`生成的`抽象语法树节点`结构为`(运算符, a, b)`，其中`运算符`为`+`、`-`、`*`、`/`中的一种。

##### 复杂用法

例如一个函数调用的`语法定义`如下：
```
invoke_function : function_name '(' argument (',' argument)* ')' = ($0, $2, *$3*($1));
```
其`语法元组定义`生成的`抽象语法树节点`结构为`(function_name, argument, argument, ...)`。

具体分析如下：
* `$0`代表取`规约式`中索引为`0`的语法元素，也就是`function_name`。
* `$2`代表取`规约式`中索引为`2`的语法元素，也就是`argument`。
* `*$3*($1)`为上述`元组元素`的第6种情况`*语法节点 *子语法元组定义`。

对于`*$3*($1)`，拆解出`$3`代表定义索引为`3`的语法元素，
也就是`(',' argument)*`。

而`*$3`中的`*`代表该语法元素需要解包。
如果此处没有`*`，那么`抽象语法树节点`结构将变为`(function_name, argument, (argument, ...))`，
因此“解包”的含义也一目了然。

后续`*($1)`中的`($1)`为`子语法元组定义`，其定义是`(',' argument)*`的`语法元组`，该语法由两层组成，
第一层为`克林闭包`：`(...)*`，第二层为克林闭包内部的`(',' argument)`。因此该`子语法元组定义`定义的便是
`(',' argument)`的`语法元组`。容易理解`$1`代表索引为`1`的语法元素也就是`argument`。
而`*($1)`中的`*`代表该语法元素需要解包。如果此处没有`*`，
那么`抽象语法树节点`结构将变为`(function_name, argument, (argument), (argument)...)`。

## 使用Boson生成的分析器

目前Boson可生成`Python3`和`C++`两种语言的代码。

### Python3

在编写完Boson脚本文件之后，例如`test.boson`，使用Boson生成其对应的分析器代码（使用`lalr`分析器）：
> `boson test.boson -a lalr -l python3 -o test.py`

执行成功之后，当前目录下便会生成`test.py`文件。

使用方式也较为简便，假设从文件`test.txt`获取将要解析的文本：
```python
with open('test.txt', 'r', encoding='utf-8') as f:
    text = f.read()
```

构造`test.py`文件中的词法分析器并对文本进行解析获得`词法单元`列表：
```python
from test import BosonLexicalAnalyzer

with open('test.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    lexer = BosonLexicalAnalyzer()
    if lexer.tokenize(text) != lexer.no_error_line():
        "到这里说明文本有词法错误"
    token_list = lexer.token_list()
```

接下来调用`test.py`文件中的语法分析器构造`抽象语法树`：
```python
from test import BosonLexicalAnalyzer, BosonGrammarAnalyzer

with open('test.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    lexer = BosonLexicalAnalyzer()
    if lexer.tokenize(text) != lexer.no_error_line():
        "到这里说明文本有词法错误"
    token_list = lexer.token_list()
    parser = BosonGrammarAnalyzer()
    grammar = parser.parse(token_list)
    if grammar.error_index != grammar.no_error_index():
        "到这里说明有语法错误"
```

到这一步分析器已经生成完整的`抽象语法树`，使用者可以选择自行去解析`抽象语法树`做相应的后续语义分析等工作。
也可以使用Boson生成的语义分析器进行便捷的语义分析。

加入`test.boson`中定义了如下语法：
```
print_string: 'print' '(' string ')' = print($2);
```
那么就需要向语义分析器注册名为`print`的语义动作：
```python
from test import BosonLexer, BosonParser, BosonInterpreter

with open('test.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    lexer = BosonLexer()
    if lexer.tokenize(text) != lexer.no_error_line():
        "到这里说明文本有词法错误"
    token_list = lexer.token_list()
    parser = BosonParser()
    grammar = parser.parse(token_list)
    if grammar.error_index != grammar.no_error_index():
        "到这里说明有语法错误"
    interpreter = BosonInterpreter()
    @interpreter.register_action('print')
    def _print(grammar_entity): # 根据语法元组定义只有一个参数，因此len(grammar_entity) == 1。
        print(grammar_entity[0])
    interpreter.execute(grammar.grammar_tree) # 对抽象语法树执行语义分析。
```

至此，程序已经结束。使用Boson生成分析器代码，可以很方便进行调用，进行许多涉及语法分析的工作。

### C++

此处有一个利用Boson和mpfr构造高精度计算器的例子（有详细构造过程和使用说明）：

[Github地址](https://github.com/ictxiangxin/calculator)

## 联系作者

> 作者：ict

> 电子邮件：ictxiangxin@hotmail.com
