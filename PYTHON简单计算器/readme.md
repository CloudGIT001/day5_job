####  PYTHON 简单计算器程序

##### 项目需求：
```
模拟计算器开发：
实现加减乘除及拓号优先级解析
用户输入 1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )等类似公式后，
必须自己解析里面的(),+,-,*,/符号和公式(不能调用eval等类似功能偷懒实现)，运算后得出结果，结果必须与真实的计算器所得出的结果一致
```

##### 程序功能介绍：
```
模拟实现科学计算器，可以实现对表达式的优先运算。对表达式的加减乘除及拓号做优先级解析

[^0-9\.\-\+\*\/\%\/\/\*\*\(\)]   #匹配表达式是否合法

\(([\+\-\*\/\%\/\/\*\*]*\d+\.*\d*){2,}\) #匹配只有一层括号的表达式

\d+\.?\d*[\+\-]{1}\d+\.?\d*  #匹配加减法的表达式

\d+\.?\d*[\*\/\%\/\/]+[\+\-]?\d+\.*\d*  #匹配乘除法的表达式

```

##### 依赖关系：
```
运行环境：
Python3.6

依赖软件包：
import re
import sys
```


##### 运行表达式和结果示例：
```
*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
*                                                  *
*              欢迎使用PYTHON简易计算器            *
*                                                  *
*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*

输入表达式不能带空格或带英文字符按任意键继续:
请输入运算表达式[q=quit]>>>:1-2*((60-30+(-40/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))
['-40/5', 0]
result>>: -8.0
oper_result: 1-2*((60-30+-8.0*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))
['9-2*5/3+7/3*99/4*2998+10*568/14', 0]
result>>: 173545.88095238098
oper_result: 1-2*((60-30+-8.0*173545.88095238098)-(-4*3)/(16-3*2))
['60-30+-8.0*173545.88095238098', 0]
result>>: -1388337.0476190478
oper_result: 1-2*(-1388337.0476190478-(-4*3)/(16-3*2))
['-4*3', 0]
result>>: -12.0
oper_result: 1-2*(-1388337.0476190478--12.0/(16-3*2))
['16-3*2', 0]
result>>: 10.0
oper_result: 1-2*(-1388337.0476190478--12.0/10.0)
['-1388337.0476190478--12.0/10.0', 0]
result>>: -1388335.8476190479
oper_result: 1-2*-1388335.8476190479
['1-2*-1388335.8476190479', 0]
result>>: 2776672.6952380957
2776672.6952380957
请输入运算表达式[q=quit]>>>:q
成功退出计算器

Process finished with exit code 0
```
